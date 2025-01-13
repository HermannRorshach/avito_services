import os

import boto3
from botocore.config import Config
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import CreateView
from dotenv import load_dotenv

from .forms import TaskForm
from .models import Task

# Загружаем переменные окружения
load_dotenv()
YANDEX_ACCESS_KEY = os.getenv('YANDEX_CLOUD_ACCESS_KEY_ID')
YANDEX_SECRET_KEY = os.getenv('YANDEX_CLOUD_SECRET_ACCESS_KEY')
# YANDEX_BUCKET_NAME = 'adverts-bucket'
YANDEX_ENDPOINT_URL = 'https://storage.yandexcloud.net'

# Настройка клиента S3 для Яндекс Object Storage
s3_client = boto3.client(
    service_name='s3',
    endpoint_url=YANDEX_ENDPOINT_URL,
    aws_access_key_id=YANDEX_ACCESS_KEY,
    aws_secret_access_key=YANDEX_SECRET_KEY,
    config=Config(signature_version='s3v4')
)


@method_decorator(login_required, name='dispatch')
class TasksListView(ListView):
    model = Task
    template_name = 'unique_ad_image_generator/tasks.html'
    context_object_name = 'tasks'

@method_decorator(login_required, name='dispatch')
class TaskCreateView(CreateView):
    model = Task
    template_name = 'add_item.html'
    form_class = TaskForm
    success_url = reverse_lazy('image_generator:tasks')
    extra_context = {'role': 'задачу'}

    def form_valid(self, form):
        task = form.save()
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class TaskView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'unique_ad_image_generator/task.html'
    context_object_name = 'task'

    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs.get('pk'), user=self.request.user)
