from django.db.models import Q

from ...ads.models import Ad, ExchangeProposal


def get_available_ads_for_exchange():
    accepted_proposals = ExchangeProposal.objects.filter(status="accepted")
    blocked_ad_ids = set(
        accepted_proposals.values_list("ad_sender_id", flat=True)
    ).union(accepted_proposals.values_list("ad_receiver_id", flat=True))

    return Ad.objects.exclude(id__in=blocked_ad_ids).order_by("-created_at")


def get_filtered_ads(query="", category="", condition=""):
    ads = Ad.objects.all().order_by("-created_at")
    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        ads = ads.filter(category=category)
    if condition:
        ads = ads.filter(condition=condition)
    return ads


def get_filter_options():
    categories = Ad.objects.values_list("category", flat=True).distinct()
    conditions = [choice[0] for choice in Ad.CONDITION_CHOICES]
    return categories, conditions


def get_blocked_ad_ids():
    accepted_proposals = ExchangeProposal.objects.filter(status="accepted")
    return set(accepted_proposals.values_list("ad_sender_id", flat=True)).union(
        accepted_proposals.values_list("ad_receiver_id", flat=True)
    )


def get_filtered_proposals(sender=None, receiver=None, status=None):
    qs = ExchangeProposal.objects.all().order_by("-created_at")
    if sender:
        qs = qs.filter(ad_sender__user_id=sender)
    if receiver:
        qs = qs.filter(ad_receiver__user_id=receiver)
    if status:
        qs = qs.filter(status=status)
    return qs
