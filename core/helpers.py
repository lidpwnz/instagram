def get_widget_attrs(**kwargs):
    context = {'class': 'form-control mb-3'}
    if kwargs:
        context.update(kwargs)
    return context


