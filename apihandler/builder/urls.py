from django.urls import path
from builder.views.views import test
from builder.views.apihandler import fetch_news

urlpatterns = [
    path('testing', test),
    path('news', fetch_news),
]

