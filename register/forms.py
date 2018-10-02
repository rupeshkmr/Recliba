from django import forms
class RegisterUpdateForm(forms.ModelForm):#widget for ading html classes customizing django widgets
    return_date=forms.DateField(widget=forms.DateInput(attrs={"class":"form-control","placeholder":"Your Email"}))
    # status=forms.BooleanField(widget=forms.BooleanInput(
    #                           attrs={
    #                               "class":"form-control",
    #                               "placeholder":"Your Full Name"}))
class IssueForm(forms.Form):
    roll=forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Roll No"}))

class ReturnForm(forms.Form):
    book=forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control","placeholder":"Book No"}))
