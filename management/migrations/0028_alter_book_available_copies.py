# Generated by Django 4.0.4 on 2022-05-14 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0027_alter_book_available_copies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='available_copies',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
