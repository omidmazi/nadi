from xml.etree.ElementTree import Comment
from django import forms 
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        exclude=["post"]
        labels={
            "user_name": "نام شما",
            "user_email":"ایمیل",
            "text":"نظر شما",
        }
