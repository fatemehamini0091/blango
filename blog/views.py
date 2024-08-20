from django.shortcuts import render, get_object_or_404, redirect
# from django.views.decorators.vary import vary_on_headers 
from django.utils import timezone
# from django.views.decorators.cache import cache_page
from blog.models import Post
from blog.forms import CommentForm
import logging

logger = logging.getLogger(__name__)


def get_ip(request):
  from django.http import HttpResponse
  return HttpResponse(request.META['REMOTE_ADDR'])

#in this case we want to cache the response for 300 seconds (5 minutes)
# @cache_page(300)
# @vary_on_headers("Cookie")
def index(request):
    # posts = (
    #   Post.objects.filter(published_at__lte=timezone.now())
    #   .select_related("author")
    #   .only("title", "content","summary","author","published_at","slug")
    # )
    # posts = (
    #   Post.objects.filter(published_at__lte=timezone.now())
    #   .select_related("author")
    #   .defer("created_at", "modified_at")
    # )
    posts = Post.objects.filter(published_at__lte=timezone.now()).select_related("author")
    logger.debug("Got %d posts", len(posts))
    return render(request, "blog/index.html", {"posts": posts})


def post_detail(request, slug):
  post = get_object_or_404(Post, slug=slug)

  if request.user.is_active:
    if request.method == "POST":
      comment_form = CommentForm(request.POST)

      if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.content_object = post
        comment.creator = request.user
        comment.save()
        """
        perform a redirect back to the current Post 
        (this essentially just refreshes
         the page for the user so they see their new comment)
        """
        return redirect(request.path_info)
    else:
      comment_form = CommentForm() 
  else:
    comment_form = None
  return render(request, "blog/post-detail.html", 
    {"post":post, "comment_form": comment_form})