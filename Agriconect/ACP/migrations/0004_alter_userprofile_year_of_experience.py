# Generated by Django 5.1.5 on 2025-02-04 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("ACP", "0003_remove_userprofile_year_of_joining_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="year_of_experience",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
