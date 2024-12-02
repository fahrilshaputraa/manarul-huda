# Generated by Django 4.2.16 on 2024-11-20 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_websitesettings_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='websitesettings',
            name='location_link',
            field=models.URLField(null=True, verbose_name='GitHub URL'),
        ),
        migrations.AddField(
            model_name='websitesettings',
            name='sub_name',
            field=models.CharField(help_text='Sub Name of the website', max_length=255, null=True),
        ),
    ]
