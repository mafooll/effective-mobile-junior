from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView, View)

from .forms import AdForm, ProposalForm
from .models import Ad, ExchangeProposal
from .services.proposals import (accept_proposal, create_exchange_proposal,
                                 reject_proposal)
from .services.queries import (get_available_ads_for_exchange,
                               get_blocked_ad_ids, get_filter_options,
                               get_filtered_ads, get_filtered_proposals)


class AdListView(LoginRequiredMixin, ListView):
    model = Ad
    template_name = "ads/ad_list.html"
    context_object_name = "ads"
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        category = self.request.GET.get("category", "")
        condition = self.request.GET.get("condition", "")
        return get_filtered_ads(query, category, condition).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories, conditions = get_filter_options()
        blocked_ad_ids = get_blocked_ad_ids()

        context.update(
            {
                "categories": categories,
                "conditions": conditions,
                "query": self.request.GET.get("q", ""),
                "selected_category": self.request.GET.get("category", ""),
                "selected_condition": self.request.GET.get("condition", ""),
                "blocked_ad_ids": blocked_ad_ids,
            }
        )
        return context


class AdDetailView(LoginRequiredMixin, DetailView):
    model = Ad
    template_name = "ads/ad_detail.html"
    context_object_name = "ad"


class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = "ads/ad_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("ads:ad_detail", kwargs={"pk": self.object.pk})


class AdEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = "ads/ad_form.html"
    context_object_name = "ad"

    def test_func(self):
        ad = self.get_object()
        return ad.user == self.request.user

    def handle_no_permission(self):
        return redirect("ads:ad_detail", pk=self.get_object().pk)

    def get_success_url(self):
        return reverse_lazy("ads:ad_detail", kwargs={"pk": self.object.pk})


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = "ads/ad_confirm_delete.html"
    success_url = reverse_lazy("ads:ad_list")

    def test_func(self):
        ad = self.get_object()
        return ad.user == self.request.user

    def handle_no_permission(self):
        return redirect("ads:ad_detail", pk=self.get_object().pk)


class ProposalListView(LoginRequiredMixin, ListView):
    model = ExchangeProposal
    template_name = "ads/proposal_list.html"
    context_object_name = "proposals"

    def get_queryset(self):
        sender = self.request.GET.get("sender")
        receiver = self.request.GET.get("receiver")
        status = self.request.GET.get("status")
        return get_filtered_proposals(
            sender=sender, receiver=receiver, status=status
        ).order_by("-created_at")


class ProposalCreateView(LoginRequiredMixin, CreateView):
    model = ExchangeProposal
    form_class = ProposalForm
    template_name = "ads/proposal_form.html"
    success_url = reverse_lazy("ads:proposal_list")

    def get_form(self, form_class=None):
        form_class = form_class or self.get_form_class()
        available_ads = get_available_ads_for_exchange()
        return form_class(
            available_ads_queryset=available_ads, **self.get_form_kwargs()
        )

    def form_valid(self, form):
        ad_sender = form.cleaned_data["ad_sender"]
        ad_receiver = form.cleaned_data["ad_receiver"]
        try:
            create_exchange_proposal(ad_sender, ad_receiver)
        except (PermissionDenied, ValueError) as e:
            form.add_error(None, str(e))
            return self.form_invalid(form)
        messages.success(self.request, "Proposal created successfully.")
        return redirect(self.success_url)


class ProposalAcceptView(LoginRequiredMixin, View):

    def post(self, request, pk):
        proposal = get_object_or_404(ExchangeProposal, pk=pk)
        try:
            accept_proposal(proposal, request.user)
            messages.success(request, "Proposal accepted.")
        except (PermissionDenied, ValueError) as e:
            messages.error(request, str(e))
        return redirect("ads:proposal_list")

    def get(self, request, *args, **kwargs):
        return redirect("ads:proposal_list")


class ProposalRejectView(LoginRequiredMixin, View):

    def post(self, request, pk):
        proposal = get_object_or_404(ExchangeProposal, pk=pk)
        try:
            reject_proposal(proposal, request.user)
            messages.success(request, "Proposal rejected.")
        except (PermissionDenied, ValueError) as e:
            messages.error(request, str(e))
        return redirect("ads:proposal_list")

    def get(self, request, *args, **kwargs):
        return redirect("ads:proposal_list")
