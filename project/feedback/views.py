from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import render, redirect
from django.urls import reverse

from django.views.generic import TemplateView, RedirectView
from django.views.generic.edit import FormMixin, TemplateResponseMixin
from django.views import View

from feedback.forms import FeedbackForm
from feedback.models import Feedback


# Create your views here
class FeedbackView(View):
    @method_decorator(login_required(login_url='/admin/login/?next=/feedback/'))
    def post(self, request):
        form = FeedbackForm(data=request.POST)
        if form.is_valid():
            form.save(fill_name=request.user.username)
            return redirect(reverse('feedback_list'))

    def get(self, request):  # feedback_index
        form = FeedbackForm()
        return render(request, 'feedback_index.html', context={'form': form})

class FeedbackListView(View):
    def get(self, request):
        feedbacks = Feedback.objects.all()
        return render(request, 'feedback_list.html', context={'feedbacks': feedbacks})
