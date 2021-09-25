from django.urls import reverse_lazy
from django.views import generic

from instagram.forms.post_form import PostForm
from instagram.models import Post


class PostCreate(generic.CreateView):
    model = Post
    template_name = 'posts/post.html'
    form_class = PostForm

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(PostCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile', kwargs={'pk': self.object.pk})
