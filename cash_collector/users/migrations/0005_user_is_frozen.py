# Generated by Django 4.2.14 on 2024-07-27 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_user_total_collected'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_frozen',
            field=models.BooleanField(blank=True, default=None, null=True),
        ),
    ]
