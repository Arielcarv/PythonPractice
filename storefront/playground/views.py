from django.shortcuts import render


def calculate():
    x = 1
    y = 2
    return x, y


def say(request):
    x, y = calculate()

    context = {
        "name": "Ariel",
        "x": x,
        "y": y,
    }
    return render(request, "hello.html", context)


def home(request):
    return render(request, "home.html")
