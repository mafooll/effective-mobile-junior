from django.urls import path

from .views import (AdCreateView, AdDeleteView, AdDetailView, AdEditView,
                    AdListView, ProposalAcceptView, ProposalCreateView,
                    ProposalListView, ProposalRejectView)

app_name = "ads"

urlpatterns = [
    path("", AdListView.as_view(), name="ad_list"),
    path("ad/<int:pk>/", AdDetailView.as_view(), name="ad_detail"),
    path("ad/create/", AdCreateView.as_view(), name="ad_create"),
    path("ad/<int:pk>/edit/", AdEditView.as_view(), name="ad_edit"),
    path("ad/<int:pk>/delete/", AdDeleteView.as_view(), name="ad_delete"),
    path("proposals/", ProposalListView.as_view(), name="proposal_list"),
    path("proposals/create/", ProposalCreateView.as_view(), name="proposal_create"),
    path(
        "proposals/<int:pk>/accept/",
        ProposalAcceptView.as_view(),
        name="proposal_accept",
    ),
    path(
        "proposals/<int:pk>/reject/",
        ProposalRejectView.as_view(),
        name="proposal_reject",
    ),
]
