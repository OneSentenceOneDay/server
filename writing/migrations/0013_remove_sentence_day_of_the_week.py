# Generated by Django 4.1.5 on 2023-02-13 14:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('writing', '0012_remove_post_bool_like_users_sentence_day_of_the_week'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sentence',
            name='day_of_the_week',
        ),
    ]
