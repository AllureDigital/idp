from django import forms

class EmailForm(forms.Form):
    from_email = forms.EmailField(label='From', required=False, widget=forms.TextInput(attrs={'readonly': True}))
    to_email = forms.EmailField(label='To')
    cc_email = forms.EmailField(label='CC', required=False)
    bcc_email = forms.EmailField(label='BCC', required=False)
    subject = forms.CharField(label='Subject')
    body = forms.CharField(label='Body', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        user_email = kwargs.pop('user_email', None)
        super(EmailForm, self).__init__(*args, **kwargs)
        if user_email:
            self.fields['from_email'].initial = user_email


class ReplyEmailForm(forms.Form):
    from_email = forms.EmailField(label='From', required=False, widget=forms.TextInput(attrs={'readonly': True}))
    to_email = forms.EmailField(label='To')
    cc_email = forms.EmailField(label='CC', required=False)
    bcc_email = forms.EmailField(label='BCC', required=False)
    subject = forms.CharField(label='Subject')
    body = forms.CharField(label='Body', widget=forms.Textarea)