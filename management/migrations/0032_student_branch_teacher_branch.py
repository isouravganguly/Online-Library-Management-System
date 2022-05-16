# Generated by Django 4.0.4 on 2022-05-16 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0031_rename_book_transfers_eachbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='management.department'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='management.department'),
        ),
    ]