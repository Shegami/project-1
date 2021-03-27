# Generated by Django 3.1.7 on 2021-03-23 16:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shortener',
            old_name='original_url',
            new_name='full_url',
        ),
        migrations.RemoveField(
            model_name='shortener',
            name='date',
        ),
        migrations.AddField(
            model_name='shortener',
            name='create_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='shortener',
            name='short_url',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]
