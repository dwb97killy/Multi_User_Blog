# Generated by Django 4.1 on 2022-09-16 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Blog", "0011_alter_comments_create_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogcontext",
            name="publish_time",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
