from django import forms
from .models import Task


from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['bucket_name', 'copy_count', 'delete_extra_files', 'task_type']



    def clean_copy_count(self):
        copy_count = self.cleaned_data.get('copy_count')
        if copy_count <= 0:
            raise forms.ValidationError('Количество копий должно быть целым положительным числом.')
        return copy_count
