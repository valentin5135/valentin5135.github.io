from django.shortcuts import render, redirect
from django import forms
from . import util
from django.core.files.storage import default_storage
from .models import Articles, Search
from .forms import ArticlesForm, SearchForm
import markdown2
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "search_form": SearchForm(),
        "entries": util.list_entries()
    })

def page(request, title):
    for entry in util.list_entries():
        if title == entry:
            return render(request, "encyclopedia/page.html", {
                "html_text": markdown2.markdown(util.get_entry(title)),
                "search_form": SearchForm(),
                "title": title
            })

    return render(request, 'encyclopedia/notfound.html',
        {"search_form": SearchForm()}, status=404)


def create(request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            # check if there is an article with this title
            for entry in util.list_entries():
                if form.cleaned_data["title"] == entry:
                    return render(request, "encyclopedia/create.html", {
                        "search_form": SearchForm(),
                        "error": 'Page with this title already exist!'
                    })
            util.save_entry(form.cleaned_data["title"],
            form.cleaned_data["content"])
            return redirect('wiki:page', title=form.cleaned_data["title"])
        else:
            error = 'Error: Invalid request!'
    form = ArticlesForm()

    return render(request, "encyclopedia/create.html", {
        "search_form": SearchForm(),
        "form": form,
        "error": error
    })

def randpage(request):
    rand_entry = random.choice(util.list_entries());
    return render(request, "encyclopedia/page.html", {
        "search_form": SearchForm(),
        "html_text": markdown2.markdown(util.get_entry(rand_entry)),
        "title": rand_entry
    })

def edit(request, title):
    error = ''

    form = ArticlesForm(initial={
        'title': title,
        'content': util.get_entry(title)
    })
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            util.save_entry(form.cleaned_data["title"],
            form.cleaned_data["content"])
            return redirect('wiki:page', title=form.cleaned_data["title"])
        else:
            error = 'Error: Invalid request!'

    return render(request, "encyclopedia/edit.html", {
        "search_form": SearchForm(),
        "form": form,
        "error": error
    })

def search(request):
    error = ''
    search_entries = []
    uniq_entries = []
    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            search_request = search_form.cleaned_data["search_page"]
        else:
            error = 'Error: Invalid request!'
    # if the search text matches the title of the article
    if default_storage.exists(f"entries/{search_request}.md"):
        return render(request, "encyclopedia/page.html", {
            "search_form": SearchForm(),
            "html_text": markdown2.markdown(util.get_entry(search_request)),
            "title": search_request
        })
    else:
    # if the search text is contained in the title of the article
        entries = util.list_entries()
        for entry in entries:
            step = len(search_request)
            for i in range(len(entry) - step + 1):
                if search_request == entry[i : i + step]:
                    search_entries.append(entry)
        # repeatability check
        for entry in search_entries:
            if entry not in uniq_entries:
                uniq_entries.append(entry)
        if uniq_entries == []:
            error = 'There are no pages that contain this text'
        return render(request, "encyclopedia/index.html", {
            "search_form": SearchForm(),
            "search_request": search_request,
            "entries": uniq_entries,
            "error": error
        })

    return render(request, "encyclopedia/index.html", {
        "search_form": SearchForm(),
        "search_request": search_request,
        "entries": entries,
        "error": error
    })

def delete(request, title):
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)

    return render(request, "encyclopedia/index.html", {
        "search_form": SearchForm(),
        "entries": util.list_entries()
    })
