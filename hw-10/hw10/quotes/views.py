from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse

from .forms import AuthorForm, QuoteForm
from .models import Quote, Author, Tag


def get_quotes(request, page=1):
    quotes = Quote.objects.all().order_by("-created_at")

    par_page = 10

    paginator = Paginator(quotes, par_page)

    return render(
        request,
        "quotes/quotes.html",
        context={
            "quotes": paginator.page(page),
        },
    )


def get_author(request, fullname):
    try:
        author = Author.objects.get(fullname=fullname)
    except Author.DoesNotExist:
        return HttpResponse(f"<h1>Author with name - {fullname} does not exist</h1>")

    return render(
        request,
        "quotes/author.html",
        context={
            "author": author,
        },
    )


@login_required
def create_author(request):
    if request.method == "POST":
        form = AuthorForm(request.POST)

        if form.is_valid():
            author = form.save(commit=False)
            author.save()

            return redirect(to="quotes:author", fullname=form.cleaned_data["fullname"])
        else:
            return render(
                request,
                "quotes/create_author.html",
                context={
                    "form": form,
                },
            )

    return render(
        request,
        "quotes/create_author.html",
        context={
            "form": AuthorForm(),
        },
    )


@login_required
def create_quote(request):
    tags = Tag.objects.all()
    authors = Author.objects.all()

    if request.method == "POST":
        form = QuoteForm(request.POST)

        if form.is_valid():
            a = Author.objects.get(id=request.POST["author"])
            q = Quote.objects.create(
                quote=request.POST["quote"],
                author=a,
            )

            for tag in request.POST.getlist("tags"):
                q.tags.add(tag)

            return redirect(to="quotes:main")
        else:
            return render(
                request,
                "quotes/create_quote.html",
                context={
                    "form": form,
                    "tags": tags,
                    "authors": authors,
                },
            )

    return render(
        request,
        "quotes/create_quote.html",
        context={
            "form": QuoteForm(),
            "tags": tags,
            "authors": authors,
        },
    )
