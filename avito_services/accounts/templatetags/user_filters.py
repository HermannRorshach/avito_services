from django import template
from django.forms.widgets import CheckboxInput

register = template.Library()


@register.filter
def addclass(field, css):
    if isinstance(field.field.widget, CheckboxInput):
        return field  # Возвращаем поле без добавления класса
    return field.as_widget(attrs={'class': css})
