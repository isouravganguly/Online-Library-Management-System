# Generated by Django 4.0.4 on 2022-05-09 14:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0018_student_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]