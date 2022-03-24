from .models import Articles, Search
from django.forms import ModelForm, TextInput, Textarea


class ArticlesForm(ModelForm):
    class Meta:
        model = Articles
        fields = ['title', 'content']

        widgets = {
            "title": TextInput(attrs={
                'class': 'create-page',
                'placeholder': 'Article title'
            }),
            "content": Textarea(attrs={
                'class': 'create-page',
                'placeholder': 'Article text'
                })

        }
class SearchForm(ModelForm):
    class Meta:
        model = Search
        fields = ['search_page']

        widgets = {
            "search_page": TextInput(attrs={
                'class': 'search-page',
                'placeholder': 'Search Encyclopedia'
            })

        }
