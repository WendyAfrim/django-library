# Generated by Django 4.1.4 on 2022-12-13 15:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='library',
            name='department',
            field=models.IntegerField(),
        ),
    ]