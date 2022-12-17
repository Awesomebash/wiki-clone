from django.shortcuts import redirect, render
from django import forms

from . import util

import markdown
import random


class SearchForm(forms.Form):
    search = forms.CharField(label="Search")


class CreateForm(forms.Form):
    title = forms.CharField(label="Title:")
    markdownForm = forms.CharField(label="Markdown:", widget=forms.Textarea(attrs={
        'name': 'markdown',
        'rows': 30,
        'cols': 5
    }))

class EditForm(forms.Form):
    markdownForm = forms.CharField(label="", widget=forms.Textarea(attrs={
        'rows': 30,
        'cols': 5
    }))


def index(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            entryObject = util.get_entry(search)
            if entryObject == None:
                entries = util.list_entries()
                searchOutput = []

                for entry in entries:
                    if entry.lower().find(search.lower()) != -1:
                        searchOutput.append(entry)
                if len(searchOutput) > 0:
                    return render(request, "encyclopedia/search.html", {
                        "entries": searchOutput,
                        "title": search
                    })
                else:
                    return render(request, "encyclopedia/error.html")
            else:
                return redirect('wiki:entry', search)
        else:
            return redirect('wiki:index')
    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries()
        })


def entry(request, title):
    entryObject = util.get_entry(title)
    if entryObject == None:
        return render(request, "encyclopedia/error.html")
    else:
        entryHTML = markdown.markdown(entryObject)
        return render(request, "encyclopedia/entry.html", {
            "title": title.lower(),
            "entry": entryHTML
        })


def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if not form.is_valid():
            return redirect('wiki:index')
        createTitle = form.cleaned_data["title"]
        createMarkdown = form.cleaned_data["markdownForm"]
        if createTitle in util.list_entries():
            return render(request, "encyclopedia/error.html")
        util.save_entry(createTitle, createMarkdown)
        return redirect('wiki:entry', createTitle)
    else:
        return render(request, "encyclopedia/create.html", {
            "form": CreateForm()
        })


def rnd(request):
    return redirect('wiki:entry', random.choice(util.list_entries()))


def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if not form.is_valid():
            return redirect('wiki:index')
        createMarkdown = form.cleaned_data["markdownForm"]
        util.save_entry(title, createMarkdown)
        return redirect('wiki:entry', title)
    else:
        form = EditForm(initial={'markdownForm': util.get_entry(title)})
        return render(request, "encyclopedia/edit.html", {
            "form": form,
            "title": title
        })
