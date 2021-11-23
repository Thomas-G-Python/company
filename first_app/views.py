from django.shortcuts import render, reverse
from django.http import HttpResponse, HttpResponseRedirect
import datetime
# jede View MUSS ein http-Response Objekt zurückgeben


def first_view(request):
    return HttpResponse("Hello World!")


def second_view(request):
    """Analyze request object"""
    print("alle Rezepte-Objekte auf der Konsole")
    # print(dir(request))
    print("Scheme: ", request.scheme)
    print("Body: ", request.body)
    print("Path: ", request.path)
    print("Method: ", request.method)
    print("GET:", request.GET)
    print("Header: ", request.headers)
    print("build absolute path: ", request.build_absolute_uri())
    return HttpResponse("Request Objekt")


def third_view(request):
    """das Response Objekt"""
    response = HttpResponse()
    response['age'] = 120
    now = datetime.datetime.now().strftime('%H:%M %d.%m.%y')
    html = f"<html><body>It is now {now}</body></html>"
    response.content = html
    return response


def fourth_view(request):
    """Umleitung"""
    return HttpResponseRedirect(reverse("first_app:second_view"))
    # return HttpResponseRedirect("/firstapp/second") # schlecht.
    # return HttpResponseRedirect("https://google.com")
