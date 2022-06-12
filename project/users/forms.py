from django import forms


class EmailMessageForm(forms.Form):
    email = forms.EmailField(label="Ваш e-mail", required=True)
    message = forms.CharField(label="Сообщение", required=True, widget=forms.Textarea)
