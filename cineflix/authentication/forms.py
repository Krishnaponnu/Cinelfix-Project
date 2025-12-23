from django import forms

from .models import Profile

from re import fullmatch


class LoginForm(forms.Form):

    email  = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','required':'required'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control','required':'required'}))

class SignUpForm(forms.ModelForm):

    class Meta:

        model = Profile

        fields = ['first_name','last_name','email']

        widgets = {

            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'})

        }

    def clean(self):

        cleaned_data = super().clean()

        email = cleaned_data.get('email')

        if Profile.objects.filter(username=email).exists():

            self.add_error('email','This email Already Registered')



class AddphoneForm(forms.Form):

    phone = forms.CharField(max_length=14,widget=forms.TextInput(attrs={'class':'form-control'}))

    def clean(self):

        cleaned_data =  super().clean()

        phone = cleaned_data.get('phone')

        pattern = '(\\+?91)?\\s?[6-9]\\d{9}'

        valid = fullmatch(pattern,phone)

        if not valid:

            self.add_error('phone','Invalid Phone Number')

        if Profile.objects.filter(phone=phone).exists():

            self.add_error('phone','This Phone Number Already Registered')

class OTPForm(forms.Form):

    otp = forms.CharField(max_length=4,widget=forms.TextInput(attrs={'class':'form-control'}))



class ChangePasswordForm(forms.Form):

    new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    def clean(self):
        
        cleaned_data = super().clean()

        new_password = cleaned_data.get('new_password')

        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:

            self.add_error('confirm_password','passwords does not match')