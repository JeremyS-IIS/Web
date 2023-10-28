from django.shortcuts import render


def index(request, *args, **kwargs):  # noqa: ANN201, D103, ANN001, ARG001, ANN002, ANN003
    return render(request, "frontend/index.html")


def portal(request, *args, **kwargs): # noqa: ANN201, D103, ANN001, ARG001, ANN002, ANN003
    return render(request, "frontend/portal.html")
