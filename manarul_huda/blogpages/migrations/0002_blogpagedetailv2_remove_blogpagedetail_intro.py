# Generated by Django 5.0.9 on 2024-11-05 08:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogpages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogPageDetailV2',
            fields=[
                ('blogpagedetail_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='blogpages.blogpagedetail')),
            ],
            options={
                'abstract': False,
            },
            bases=('blogpages.blogpagedetail',),
        ),
        migrations.RemoveField(
            model_name='blogpagedetail',
            name='intro',
        ),
    ]
