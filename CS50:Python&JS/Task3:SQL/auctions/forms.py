from .models import Auction, Comment, Bet, WatchList
from django.forms import ModelForm, TextInput, Textarea, NumberInput, CheckboxInput


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = ['name', 'categorie', 'description', 'photo']

        widgets = {
            "name": TextInput(attrs={
                'class': 'auction-form',
                'placeholder': 'List name'
            }),
            "categorie": TextInput(attrs={
                'class': 'auction-form',
                'placeholder': 'List category'
            }),
            "description": Textarea(attrs={
                'class': 'auction-form',
                'placeholder': 'List description'
            })
        }
class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

        widgets = {
            "comment": Textarea(attrs={
                'class': 'comment-form',
                'placeholder': 'Enter your comment here...'
            })

        }
class NewBetForm(ModelForm):
    class Meta:
        model = Bet
        fields = ['current_bet']

        widgets = {
            "current_bet": NumberInput(attrs={
                'class': 'bet-form',
                'placeholder': 'Your new bet value'
            })
        }

class BetForm(ModelForm):
    class Meta:
        model = Bet
        fields = ['current_bet']

        widgets = {
            "current_bet": NumberInput(attrs={
                'class': 'bet-form',
                'placeholder': 'List price'
            })
        }

class WatchListForm(ModelForm):
    class Meta:
        model = WatchList
        fields = ['follow']

        widgets = {
            "follow": CheckboxInput(attrs={
                'class': 'watchlist-form'
            })
        }
