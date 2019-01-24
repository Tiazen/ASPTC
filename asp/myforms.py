from django import forms


class registForm(forms.Form):
    login = forms.CharField(label='login', max_length=50)
    passw = forms.CharField(widget=forms.PasswordInput(), max_length=64)
    name = forms.CharField(label='name', max_length=50)
    surname = forms.CharField(label='surname', max_length=50)
    degrees = (('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),('11','11'))
    degree = forms.MultipleChoiceField(choices=degrees, widget=forms.Select())
    letters = (('А', 'A'), ('Б', 'Б'), ('В', 'В'), ('Г', 'Г'), ('Д', 'Д'), ('Е', 'E'), ('ДОП', 'ДОП'))
    letter = forms.MultipleChoiceField(choices=letters, widget=forms.Select())


class loginForm(forms.Form):
    login = forms.CharField(label='login', max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(), max_length=64)


class addtaskForm(forms.Form):
    taskName = forms.CharField(max_length=100)
    inputs = forms.CharField(max_length=300)
    rights = forms.CharField(max_length=300)
    textdescription = forms.CharField(widget=forms.Textarea(attrs={'rows': '10', 'cols': '55'}), max_length=600)

class uploadForm(forms.Form):
    file = forms.FileField()
