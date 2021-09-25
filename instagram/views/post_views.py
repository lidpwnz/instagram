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
    def get_post(self):
        return Post.objects.get(pk=self.kwargs.get('post_pk'))

    def post(self, request, *args, **kwargs):
        user_who_likes = request.user
        post = self.get_post()
        if user_who_likes in post.users_who_like_it.all():
            post.users_who_like_it.get(liked_user=user_who_likes).delete()
            post.likes_count -= 1
        else:
            post.users_who_like_it.add(user_who_likes)
            post.likes_count += 1

        post.save()
        return redirect(self.request.get_full_path)


class AddCommentToPostView(generic.View):
    pass
