from venv import logger

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand


from ...models import User
from ...patient import Patient
from ...doctor import Doctor
from ...license import License

from diagnoses.register_status import RegisterStatus
from diagnoses.models import Diagnosis

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


def create_doctor_and_diagnosis():
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

    diagnosis_1 = Diagnosis.objects.create(doctor=Doctor.objects.get(user_id=user.id))
    diagnosis_1.title = 'Mental Illness Baster SS'
    diagnosis_1.description = 'Free to talk to me'
    diagnosis_1.video_link = 'https://zoom.us/codeuniversity/1234567890'
    diagnosis_1.video_password = '1qazxsw2'
    diagnosis_1.status = RegisterStatus.UNREGISTERED
    diagnosis_1.date = '2020-12-23'
    diagnosis_1.save()

    diagnosis_2 = Diagnosis.objects.create(doctor=Doctor.objects.get(user_id=user.id))
    diagnosis_2.title = 'Mental Illness'
    diagnosis_2.description = 'Free to talk to me'
    diagnosis_2.video_link = 'https://zoom.us/codeuniversity/1234567890'
    diagnosis_2.video_password = '1qazxsw2'
    diagnosis_2.status = RegisterStatus.UNREGISTERED
    diagnosis_2.date = '2020-12-21'
    diagnosis_2.save()

    diagnosis_3 = Diagnosis.objects.create(doctor=Doctor.objects.get(user_id=user.id))
    diagnosis_3.title = 'Preventive Medicine Trial'
    diagnosis_3.description = 'Free to talk to me'
    diagnosis_3.video_link = 'https://zoom.us/codeuniversity/1234567890'
    diagnosis_3.video_password = '1qazxsw2'
    diagnosis_3.status = RegisterStatus.UNREGISTERED
    diagnosis_3.date = '2020-12-21'
    diagnosis_3.save()

    return user


def create_patient_and_diagnosis():
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

    diagnosis = Diagnosis.objects.create(doctor=Doctor.objects.get(user_id=user.id-1),
                                           patient=Patient.objects.get(user_id=user.id))
    diagnosis.title = 'Mental Illness Baster SS'
    diagnosis.description = 'Free to talk to me'
    diagnosis.video_link = 'https://zoom.us/codeuniversity/1234567890'
    diagnosis.video_password = '1qazxsw2'
    diagnosis.status = RegisterStatus.REGISTERED
    diagnosis.date = '2020-12-23'
    diagnosis.save()

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

    create_doctor_and_diagnosis()
    create_patient_and_diagnosis()
