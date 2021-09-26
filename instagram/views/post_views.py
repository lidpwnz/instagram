from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

from instagram.forms.post_form import PostForm
from instagram.models import Post, Like


class PostCreate(generic.CreateView):
    model = Post
    template_name = 'posts/post.html'
    form_class = PostForm

    def get_initial(self):
        return {'owner': self.request.user}

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})


class AddLikeToPostView(generic.View):
    success_url = None

    def get_post(self):
        return Post.objects.get(pk=self.kwargs.get('post_pk'))

    def get(self, request, *args, **kwargs):
        self.post(request, *args, **kwargs)
        return redirect('profile', pk=self.request.user.pk)

    def set_like(self):
        post = self.get_post()
        user_who_likes = self.request.user
        post_users_pk_list = post.users_who_like_it.values_list('liked_user', flat=True)

        if user_who_likes.pk not in post_users_pk_list:
            Like.objects.create(post=post, liked_user=user_who_likes)
            post.likes_count += 1

        else:
            post.users_who_like_it.get(liked_user=user_who_likes).delete()
            post.likes_count -= 1

        return post

    def post(self, request, *args, **kwargs):
        post = self.set_like()
        post.save()
        return redirect('post_detail', pk=post.pk)


class PostDetail(generic.DetailView):
    model = Post
    template_name = 'posts/detail.html'
    context_object_name = 'post'


class AddCommentToPostView(generic.View):
    pass
