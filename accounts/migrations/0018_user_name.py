# Generated by Django 4.1.5 on 2023-02-01 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_remove_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
