from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_comments.models import Comment
from django.contrib import messages
from .forms import CustomCommentForm
from django.http import JsonResponse

def get_pending_count(request):
    count = Comment.objects.filter(is_public=False, is_removed=False).count()
    return JsonResponse({'count': count})

def index(request):
    comments_list = Comment.objects.all().order_by('-submit_date')  # Ambil semua komentar
    paginator = Paginator(comments_list, 10)  # 10 komentar per halaman

    page_number = request.GET.get('page')  # Ambil nomor halaman dari query params
    comments = paginator.get_page(page_number)  # Dapatkan halaman saat ini

    # Tambahkan initial count untuk JavaScript
    pending_count = Comment.objects.filter(is_public=False, is_removed=False).count()
    
    return render(request, 'comments/admin/list.html', {
        'comments': comments,
        'pending_count': pending_count
    })

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        comment.delete()
        messages.success(request, _("Comment has been deleted."))
        return redirect(request.GET.get('next', 'comments:index'))  # Redirect ke halaman 'next'

    return render(request, 'comments/admin/confirm_delete.html', {
        'comment': comment,
        'next': request.GET.get('next', 'comments:index')
    })

def approve_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.is_public = True
    comment.save()
    return redirect(request.GET.get('next', 'comments:index'))

def post_comment(request, object_id):
    if request.method == 'POST':
        form = CustomCommentForm(request=request, data=request.POST)
        if form.is_valid():
            # Cek apakah user meminta preview
            if 'preview' in request.POST:
                return render(request, 'comments/preview.html', {'form': form})
            
            # Jika tidak, simpan komentar
            comment = form.save()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Untuk request AJAX, return success response
                return JsonResponse({
                    'status': 'success',
                    'message': 'Komentar berhasil dikirim dan menunggu persetujuan admin.'
                })
            
            messages.success(
                request, 
                'Komentar berhasil dikirim dan akan ditampilkan setelah disetujui oleh admin.'
            )
            return redirect(comment.content_object.get_absolute_url())
        else:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Return error untuk request AJAX
                return JsonResponse({
                    'status': 'error',
                    'message': 'Ada kesalahan dalam form.',
                    'errors': form.errors
                }, status=400)
    else:
        form = CustomCommentForm(request=request)
    
    return render(request, 'comments/form.html', {'form': form})