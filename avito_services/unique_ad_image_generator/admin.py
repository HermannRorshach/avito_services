from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Task._meta.fields]

#     search_fields = ('name', 'email')
#     list_filter = ('date', 'registration_date')


# @admin.register(Feedback)
# class FeedbackAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'text', 'date')
#     search_fields = ('name', 'email', 'text')
#     list_filter = ('date',)
