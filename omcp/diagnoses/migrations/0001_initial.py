# Generated by Django 3.1.4 on 2020-12-09 08:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Diagnosis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=50)),
                ('description', models.CharField(default='', max_length=1000)),
                ('video_link', models.CharField(default='', max_length=100)),
                ('video_password', models.CharField(default='', max_length=50)),
                ('type', models.CharField(default='Mental Illness', max_length=50)),
                ('status', models.CharField(default='REGISTERED', max_length=50)),
                ('date', models.DateField(blank=True, null=True)),
                ('image', models.FileField(blank=True, default='diagnoses/no-img.jpg', upload_to='diagnoses/')),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.doctor')),
                ('patient', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.patient')),
            ],
        ),
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('diagnosis', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='diagnoses.diagnosis')),
                ('comment', models.CharField(default='', max_length=1000)),
            ],
        ),
    ]
