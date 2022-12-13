from django import forms
from book.models import Book


class BookForm(forms.ModelForm):

    class Meta:
        model = Book
        exclude = []



# class BookForm(forms.Form):
#    title        = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control'}))
#    author       = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
#    cover        = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
#    editor       = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))  
#    collection   = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))     
#    gender       = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))  