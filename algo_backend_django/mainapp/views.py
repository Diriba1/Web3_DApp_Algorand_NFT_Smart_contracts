from django.shortcuts import render

# Create your views here.
from .models import Account


def index(request):
    """Display all the created standalone accounts."""

    accounts = Account.objects.order_by("-created")
    context = {"accounts": accounts}
    return render(request, "mainapp/index.html", context)
