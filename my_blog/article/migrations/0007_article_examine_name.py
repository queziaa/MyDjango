# Generated by Django 2.0.3 on 2018-04-24 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0006_user_data_admin'),
    ]

    operations = [
        migrations.AddField(
            model_name='article_examine',
            name='name',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]