# Generated by Django 4.2.16 on 2024-11-23 12:46

from django.db import migrations
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_gallery_search_image'),
    ]

    operations = [
        migrations.DeleteModel(
            name='NavigationSettings',
        ),
        migrations.RemoveField(
            model_name='footertext',
            name='body',
        ),
        migrations.AddField(
            model_name='footertext',
            name='menu_items',
            field=wagtail.fields.StreamField([('menu_item', 5)], block_lookup={0: ('wagtail.blocks.CharBlock', (), {'max_length': 100}), 1: ('wagtail.blocks.PageChooserBlock', (), {'required': False}), 2: ('wagtail.blocks.URLBlock', (), {'required': False}), 3: ('wagtail.blocks.StructBlock', [[('title', 0), ('page', 1), ('external_link', 2)]], {}), 4: ('wagtail.blocks.StreamBlock', [[('items', 3)]], {'max_num': 5, 'min_num': 1}), 5: ('wagtail.blocks.StructBlock', [[('title', 0), ('link', 4)]], {})}, null=True),
        ),
        migrations.AddField(
            model_name='footertext',
            name='social_media',
            field=wagtail.fields.StreamField([('social_media', 2)], block_lookup={0: ('wagtail.images.blocks.ImageChooserBlock', (), {'required': False}), 1: ('wagtail.blocks.URLBlock', (), {'required': False}), 2: ('wagtail.blocks.StructBlock', [[('icon', 0), ('link', 1)]], {})}, null=True),
        ),
    ]
