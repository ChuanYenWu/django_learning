# Generated by Django 5.0.6 on 2024-06-09 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_lunchboxmodel_lunchbox_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='buyingmodel',
            name='buytime',
            field=models.DateField(blank=True, null=True),
        ),
    ]
