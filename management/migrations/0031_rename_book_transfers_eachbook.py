# Generated by Django 4.0.4 on 2022-05-15 17:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0030_alter_circulation_transfer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transfers',
            old_name='book',
            new_name='eachbook',
        ),
    ]
