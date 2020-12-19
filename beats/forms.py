from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from .validators import validate_Audiofile_extension, validate_Imgfile_extension

DUPLICATE_EMAIL = _("This email address is already in use. "
                    "Please supply a different email address.")

class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(max_length=255, required=True)
    check = forms.BooleanField(required=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(DUPLICATE_EMAIL)
        return self.cleaned_data['email']
        

class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a Beat', required=True, validators=[validate_Audiofile_extension])

    imgfile = forms.FileField(label='Select an Image', required=True, validators=[validate_Imgfile_extension])

    strokeColour = forms.CharField(required=True, disabled=False,widget=forms.Textarea(attrs={"style": "resize: none", 'rows':1, 'cols':1}))

    fillColour = forms.CharField(required=True, disabled=False,widget=forms.Textarea(attrs={"style": "resize: none", 'rows':1, 'cols':1}))

class ChangeEmail(forms.Form):
    new_email1 = forms.EmailField(label=u'Type new Email')
    new_email2 = forms.EmailField(label=u'Type Email again') 
    

    error_messages = {
        'email_mismatch': _("The two email addresses fields didn't match."),
        'not_changed': _("The email address is the same as the one already defined."),
    }
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(ChangeEmail, self).__init__(*args, **kwargs)

    def clean_new_email1(self):
        old_email = self.user.email
        new_email1 = self.cleaned_data.get('new_email1')
        if new_email1 and old_email:
            if new_email1 == old_email:
                raise forms.ValidationError(
                    self.error_messages['not_changed'],
                    code='not_changed',
                )
            if User.objects.filter(email__iexact=self.cleaned_data['new_email1']):
                raise forms.ValidationError(DUPLICATE_EMAIL)
        return new_email1

    def clean_new_email2(self):
        new_email1 = self.cleaned_data.get('new_email1')
        new_email2 = self.cleaned_data.get('new_email2')
        if new_email1 and new_email2:
            if new_email1 != new_email2:
                print("yo")
                raise forms.ValidationError(
                    self.error_messages['email_mismatch'],
                    code='email_mismatch',
                )
        return new_email2

    def save(self, commit=True):
        email = self.cleaned_data["new_email1"]
        self.user.email = email
        if commit:
            self.user.save()
        return self.user
        