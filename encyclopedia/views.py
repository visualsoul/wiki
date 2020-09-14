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
        raise Http404(f"404 Error - Entry [{title}] doesn't exist!")


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

