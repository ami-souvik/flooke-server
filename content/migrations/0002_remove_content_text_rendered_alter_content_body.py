# Generated by Django 5.1 on 2024-08-20 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='text_rendered',
        ),
        migrations.AlterField(
            model_name='content',
            name='body',
            field=models.CharField(max_length=1024),
        ),
    ]
