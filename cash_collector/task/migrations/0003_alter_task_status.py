# Generated by Django 4.2.14 on 2024-07-25 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_alter_task_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'pending'), (2, 'collected'), (3, 'delivered')], default=1, max_length=20),
        ),
    ]
