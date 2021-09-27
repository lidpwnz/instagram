from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View

from instagram.forms.post_form import PostForm, CommentForm
from instagram.models import Post, Like


class PostCreate(generic.CreateView):
    model = Post
    template_name = 'posts/post.html'
    form_class = PostForm

    def get_initial(self):
        return {'owner': self.request.user}

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.request.user.profile.pk})


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'posts/post_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_pk'
    form = CommentForm

    def get_context_data(self, **kwargs):
        kwargs['form'] = self.form()
        return super().get_context_data(**kwargs)

class PostDeleteView(View):
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['post_pk'])
        post_owner_pk = post.owner.profile.pk
        post.delete()
        return redirect('profile', pk=post_owner_pk)


class FeedView(generic.ListView):
    template_name = 'posts/feed.html'
    model = Post
    context_object_name = 'posts'
    ordering = ['-created_at']
    form = CommentForm

    def get_queryset(self):
        queryset = []
        for i in self.request.user.profile.subscribes.all():
            if self.request.user.profile == i:
                continue
            for j in i.user.posts.all():
                queryset.append(j)
        return queryset

    def get_context_data(self, **kwargs):
        kwargs['form'] = self.form()
        return super().get_context_data(**kwargs)


class AddLikeToPostView(generic.View):
    success_url = None
    like_class = Like
    user_who_likes = None
    _post = None

    def dispatch(self, request, *args, **kwargs):
        self.user_who_likes = self.request.user
        self._post = self.get_post()
        return super(AddLikeToPostView, self).dispatch(request, *args, **kwargs)

    def get_post(self):
        return Post.objects.get(pk=self.kwargs.get('post_pk'))

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def add_like(self):
        Like.objects.create(post=self._post, liked_user=self.user_who_likes)

    def remove_like(self):
        self._post.users_who_like_it.get(liked_user=self.user_who_likes).delete()

    def get_success_url(self):
        return self.request.META['HTTP_REFERER']

    def set_like(self):
        user_who_likes = self.request.user
        post_users_pk_list = self._post.users_who_like_it.values_list('liked_user', flat=True)

        if user_who_likes.pk not in post_users_pk_list:
            self.add_like()
        else:
            self.remove_like()

        self._post.save()

    def post(self, request, *args, **kwargs):
        self.set_like()
        return redirect(self.get_success_url())


class AddCommentToPostView(View):

    def get_success_url(self):
        return self.request.META['HTTP_REFERER']

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        post = get_object_or_404(Post, pk=self.kwargs.get('post_pk'))
        if form.is_valid():
            post.comments.create(
                text=request.POST.get('text'),
                post=post,
                comment_author=post.owner
            )
        return redirect(self.get_success_url())
