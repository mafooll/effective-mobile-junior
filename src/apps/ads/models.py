from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ad(models.Model):
    CONDITION_CHOICES = [
        ("new", "New"),
        ("used", "Used"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ads")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    category = models.CharField(max_length=100)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.user})"


class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("rejected", "Rejected"),
    ]

    ad_sender = models.ForeignKey(
        Ad, on_delete=models.CASCADE, related_name="sent_proposals"
    )
    ad_receiver = models.ForeignKey(
        Ad, on_delete=models.CASCADE, related_name="received_proposals"
    )
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Proposal {self.id}: {self.ad_sender} -> {self.ad_receiver} [{self.status}]"
