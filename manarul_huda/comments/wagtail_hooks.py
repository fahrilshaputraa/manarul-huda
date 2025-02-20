from django.urls import path
from wagtail import hooks
from . import views
from django.urls import include
from django_comments.models import Comment
from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        path('comments/', include(([
            path('', views.index, name='index'),
            path('<int:comment_id>/delete/', views.delete_comment, name='delete'),
            path('<int:comment_id>/approve/', views.approve_comment, name='approve'),
            path('api/pending-count/', views.get_pending_count, name='pending-count'),
        ], 'comments'))), 
    ]

@hooks.register('register_admin_menu_item')
def register_comments_menu_item():
    from wagtail.admin.menu import MenuItem
    
    return MenuItem(
        label='Comments',
        url=reverse('comments:index'),
        icon_name='comment',
        name='comments',
        classnames='comments-menu-item',
        order=1000,
    )
