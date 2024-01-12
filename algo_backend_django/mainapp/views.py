from django.shortcuts import render, redirect
from .helpers import add_standalone_account
from django.contrib import messages
from .models import Account
from .forms import TransferFundsForm

from .helpers import (
    INITIAL_FUNDS,
    add_transaction,
    cli_passphrase_for_account,
    initial_funds_sender,
)

def index(request):
    """Display all the created standalone accounts."""

    accounts = Account.objects.order_by("-created")
    context = {"accounts": accounts}
    return render(request, "mainapp/index.html", context)

def create_standalone(request):
    """Create standalone account."""
    private_key, address = add_standalone_account()
    account = Account.objects.create(address=address, private_key=private_key)
    context = {"account": (address, account.passphrase)}
    return render(request, "mainapp/create_standalone.html", context)

def initial_funds(request, receiver):
    """Add initial funds to provided standalone receiver account."""
    sender = initial_funds_sender()
    if sender is None:
        message = "Initial funds weren't transferred!"
        messages.add_message(request, messages.ERROR, message)
    else:
        add_transaction(
            sender,
            receiver,
            cli_passphrase_for_account(sender),
            INITIAL_FUNDS,
            "Initial funds",
        )
    return redirect("standalone-account", receiver)


from .forms import TransferFundsForm


def transfer_funds(request, sender):
    """Transfer funds from the provided sender account to the receiver from the form."""
    if request.method == "POST":

        if "retrieve_passphrase" in request.POST:
            sender_instance = Account.instance_from_address(sender)
            request.POST = request.POST.copy()
            request.POST.update({"passphrase": sender_instance.passphrase})
            form = TransferFundsForm(request.POST)
        else:

            form = TransferFundsForm(request.POST)

            if form.is_valid():

                error_field, error_description = add_transaction(
                    sender,
                    form.cleaned_data["receiver"],
                    form.cleaned_data["passphrase"],
                    form.cleaned_data["amount"],
                    form.cleaned_data["note"],
                )
                if error_field == "":
                    message = "Amount of {} microAlgos has been successfully transferred to account {}".format(
                        form.cleaned_data["amount"], form.cleaned_data["receiver"]
                    )
                    messages.add_message(request, messages.SUCCESS, message)
                    return redirect("standalone-account", sender)

                form.add_error(error_field, error_description)

    else:

        form = TransferFundsForm()

    context = {"form": form, "sender": sender}

    return render(request, "mainapp/transfer_funds.html", context)
