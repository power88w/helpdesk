from django import forms
from django.utils.translation import ugettext_lazy as _

class CheckoutForm(forms.Form):
    payment_method_nonce = forms.CharField(
        max_length=1000,
        widget=forms.widgets.HiddenInput,
        required=False,
    )

    def clean(self):
        self.cleaned_data = super(CheckoutForm, self).clean()
        # Braintree nonce is missing
        if not self.cleaned_data.get('payment_method_nonce'):
            raise forms.ValidationError(_(
                'We couldn\'t verify your payment. Please try again.'))
        return self.cleaned_data