# Generated by Django 3.1.6 on 2021-02-03 02:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingredient', '0002_auto_20210203_0152'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['id']},
        ),
    ]
