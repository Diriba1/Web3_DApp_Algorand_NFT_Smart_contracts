from algosdk.constants import address_len, mnemonic_len, note_max_length
from algosdk.encoding import is_valid_address
from django import forms
from django.core.exceptions import ValidationError
from django.forms.fields import CharField


class TransferFundsForm(forms.Form):
    """Django form for transferring microAlgos between accounts."""

    passphrase = forms.CharField(required=False)
    receiver = forms.CharField(max_length=address_len)
    amount = forms.IntegerField(min_value=1)
    note = forms.CharField(max_length=note_max_length, required=False)

    def clean_passphrase(self):
        """Example validation for the passphrase field."""
        data = self.cleaned_data["passphrase"]
        words = data.split(" ")
        if len(words) != mnemonic_len:
            raise ValidationError(
                "Passphrase must have exactly %s words!" % (mnemonic_len,)
            )
        return data

    def clean_receiver(self):
        """Example validation for the receiver field."""
        data = self.cleaned_data["receiver"]
        if not is_valid_address(data):
            raise ValidationError("Provided value is not a valid Algorand address!")
        return data