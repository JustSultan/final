# Generated by Django 4.0.3 on 2022-08-27 18:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("profiles", "0005_alter_profile_bio"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=models.ImageField(
                default="avatar.png",
                upload_to="avatars/",
                validators=[
                    django.core.validators.FileExtensionValidator(
                        ["png", "jpg", "jpeg"]
                    )
                ],
            ),
        ),
    ]
