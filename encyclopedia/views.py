from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from . import util

from markdown2 import Markdown
import random
md = Markdown()


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
        raise Http404(f"404 Error - Entry ({title}) doesn't exist!")


def random_entry(request):
    entry = random.choice(util.list_entries())
    if entry is not None:
        return HttpResponseRedirect(reverse('entry', args=[entry]))
    return render(request, "encyclopedia/error.html")

