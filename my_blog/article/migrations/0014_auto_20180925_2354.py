# Generated by Django 2.0.7 on 2018-09-25 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0013_auto_20180426_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='Search_db',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marking', models.CharField(max_length=16)),
                ('page_quantity', models.IntegerField()),
                ('page', models.TextField(max_length=10000, null=True)),
                ('examine_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AlterField(
            model_name='article',
            name='user',
            field=models.CharField(max_length=16),
        ),
        migrations.AlterField(
            model_name='user_data',
            name='name',
            field=models.CharField(max_length=14, null=True),
        ),
    ]