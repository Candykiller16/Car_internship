# Generated by Django 4.1 on 2022-08-08 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fromdealertoshowroomtransaction',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
        migrations.AddField(
            model_name='fromshowroomtocustomertransaction',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
    ]
