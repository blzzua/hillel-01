# Generated by Django 4.1.7 on 2023-03-31 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feedback', '0002_alter_feedback_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='name',
            field=models.CharField(default='satisfied customer', max_length=255),
        ),
    ]