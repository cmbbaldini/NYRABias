from django_filters import rest_framework as filters
from .models import Race

class RaceFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter(field_name="date")
    track = filters.CharFilter(field_name= "track", lookup_expr='iexact')
    surface = filters.CharFilter(field_name="surface", lookup_expr='iexact')
    distance = filters.CharFilter(field_name="distance", lookup_expr='iexact')
    condition = filters.CharFilter(field_name="condition", lookup_expr='iexact')
    condition_neg = filters.CharFilter(field_name="condition", exclude=True)
    fieldSize_lt = filters.NumberFilter(field_name="fieldSize", lookup_expr="lt")
    fieldSize_gt = filters.NumberFilter(field_name="fieldSize", lookup_expr="gt")
    maidens = filters.BooleanFilter(field_name="maidens")

    class Meta:
        model = Race
        fields = ['date', 'track', 'surface', 'distance', 'condition', 'fieldSize', 'maidens']