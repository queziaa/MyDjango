# Generated by Django 2.0.3 on 2018-04-12 08:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0004_user_data'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_data',
            old_name='cookie_psaaword',
            new_name='cookie_password',
        ),
    ]