# Generated by Django 4.0.4 on 2022-05-15 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0029_rename_isbn_eachbook_book_remove_eachbook_bid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='circulation',
            name='transfer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='management.transfers'),
        ),
    ]
