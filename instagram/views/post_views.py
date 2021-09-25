from django.urls import reverse_lazy
from django.views import generic

from instagram.forms.post_form import PostForm
from instagram.models import Post


class PostCreate(generic.CreateView):
    model = Post
    template_name = 'posts/post.html'
    form_class = PostForm

    def get_initial(self):
        return {'owner': self.request.user}

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})
