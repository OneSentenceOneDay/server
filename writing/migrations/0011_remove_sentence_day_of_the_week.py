# Generated by Django 4.1.5 on 2023-02-13 13:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('writing', '0010_sentence_day_of_the_week'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sentence',
            name='day_of_the_week',
        ),
    ]
