from django.forms import ModelForm, Textarea
from blogging.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["title", "text"]

        widgets = {
            "title": Textarea(attrs={"cols": 60, "rows":1}),
            "text": Textarea(attrs={"cols": 60, "rows":20})
        }
