
from django.http import HttpResponseRedirect
from .models import *
from django.shortcuts import render,redirect
from .forms import CompanyForm,EmployeeForm,EditEmployeeForm


# To retrieve Company details
def index(request):
    companies = Company.objects.all()
    return render(request, "index.html", {'companies':companies})

def edit(request, coName):
    company = Company.objects.get(coName=coName)
    return render(request, "edit.html", {'company':company})

# To Update Company
def update(request, coName):
    company = Company.objects.get(coName=coName)
    form = CompanyForm(instance=company)
    if request.method == "POST":
        form = CompanyForm(request.POST,request.FILES, instance=company)
        if form.is_valid():
            company =  form.save(commit=False)
            company.save()
        return redirect("/")
    return render(request, "edit.html", {'form':form})

# To Delete Company details
def delete(request, coName):
    company = Company.objects.get(coName=coName)
    company.delete()
    return redirect("/")


# To show employee details
def employees(request):
    employees = Employee.objects.all()
    return render(request, "employees.html", {'employees':employees})

def emp(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST, request.FILES)
        if form.is_valid():
            employee = form.save(commit=False)
            
            employee.save()
        return HttpResponseRedirect('/employees')
    else:
        form = EmployeeForm()

    return render(request, "addemp.html", {'form':form})



# To delete employee details
def deleteEmp(request, first_name):
    employee = Employee.objects.get(first_name=first_name)
    employee.delete()
    return redirect("/employees")

# To edit employee details
def editemp(request, first_name):
    employee = Employee.objects.get(first_name=first_name)
    return render(request, "editemployee.html", {'employee':employee})

# To update employee details
def updateEmp(request, first_name):
    employee = Employee.objects.get(first_name=first_name)
    form = EditEmployeeForm(instance= employee)
    if request.method == "POST":
        form = EditEmployeeForm(request.POST,request.FILES, instance=employee)
        if form.is_valid():
            employee =  form.save(commit=False)
            employee.save()
        return redirect("/employees")
    return render(request, "editemployee.html", {'form': form})

