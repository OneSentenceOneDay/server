# Generated by Django 4.1.5 on 2023-02-05 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writing', '0005_post_bool_like_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='bool_like_users',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
