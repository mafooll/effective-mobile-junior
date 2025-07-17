import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from apps.ads.models import Ad, ExchangeProposal


@pytest.mark.django_db
def test_ad_list_view_authenticated(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser", password="testpass"
    )
    client.login(username="testuser", password="testpass")
    response = client.get(reverse("ads:ad_list"))
    assert response.status_code == 200
    assert "ads" in response.context


@pytest.mark.django_db
def test_ad_create_view(client, django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser", password="testpass"
    )
    client.login(username="testuser", password="testpass")
    response = client.post(
        reverse("ads:ad_create"),
        data={
            "title": "New Ad",
            "description": "Test description",
            "category": "electronics",
            "condition": "used",
        },
    )
    assert response.status_code == 302  # redirect after success
    assert Ad.objects.filter(title="New Ad").exists()


@pytest.mark.django_db
def test_proposal_create_view(client, django_user_model):
    user1 = django_user_model.objects.create_user(username="user1", password="pass")
    user2 = django_user_model.objects.create_user(username="user2", password="pass")
    ad1 = Ad.objects.create(
        user=user1, title="Ad1", description="Desc", category="books", condition="new"
    )
    ad2 = Ad.objects.create(
        user=user2, title="Ad2", description="Desc", category="books", condition="new"
    )

    client.login(username="user1", password="pass")
    url = reverse("ads:proposal_create")
    response = client.post(url, data={"ad_sender": ad1.id, "ad_receiver": ad2.id})

    assert response.status_code == 302
    assert ExchangeProposal.objects.count() == 1


@pytest.mark.django_db
def test_proposal_accept_view(client, django_user_model):
    sender = django_user_model.objects.create_user(username="sender", password="pass")
    receiver = django_user_model.objects.create_user(
        username="receiver", password="pass"
    )
    ad1 = Ad.objects.create(
        user=sender, title="Ad1", description="", category="books", condition="new"
    )
    ad2 = Ad.objects.create(
        user=receiver, title="Ad2", description="", category="books", condition="new"
    )
    proposal = ExchangeProposal.objects.create(
        ad_sender=ad1, ad_receiver=ad2, status="pending"
    )

    client.login(username="receiver", password="pass")
    url = reverse("ads:proposal_accept", kwargs={"pk": proposal.pk})
    response = client.post(url)
    proposal.refresh_from_db()

    assert response.status_code == 302
    assert proposal.status == "accepted"


@pytest.mark.django_db
def test_proposal_reject_view(client, django_user_model):
    sender = django_user_model.objects.create_user(username="sender", password="pass")
    receiver = django_user_model.objects.create_user(
        username="receiver", password="pass"
    )
    ad1 = Ad.objects.create(
        user=sender, title="Ad1", description="", category="books", condition="new"
    )
    ad2 = Ad.objects.create(
        user=receiver, title="Ad2", description="", category="books", condition="new"
    )
    proposal = ExchangeProposal.objects.create(
        ad_sender=ad1, ad_receiver=ad2, status="pending"
    )

    client.login(username="receiver", password="pass")
    url = reverse("ads:proposal_reject", kwargs={"pk": proposal.pk})
    response = client.post(url)
    proposal.refresh_from_db()

    assert response.status_code == 302
    assert proposal.status == "rejected"
