# Generated by Django 3.2.9 on 2021-11-12 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0003_pet_animal_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='color',
            field=models.CharField(default='braun', max_length=15),
            preserve_default=False,
        ),
    ]
