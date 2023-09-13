from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=63, label='Nom d’utilisateur')
    password = forms.CharField(max_length=63, widget=forms.PasswordInput, label='Mot de passe')


class RegisterForm(forms.ModelForm):
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        labels = {'username' : 'nom d\'utilisateur', 'email' : 'adresse email', 'password' : 'mot de passe', 'password2' : 'confirmer le mot de passe'}

    def clean(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2 :
            raise forms.ValidationError("Les deux mots de passe ne correspondent pas")

class MailForm(forms.Form) :
    subject = forms.CharField(max_length=255, label='Sujet')
    message = forms.CharField(widget=forms.Textarea, label='Contenu')
    to = forms.CharField(max_length=255, label='Destinataire')
    cc = forms.CharField(max_length=255, label='cc', required=False)
    bcc = forms.CharField(max_length=255, label='bcc', required=False)
    piece_jointe = forms.FileField(label='Pièce jointe', required=False)