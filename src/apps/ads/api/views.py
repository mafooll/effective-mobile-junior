from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from ..models import Ad, ExchangeProposal
from .filters import AdFilter, ProposalFilter
from .permissions import IsOwnerOrReadOnly, IsProposalParticipant
from .serializers import AdSerializer, ExchangeProposalSerializer


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all().order_by("-created_at")
    serializer_class = AdSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExchangeProposalViewSet(viewsets.ModelViewSet):
    queryset = ExchangeProposal.objects.all().order_by("-created_at")
    serializer_class = ExchangeProposalSerializer
    permission_classes = [IsAuthenticated, IsProposalParticipant]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProposalFilter

    def perform_create(self, serializer):
        serializer.save()
