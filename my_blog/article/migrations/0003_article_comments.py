# Generated by Django 2.0.3 on 2018-04-02 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_remove_article_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='comments',
            field=models.IntegerField(default=0),
        ),
    ]
