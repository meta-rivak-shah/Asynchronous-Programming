from django import forms
from Dashboard.models import PostModel


class PostForm(forms.Form):
    post_text = PostModel.validations.post_text(required=True, label='post text', widget=forms.Textarea(
        attrs={"placeholder": "Enter Something"}))
    post_type = PostModel.validations.post_type(required=True)

    class Meta:
        model = PostModel
        fields = ('post_text', 'post_type', 'post_img')

