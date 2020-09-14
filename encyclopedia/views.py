from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django import forms
from . import util

from markdown2 import Markdown
import random


md = Markdown()

class CreateEntryForm(forms.Form):
    entry_title = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control"}))
    entry_text = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control"}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    entry = util.get_entry(title)
    if entry is not None:
        html_data = md.convert(entry)
        return render(request, "encyclopedia/entry.html", {
        'title': title, 'html_data': html_data
        })
    else:
        raise Http404(f"404 Error - Entry [{title}] doesn't exist!")


def create(request):
    if request.method == 'POST':
        form = CreateEntryForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data['entry_title']
            entry_text = form.cleaned_data['entry_text']
            util.save_entry(title=entry_title, content=entry_text)
            return HttpResponseRedirect(reverse('entry', args=[entry_title]))
    return render(request, "encyclopedia/create.html", {
        'form': CreateEntryForm()
    })

def edit(request):
    if request.POST:
        form = CreateEntryForm(request.POST)
        if form.is_valid():
            entry_title = form.cleaned_data['entry_title']
            entry_text = form.cleaned_data['entry_text'].replace("\n", "")
            util.save_entry(title=entry_title, content=entry_text)
            return HttpResponseRedirect(reverse('entry', args=[entry_title]))
    if request.GET:
        title = request.GET['title']
        entry = util.get_entry(title)
        form = CreateEntryForm(initial={'entry_title': title, 'entry_text': entry})
        return render(request, "encyclopedia/edit.html", { 'form':form, 'title': title })
    


def search(request):
    entries = [x.lower() for x in util.list_entries()]
    entry_list = []
    q = None
    if request.method == 'POST':
        q = request.POST['q']
        if q == "":
            q = None
        else:
            if q.lower() in entries:
                return HttpResponseRedirect(reverse('entry', args=[q]))
            else:
                for e in util.list_entries():
                    if q.lower() in e.lower():
                        entry_list.append(e)

    return render(request, "encyclopedia/search_results.html", {
        'q': q,
        'entries': entry_list
    })


def random_entry(request):
    entry = random.choice(util.list_entries())
    if entry is not None:
        return HttpResponseRedirect(reverse('entry', args=[entry]))
    return render(request, "encyclopedia/error.html")

