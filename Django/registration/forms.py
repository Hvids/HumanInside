from django import forms
from django.utils.safestring import mark_safe


class RegisterForm(forms.Form):
    fields = ["username", 'first_name', 'last_name', "age", "password1", "password2"]


class MyForm(forms.Form):
    my_field = forms.CharField(label=mark_safe('my label<br />next line'))
