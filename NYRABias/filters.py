import django_filters.rest_framework as filter
from .models import Race

class RaceFilter(filter.FilterSet):
    date = filter.DateFromToRangeFilter(field_name="date")
    track = filter.CharFilter(field_name= "track", lookup_expr='iexact')
    surface = filter.CharFilter(field_name="surface", lookup_expr='iexact')
    distance = filter.CharFilter(field_name="distance", lookup_expr='iexact')
    condition = filter.CharFilter(field_name="condition", lookup_expr='iexact')
    fieldSize_lt = filter.NumberFilter(field_name="fieldSize", lookup_expr="lt")
    fieldSize_gt = filter.NumberFilter(field_name="fieldSize", lookup_expr="gt")
    maidens = filter.BooleanFilter(field_name="maidens")

    class Meta:
        model = Race
        fields = ['date', 'track', 'surface', 'distance', 'condition', 'fieldSize', 'maidens']