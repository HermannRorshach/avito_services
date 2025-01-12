from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.ServicesView.as_view(), name='services'),
    path('cabinet', views.CabinetView.as_view(), name='cabinet'),

]
