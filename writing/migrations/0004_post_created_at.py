# Generated by Django 4.1.5 on 2023-02-02 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writing', '0003_post_like_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]