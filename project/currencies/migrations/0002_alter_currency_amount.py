# Generated by Django 4.1.7 on 2023-05-02 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currencies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currency',
            name='amount',
            field=models.DecimalField(decimal_places=8, default=1, max_digits=18),
        ),
    ]