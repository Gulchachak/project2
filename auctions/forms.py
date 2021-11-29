from django.forms import ModelForm
from .models import Listing

class ListingCreateForm(ModelForm):
    class Meta:
        model = Listing
        # fields = '__all__'
        fields = ['title', 'description', 'starting_bid', 'category', 'img_url', 'date']