# Generated by Django 3.2.11 on 2022-01-30 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VotersList',
            fields=[
                ('aadhaar_no', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=70)),
                ('dob', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('candidate', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('votes', models.IntegerField()),
            ],
        ),
    ]
