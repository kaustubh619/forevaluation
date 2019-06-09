from django import forms
from .models import Input


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class InputsForm(forms.ModelForm):
    valuation_date = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))

    class Meta:
        model = Input
        fields = ['organization', 'project', 'valuation_date', 'statutory_corporate_tax_rate', 'statutory_mat_rate', 'post_tax_wacc', 'long_term_growth_rate', 'company_specific_risk', 'contingent_liability', 'total_shares_outstanding']


class Registration(forms.Form):
    username = forms.CharField(max_length=10)
    password = forms.CharField(widget=forms.PasswordInput)

