# Generated by Django 4.2 on 2024-08-28 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0002_remove_content_text_rendered_alter_content_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='body',
            field=models.JSONField(),
        ),
    ]
