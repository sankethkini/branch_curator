from django import forms
from .models import *

class MemberSignup(forms.ModelForm):
    class Meta:
        model=Member
        fields=('mid','name','contact','email','dept','password')

        widgets={
            'name':forms.TextInput(attrs={'class':'form-control','placeholder':'your name'}),
            'mid':forms.TextInput(attrs={'class':'form-control','placeholder':'your usn/teacher id'}),
            'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'your email'}),
            'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'password'}),
            'contact':forms.NumberInput(attrs={'class':'form-control','placeholder':'mobile number'}),
            'dept':forms.TextInput(attrs={'class':'form-control','placeholder':'department (e.g ise)'}),
        } 

class Login(forms.Form):
    id=forms.CharField(max_length=10,label='id')
    password=forms.CharField(max_length=20,label='password',widget=forms.PasswordInput)
    id.widget.attrs['class']='form-control'
    password.widget.attrs['class']='form-control'

class CreateProject(forms.Form):
    name=forms.CharField(max_length=20,label='name')
    time=forms.IntegerField(label='time')
    starttime=forms.DateField(label='start',widget=forms.SelectDateWidget)
    projshortdesc=forms.CharField(label='desc')
    field=forms.CharField(label='field')
    number_of_people=forms.IntegerField(label='people')
    techstack=forms.CharField(label='techstack')
    name.widget.attrs['class']='form-control'
    time.widget.attrs['class']='form-control' 
    starttime.widget.attrs['class']='form-control'
    field.widget.attrs['class']='form-control'
    number_of_people.widget.attrs['class']='form-control'
    projshortdesc.widget.attrs['class']='form-control'
    time.widget.attrs['placeholder']='Ex. 30 days'
    techstack.widget.attrs['class']='form-control'

class CreateBlog(forms.Form):
    title=forms.CharField(max_length=20,label='title')
    body=forms.CharField(widget=forms.Textarea,label='body')

    title.widget.attrs['class']='form-control'
    body.widget.attrs['class']='form-control'