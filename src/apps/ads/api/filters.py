import django_filters
from django.db import models

from ..models import Ad, ExchangeProposal


class AdFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(method="filter_search")

    class Meta:
        model = Ad
        fields = ["category", "condition"]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(title__icontains=value) | models.Q(description__icontains=value)
        )


class ProposalFilter(django_filters.FilterSet):
    class Meta:
        model = ExchangeProposal
        fields = ["ad_sender__user", "ad_receiver__user", "status"]
