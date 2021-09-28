from django.shortcuts import redirect


def get_widget_attrs(**kwargs):
    context = {'class': 'form-control mb-3'}
    if kwargs:
        context.update(kwargs)
    return context


def redirect_to_feed(request):
    return redirect('feed')


