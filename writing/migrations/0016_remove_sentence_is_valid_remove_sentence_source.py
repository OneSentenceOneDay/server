# Generated by Django 4.1.5 on 2023-03-09 21:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('writing', '0015_sentence_source'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sentence',
            name='is_valid',
        ),
        migrations.RemoveField(
            model_name='sentence',
            name='source',
        ),
    ]
