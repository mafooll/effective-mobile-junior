from django import forms

from .models import Ad, ExchangeProposal


class AdForm(forms.ModelForm):
    image_url = forms.URLField(required=False, assume_scheme="https")

    class Meta:
        model = Ad
        fields = ["title", "description", "image_url", "category", "condition"]


class ProposalForm(forms.ModelForm):
    class Meta:
        model = ExchangeProposal
        fields = ["ad_sender", "ad_receiver", "comment"]

    def __init__(self, *args, available_ads_queryset=None, **kwargs):
        super().__init__(*args, **kwargs)
        if available_ads_queryset is not None:
            self.fields["ad_sender"].queryset = available_ads_queryset
            self.fields["ad_receiver"].queryset = available_ads_queryset
