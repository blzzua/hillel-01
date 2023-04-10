from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator

from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import ListView
from django.views import View

from feedback.forms import FeedbackForm
from feedback.models import Feedback


# Create your views here
class FeedbackView(View):
    @method_decorator(login_required(login_url=reverse_lazy('accounts_login')))
    def post(self, request):
        form = FeedbackForm(data=request.POST)
        if form.is_valid():
            form.save(fill_name=request.user.username)
            return redirect(reverse('feedback_list'))
        else:
            return render(request, 'feedback/feedback_index.html', context={'form': form})

    def get(self, request):  # feedback_index
        form = FeedbackForm()
        return render(request, 'feedback/feedback_index.html', context={'form': form})


class FeedbackListView(ListView):
    model = Feedback
    paginate_by = 5
    paginator = Paginator
    template_name = 'feedback/list.html'

    def get_queryset(self):
        return super().get_queryset().order_by('-created_at')
