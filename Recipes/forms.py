from django import forms
from .models import Author, Recipe


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=240)
    last_name = forms.CharField(max_length=240)
    bio = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)

class AddAuthorForm(forms.ModelForm):

    class Meta:
        model = Author
        fields = ('name', 'bio', 'user')
    

class AddRecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ('title', 'author', 'description', 'required_time', 'instructions') 
    
    def non_staff(self):
        self.fields['author'].editable = False   
        return self.fields