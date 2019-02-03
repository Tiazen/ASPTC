from django import forms


class registForm(forms.Form):
    login = forms.CharField(label='login', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    passw = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), max_length=64)
    name = forms.CharField(label='name', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(label='surname', max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    degrees = (('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'))
    degree = forms.MultipleChoiceField(choices=degrees, widget=forms.Select(attrs={'class': 'form-control'}))
    letters = (('А', 'A'), ('Б', 'Б'), ('В', 'В'), ('Г', 'Г'), ('Д', 'Д'), ('Е', 'E'), ('ДОП', 'ДОП'))
    letter = forms.MultipleChoiceField(choices=letters, widget=forms.Select(attrs={'class': 'form-control'}))
    #widget=forms.Select()

class loginForm(forms.Form):
    login = forms.CharField(label='login', max_length=50, widget=forms.TextInput(attrs={'id': 'login', 'class': 'form-control', 'placeholder': 'Логин'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'id': 'password', 'class': 'form-control', 'placeholder': 'Пароль'}), max_length=64)


class addtaskForm(forms.Form):
    taskName = forms.CharField(max_length=100)
    inputs = forms.CharField(max_length=300)
    rights = forms.CharField(max_length=300)
    textdescription = forms.CharField(widget=forms.Textarea(attrs={'rows': '10', 'cols': '55'}), max_length=600)


class uploadForm(forms.Form):
    file = forms.FileField()
