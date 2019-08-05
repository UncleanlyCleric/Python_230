from django.urls import path
from blogging.views import list_view, detail_view, add_model

urlpatterns = [
    path('', list_view, name="blog_index"),
    path('posts/<int:post_id>/', detail_view, name="blog_detail"),
    path("create_post", add_model)
]
