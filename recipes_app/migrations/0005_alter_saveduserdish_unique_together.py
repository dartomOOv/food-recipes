# Generated by Django 5.1.1 on 2024-09-20 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes_app', '0004_alter_dish_slug'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='saveduserdish',
            unique_together=set(),
        ),
    ]
