from django import forms
from .models import Employee
from .models import Company

# This is for employee
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"

#this is for company
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"

class EditEmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"


