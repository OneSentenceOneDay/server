# Generated by Django 4.1.5 on 2023-02-15 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writing', '0013_remove_sentence_day_of_the_week'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='unknown',
            field=models.CharField(max_length=200, null=True),
        ),
    ]