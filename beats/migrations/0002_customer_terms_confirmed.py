# Generated by Django 2.2.2 on 2019-06-12 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='terms_confirmed',
            field=models.BooleanField(default=False),
        ),
    ]
