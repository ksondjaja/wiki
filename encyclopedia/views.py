from django.shortcuts import render
from django import forms
from django.core.files.storage import default_storage
from django.http import HttpResponse
from django.core.files.base import File, ContentFile
from django.http import HttpResponse
import markdown2
import random
import copy

from . import util


class NewTitleForm(forms.Form):
    newt = forms.CharField(label="New Title", strip=False)

class NewArticleForm(forms.Form):
    newa = forms.CharField(label="New Article", strip=False)

class NewSearchForm(forms.Form):
    q = forms.CharField(label="Search", strip=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, page):
    return render(request, "encyclopedia/entry.html", {
        "page" : page,
        "content" : markdown2.markdown(util.get_entry(page))
    })

def create(request):
    return render(request, "encyclopedia/create.html")

def preview(request):
    if request.method == "POST":
        newtitle = NewTitleForm(request.POST)
        newarticle = NewArticleForm(request.POST)
        if newtitle.is_valid() and newarticle.is_valid():
            newt = newtitle.cleaned_data["newt"]
            newa = newarticle.cleaned_data["newa"]
            for filename in util.list_entries():
                filename = str(filename)
                if newt.lower() == filename.lower():
                    return render(request, "encyclopedia/preview2.html", {
                        "newtitle" : newt,
                        "newarticle" : newa,
                        "newarticlemd" : markdown2.markdown(newa)
                    })
            return render(request, "encyclopedia/preview.html", {
                "newtitle" : newt,
                "newarticle" : newa,
                "newarticlemd" : markdown2.markdown(newa)
            })
    return HttpResponse(status=403)

def save(request):
    if request.method == "POST":
        newtitle = NewTitleForm(request.POST)
        newarticle = NewArticleForm(request.POST)
        if newtitle.is_valid() and newarticle.is_valid():
            newt = newtitle.cleaned_data["newt"]
            newa = newarticle.cleaned_data["newa"]
            for filename in util.list_entries():
                filename = str(filename)
                if newt.lower() == filename.lower():
                    return render(request, "encyclopedia/preview2.html", {
                        "newtitle" : newt,
                        "newarticle" : newa,
                        "newarticlemd" : markdown2.markdown(newa)
                    })
            text = f"#{newt}   \n\n"+newa
            util.save_entry(newt, text)
            return render(request, "encyclopedia/saved.html", {
                "message" : "added",
                "page" : newt
            })
    return HttpResponse(status=403)

def edit(request, page):
    f = default_storage.open(f"entries/{page}.md")
    f.readline()
    f.readline()
    article = f.read().decode("utf-8")
    f.close()
    return render(request, "encyclopedia/edit.html", {
        "page" : page,
        "content" : article,
        "contentmd" : markdown2.markdown(util.get_entry(page))
    })

def prevedit(request, page):
    if request.method == "POST":
        newarticle = NewArticleForm(request.POST)
        if newarticle.is_valid():
            newa = newarticle.cleaned_data["newa"]
            return render(request, "encyclopedia/prevedit.html",{
                "page": page,
                "content": newa,
                "contentmd" : markdown2.markdown(newa)
            })
    return HttpResponse(status=403)

def saveedit(request, page):
    if request.method == "POST":
        newarticle = NewArticleForm(request.POST)
        if newarticle.is_valid():
            newa = newarticle.cleaned_data["newa"]
            text = f"#{page}   \n\n"+newa
            util.save_entry(page, text)
            return render(request, "encyclopedia/saved.html",{
                "message": "edited",
                "page": page
            })
    return HttpResponse(status=403)

def rand(request):
    r = random.choice(util.list_entries())
    return entry(request, page=r)

def search(request):
    if request.method == "POST":
        newsearch = NewSearchForm(request.POST)
        if newsearch.is_valid():
            q = newsearch.cleaned_data["q"]
            results = []
            for filename in util.list_entries():
                filename = str(filename)
                if q.lower() == filename.lower():
                    return entry(request, filename)
                elif q.lower() in filename.lower():
                    results.append(filename)
    if len(results) > 0:
        return render(request, "encyclopedia/results.html", {
            "message" : f"{len(results)} match(es) found:",
            "results" : results
        })
    else:
        return render(request, "encyclopedia/results.html", {
            "message": "No matches found"
        })
    return HttpResponse(status=403)
