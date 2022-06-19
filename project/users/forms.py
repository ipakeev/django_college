from django import forms


class EmailMessageForm(forms.Form):
    email = forms.EmailField(label="Ваш e-mail", required=True)
    message = forms.CharField(label="Сообщение", required=True, widget=forms.Textarea)


class LoginForm(forms.Form):
    email = forms.EmailField(label="E-mail", required=True)
    password = forms.CharField(label="Пароль", required=True, widget=forms.PasswordInput)
