# Generated by Django 4.2.10 on 2024-04-05 22:30

from django.db import migrations
import django_ckeditor_5.fields


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_alter_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=django_ckeditor_5.fields.CKEditor5Field(blank=True, verbose_name='Содержание'),
        ),
    ]
