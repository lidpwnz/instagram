# Generated by Django 3.2.7 on 2021-09-26 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='subscribes',
            field=models.ManyToManyField(related_name='followers', to='accounts.Profile'),
        ),
        migrations.DeleteModel(
            name='Subscribes',
        ),
    ]
