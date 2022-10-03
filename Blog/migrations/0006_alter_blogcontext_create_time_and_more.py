# Generated by Django 4.1 on 2022-09-16 16:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Blog", "0005_alter_blogcontext_create_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogcontext",
            name="create_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2022, 9, 16, 16, 13, 28, 315111, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="comments",
            name="create_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2022, 9, 16, 16, 13, 28, 316079, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="userprofileinfo",
            name="profile_pic",
            field=models.ImageField(blank=True, upload_to="static/profile_img"),
        ),
    ]