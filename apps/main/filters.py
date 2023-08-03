import django_filters
from main import models


class NoteFilter(django_filters.FilterSet):
    category__title = django_filters.CharFilter(field_name='status', lookup_expr='exact')

    class Meta:
        model = models.ToDoNote
        fields = ['status']
