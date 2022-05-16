from django import forms

from .models import *


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'


class TransferForm(forms.Form):
    bid = forms.CharField(label='Book ID', max_length=10)
    sid = forms.CharField(label='Student ID', max_length=10)


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['username']
class RatingForm(forms.ModelForm):
    class Meta:
        # model = Reviews
        # exclude=['student','book']
        pass