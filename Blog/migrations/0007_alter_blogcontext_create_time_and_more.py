# Generated by Django 4.1 on 2022-09-16 16:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Blog", "0006_alter_blogcontext_create_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogcontext",
            name="create_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2022, 9, 16, 16, 13, 35, 867582, tzinfo=datetime.timezone.utc
                )
            ),
        ),
        migrations.AlterField(
            model_name="comments",
            name="create_time",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2022, 9, 16, 16, 13, 35, 868540, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]