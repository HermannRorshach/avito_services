from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.ServicesView.as_view(), name='services'),
    path('cabinet', views.CabinetView.as_view(), name='cabinet'),
    path('services', views.ServicesView.as_view(), name='services'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
    path('faq/', views.FAQView.as_view(), name='faq'),


]
