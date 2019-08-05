from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from blogging.models import Post
from django import forms
from django.utils import timezone
from blogging.forms import PostForm


def add_model(request):
    # If nobody is logged in, redirect to login screen
    if str(request.user) == "AnonymousUser":
        return redirect("http://localhost:8000/accounts/login/")

    elif request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)

            # Automatically makes the logged in user the author
            model_instance.author = request.user

            # Gets the current date/time for published date
            model_instance.published_date = timezone.now()

            model_instance.save()
            return redirect("/")

    else:
        form = PostForm()

        return render(request, "blogging/create_post.html", {"form": form})


def stub_view(request, *args, **kwargs):
    body = "Stub View\n\n"

    if args:
        body += "Args:\n"
        body += "\n".join(["\t%s" % a for a in args])

    if kwargs:
        body += "Kwargs:\n"
        body += "\n".join(["\t%s: %s" % i for i in kwargs.items()])

    return HttpResponse(body, content_type="text/plain")


def list_view(request):
    published = Post.objects.exclude(published_date__exact=None)
    posts = published.order_by("-published_date")
    context = {"posts": posts}
    return render(request, "blogging/list.html", context)


def detail_view(request, post_id):
    published = Post.objects.exclude(published_date__exact=None)
    try:
        post = published.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404
    context = {"post": post}
    return render(request, "blogging/detail.html", context)
