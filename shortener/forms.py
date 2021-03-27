from django import forms


class ShortenerForm(forms.Form):
    full_url = forms.URLField(label='Original URL')
    user_url = forms.CharField(
        label='Your shorter',
        required=False,
        max_length=12
    )
