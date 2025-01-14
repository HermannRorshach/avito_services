from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DeleteView, DetailView, ListView
from django.views.generic.edit import CreateView

from .forms import TaskForm
from .models import Task
from .utils import update_excel_with_image_urls


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



class ImageLinksWriterView(View):
    def get(self, request, *args, **kwargs):
        # Отображаем форму для ввода данных (если нужно)
        return render(request, 'unique_ad_image_generator/write_links_to_table.html')

    def post(self, request, *args, **kwargs):
        # Получаем данные из формы
        bucket_name = request.POST.get('bucket_name')
        file_obj = request.FILES['excel_file']
        sheet_name = request.POST.get('sheet_name')

        # Генерируем файл с помощью функции update_excel_with_image_urls
        output = update_excel_with_image_urls(bucket_name, file_obj, sheet_name)


        # Формируем ответ для скачивания файла
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename="{file_obj.name.rsplit(".", 1)[0]}_with_links.xlsx"'
        return response
