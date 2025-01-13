from django.db import models

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
    )
    task_type = models.CharField(
        max_length=10,
        choices=[
            ("unique", "Уникализация"),
            ("check", "Проверка"),
        ],
        verbose_name="Тип задачи",
    )
    bucket_name = models.CharField(
        max_length=255,
        verbose_name="Имя бакета",
    )
    copy_count = models.PositiveIntegerField(
        verbose_name="Количество уникализированных копий",
    )
    delete_extra_files = models.BooleanField(
        default=False,
        verbose_name="Удалить лишние файлы в папках бакета",
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ("in_progress", "В процессе"),
            ("error", "Ошибка"),
            ("completed", "Выполнена"),
        ],
        default="in_progress",
        verbose_name="Статус",
    )
    messages = models.JSONField(
        default=list,
        verbose_name="Сообщения",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"
