from django.shortcuts import HttpResponse


def homepage(request):  # noqa: ANN001, ARG001, D103, ANN201
    return HttpResponse("<h1>Hello World from Homepage!</h1>")


