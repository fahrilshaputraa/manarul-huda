from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import gettext_lazy as _
from django_comments.models import Comment
from django.contrib import messages
from .forms import CustomCommentForm
def index(request):
    comments_list = Comment.objects.all().order_by('-submit_date')  # Ambil semua komentar
    paginator = Paginator(comments_list, 10)  # 10 komentar per halaman

    page_number = request.GET.get('page')  # Ambil nomor halaman dari query params
    comments = paginator.get_page(page_number)  # Dapatkan halaman saat ini

    return render(request, 'comments/admin/list.html', {'comments': comments})

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

def post_comment(request, object_id):
    if request.method == 'POST':
        form = CustomCommentForm(request=request, data=request.POST)
        if form.is_valid():
            # Proses penyimpanan komentar
            form.save()
            messages.success(request, 'Komentar berhasil diposting!')
            return redirect('comments:index')  # Ganti dengan URL sukses sesuai kebutuhan
        else:
            messages.error(request, 'Ada kesalahan saat mengirim komentar.')
    else:
        form = CustomCommentForm(request=request)
    return render(request, 'comments/post_comment.html', {'form': form})