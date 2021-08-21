from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from feedback.models import Feedback


class FeedbackView(View):
    def post(self, request, *args, **kwargs):
        Feedback.objects.create(name=request.POST['name'], email=request.POST['email'], phone=request.POST['phone'])
        return redirect(reverse('home'))


feedback_view = FeedbackView.as_view()
