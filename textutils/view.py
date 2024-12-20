from os import remove
from urllib import request
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def analyze(request):
    djtext = request.POST.get('text', 'default')
    removepunc = request.POST.get('removepunc', 'off')
    fullcaps = request.POST.get('fullcaps', 'off')
    newlineremove = request.POST.get('newlineremove', 'off')
    extraspaceremove = request.POST.get('extraspaceremove', 'off')
    charcount = request.POST.get('charcount', 'off')

    if removepunc == "on":
        analyzed = ""
        punctuations = '''!()-[]};{:'"\,<>./?@#$%^&*_~'''
        for char in djtext:
            if char not in punctuations:
                analyzed += char
        params = {"purpose": "Removed Punctuations", "analyzed_text": analyzed}
        djtext = analyzed

    if fullcaps == "on":
        analyzed = ""
        for char in djtext:
            analyzed += char.upper()
        params = {"purpose": "ALL UPPERCASE", "analyzed_text": analyzed}
        djtext = analyzed
    
    if newlineremove == "on":
        analyzed = ""
        for char in djtext:
            if char != "\n" and char != "\r":
                analyzed += char
        params = {"purpose": "Removed new line", "analyzed_text": analyzed}
        djtext = analyzed
    
    if extraspaceremove == "on":
        analyzed = ""
        for index, char in enumerate(djtext):
            if not (djtext[index] == " " and djtext[index+1]==" "):
                analyzed = analyzed + char
        params = {"purpose": "Removed extra space", "analyzed_text": analyzed}
        djtext = analyzed

    elif charcount == "on":
        count = {}
        for char in djtext.lower():
            if char.isalnum():
                if char not in count:
                    count[char] = 1
                else:
                    count[char] += 1
        analyzed = f"The count of the characters you typed is:{str(count)}"
        params = {"purpose": "Characters Count", "analyzed_text": analyzed}

    elif removepunc!="on" and extraspaceremove!="on" and newlineremove!="on" and charcount!="on" and fullcaps!="on":
        return HttpResponse("Error")

    return render(request, "analyze.html", params)