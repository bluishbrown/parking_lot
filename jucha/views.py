from django.shortcuts import render, redirect
from .models import Post
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from .forms import CommentForm
from django.shortcuts import get_object_or_404

class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['exit_at']

    template_name = "jucha/post_update_form.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:# and request.user == self.get_object().author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['exit_at']
    template_name = "jucha/post_create_form.html"
    def form_valid(self, form):
        ##자동으로 클에이트에 넣을값
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            # form.instance.title = user가클릭한 타이틀번호(칸번호pk)
            # form.instance.ejung = 이 칸과 옆칸이 찻으면 True
            return super(PostCreate, self), self.form_valid(form)
        else:
            return redirect('/jucha/')


# Create your views here.
class PostList(ListView):
    model = Post
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()
        #context['remain_time'] = self.object.exit_at
        return context



#
# def detail(request, title):
#     post = Post.objects.get(title=title)
#     return render(
#         request,
#         'jucha/post_detail.html',
#         {'post': post,}
#     )

class PostDetail(DetailView):
    model = Post
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        #context['remain_time'] = self.object.exit_at
        context['comment_form'] = CommentForm
        return context

def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.author = request.user
                comment.save()
                return redirect(comment.get_absolute_url())
        else:
                return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied

def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authnticatec and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied
