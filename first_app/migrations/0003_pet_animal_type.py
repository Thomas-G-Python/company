# Generated by Django 3.2.9 on 2021-11-11 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_pet_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='pet',
            name='animal_type',
            field=models.CharField(choices=[('dog', 'Hund'), ('cat', 'Katze'), ('bird', 'Vogel')], default='dog', max_length=5),
            preserve_default=False,
        ),
    ]
