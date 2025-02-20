from django.templatetags.static import static
from django.utils.html import format_html

from wagtail import hooks

@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('dist/css/custom_admin.css')
    )

@hooks.register('insert_global_admin_js')
def global_admin_js():
    return format_html(
        '<script src="{}"></script>',
        static('dist/js/custom_admin.js')
    )

# @hooks.register('construct_main_menu')
# def hide_snippets_menu_item(request, menu_items):
#     menu_items[:] = [item for item in menu_items if item.name != 'snippets']

# @hooks.register('insert_global_admin_js')
# def global_admin_js():
#     return format_html(
#         '<script src="{}"></script>',
#         static('js/custom_admin.js')
#     )

# Mengubah branding
@hooks.register('construct_main_menu')
def custom_branding(request, menu_items):
    return 'Manarul Huda Buniseuri'