from django import forms
class ContactForm(forms.Form):#widget for ading html classes customizing django widgets
    fullname=forms.CharField(widget=forms.TextInput(
                              attrs={
                                  "class":"form-control",
                                  "placeholder":"Your Full Name"}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"Your Email"}))
    content=forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","placeholder":"your content"}))

    def clean_email(self):
        '''for validation of email'''
        email=self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError("Email has to be gmail.com")
        return email

