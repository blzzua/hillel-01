from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse


from feedback.forms import FeedbackForm
from feedback.models import Feedback


# Create your views here
@login_required(login_url='/admin/login/?next=/feedback/')
def feedback_index(request):
    if request.method == 'POST':
        form = FeedbackForm(data=request.POST)
        if form.is_valid():
            form.save(fill_name=request.user.username)
            return redirect(reverse('feedback_list'))
    else:
        form = FeedbackForm()
    return render(request, 'feedback_index.html', context={'form': form})


def feedback_list(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'feedback_list.html', context={'feedbacks': feedbacks})
