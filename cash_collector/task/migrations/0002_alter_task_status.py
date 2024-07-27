# Generated by Django 4.2.14 on 2024-07-25 00:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[(1, 'pending'), (2, 'collected'), (3, 'delivered')], default=1, max_length=20),
        ),
    ]
