from django.urls import path

from . import views

app_name = 'image_generator'

urlpatterns = [
    path('tasks', views.TasksListView.as_view(), name='tasks'),
    path('create_task', views.TaskCreateView.as_view(), name='create_task'),
    path('task/<int:pk>/', views.TaskView.as_view(), name='task'),
    path('write_links_to_table/', views.ImageLinksWriterView.as_view(), name="write_links")


    # path('advert_list/', views.AdvertListView.as_view(), name='advert_list'),
    # path('adverts/<int:pk>/', views.AdvertDetailView.as_view(), name='advert_detail'),
]
