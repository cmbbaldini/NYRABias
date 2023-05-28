import django_filters
from .models import Race

class RaceFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name="date")
    track = django_filters.CharFilter(field_name= "track", lookup_expr='iexact')
    surface = django_filters.CharFilter(field_name="surface", lookup_expr='iexact')
    distance = django_filters.CharFilter(field_name="surface", lookup_expr='iexact')
    condition = django_filters.CharFilter(field_name="condition", lookup_expr='iexact')
    fieldSize_lt = django_filters.NumberFilter(field_name="fieldSize", lookup_expr="lt")
    fieldSize_gt = django_filters.NumberFilter(field_name="fieldSize", lookup_expr="gt")
    maidens = django_filters.BooleanFilter(field_name="maidens")

    class Meta:
        model = Race
        fields = ['date', 'track', 'surface', 'distance', 'condition', 'fieldSize', 'maidens']