# Generated by Django 4.1.5 on 2023-02-15 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_user_liked_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='liked_num',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
