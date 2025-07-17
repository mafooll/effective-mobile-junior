from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Q

from ...ads.models import ExchangeProposal


def create_exchange_proposal(ad_sender, ad_receiver):
    if ad_sender.user == ad_receiver.user:
        raise PermissionDenied("Cannot propose exchange to your own ad.")

    ad_ids = [ad_sender.id, ad_receiver.id]
    already_exchanged = ExchangeProposal.objects.filter(
        Q(status="accepted")
        & (Q(ad_sender_id__in=ad_ids) | Q(ad_receiver_id__in=ad_ids))
    ).exists()

    if already_exchanged:
        raise ValueError("One of the ads is already involved in an accepted exchange.")

    return ExchangeProposal.objects.create(
        ad_sender=ad_sender, ad_receiver=ad_receiver, status="pending"
    )


def accept_proposal(proposal, user):
    if proposal.ad_receiver.user != user:
        raise PermissionDenied("You are not allowed to accept this proposal.")

    if proposal.status != "pending":
        raise ValueError("Proposal is already processed.")

    ad_ids = [proposal.ad_sender.id, proposal.ad_receiver.id]
    conflict = (
        ExchangeProposal.objects.filter(
            Q(status="accepted")
            & (Q(ad_sender_id__in=ad_ids) | Q(ad_receiver_id__in=ad_ids))
        )
        .exclude(pk=proposal.pk)
        .exists()
    )

    if conflict:
        raise ValueError(
            "One of the ads is already involved in another accepted exchange."
        )

    with transaction.atomic():
        proposal.status = "accepted"
        proposal.save()

        ExchangeProposal.objects.filter(
            Q(status="pending")
            & (Q(ad_sender_id__in=ad_ids) | Q(ad_receiver_id__in=ad_ids))
        ).exclude(pk=proposal.pk).update(status="rejected")


def reject_proposal(proposal, user):
    if proposal.ad_receiver.user != user:
        raise PermissionDenied("You are not allowed to reject this proposal.")

    if proposal.status != "pending":
        raise ValueError("Proposal is already processed.")

    proposal.status = "rejected"
    proposal.save()
