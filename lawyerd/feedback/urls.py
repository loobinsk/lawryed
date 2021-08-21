from django.urls import path
from .views import feedback_view

app_name = "feedbacks"
urlpatterns = [
    path("feedback", view=feedback_view, name="feedback"),
]
