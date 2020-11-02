# Generated by Django 3.1.2 on 2020-10-27 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=600)),
                ('name', models.CharField(max_length=30)),
                ('phone_number', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'db_table': 'accounts',
            },
        ),
    ]
