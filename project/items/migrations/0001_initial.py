# Generated by Django 4.1.7 on 2023-03-23 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False, unique=True)),
                ('caption', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True, null=True)),
                ('sku', models.CharField(max_length=128)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]