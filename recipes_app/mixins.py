from django.urls import reverse_lazy
from django.views.generic import CreateView


class GetSuccessUrlMixin(CreateView):
    url_name = None

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy(self.url_name)
