from django.urls import path
from wagtail import hooks
from . import views
from django.urls import include

@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        path('comments/', include(([
            path('', views.index, name='index'),
            path('<int:comment_id>/delete/', views.delete_comment, name='delete'),
        ], 'comments'))),  # <-- Tambahin ini
    ]

@hooks.register('register_admin_menu_item')
def register_comments_menu_item():
    from wagtail.admin.menu import MenuItem
    return MenuItem('Comments', '/admin/comments/', icon_name='comment')
