from venv import logger

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand

from ...models import User
from ...patient import Patient
from ...doctor import Doctor
from ...license import License

# python manage.py seed --mode=refresh
from ...validity import Validity

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    User.objects.all().delete()
    Patient.objects.all().delete()
    Doctor.objects.all().delete()
    License.objects.all().delete()


def create_review_doctor():
    user = User.objects.create()
    user.username = 'doctor'
    user.email = 'doctor@code.berlin'
    user.password = make_password('1qazxsw2')
    user.is_doctor = True
    user.is_patient = False
    user.save()

    doctor = Doctor.objects.create(user=user)
    doctor.name = 'doctor'
    doctor.country = 'Germany'
    doctor.address = 'Lohmühlenstraße 65, 12435 Berlin, Germany'
    doctor.zipcode = '12435'
    doctor.phone_number = '+49 30 12085961'
    doctor.image = 'users/no-img.svg'
    doctor.validity = Validity.IN_REVIEW
    doctor.speciality = "IT"
    doctor.save()

    license = License.objects.create(doctor=doctor)
    license.image = 'licenses/sample.jpg'
    license.save()
    logger.info("{} doctor created.".format(doctor))
    return user


def create_patient():
    user = User.objects.create()
    user.username = 'patient'
    user.email = 'patient@code.berlin'
    user.password = make_password('1qazxsw2')
    user.is_patient = True
    user.is_doctor = False
    user.save()

    patient = Patient.objects.create(user=user)
    patient.name = 'patient'
    patient.country = 'Germany'
    patient.address = 'Lohmühlenstraße 65, 12435 Berlin, Germany'
    patient.zipcode = '12435'
    patient.phone_number = '+49 30 12085961'
    patient.image = 'users/no-img.svg'
    patient.request = "IT"
    patient.save()
    logger.info("{} doctor created.".format(patient))
    return user


def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    create_review_doctor()
    create_patient()
