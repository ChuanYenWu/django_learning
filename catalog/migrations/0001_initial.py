# Generated by Django 5.0.6 on 2024-06-09 03:20

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BuyingModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for Buy Info')),
                ('customer_name', models.CharField(help_text='Enter customer name', max_length=20)),
                ('customer_phone', models.CharField(help_text='Enter customer phone number', max_length=10)),
                ('meat_num', models.IntegerField(help_text='Enter lunchbox number')),
                ('vege_num', models.IntegerField(help_text='Enter lunchbox number')),
                ('total_cost', models.IntegerField(help_text='Enter total cost')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='LunchboxModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lunchbox_name', models.CharField(help_text='Enter lunchbox name', max_length=20)),
                ('lunchbox_cost', models.IntegerField(help_text='Enter lunchbox cost')),
            ],
            options={
                'ordering': ['lunchbox_name'],
            },
        ),
    ]