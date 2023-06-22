
from django.http import HttpResponseRedirect
from .models import *
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required

from .forms import *


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


@login_required(login_url="/accounts/login/")
def profile(request):
    current_user = request.user
    profile = Profile.objects.filter(user_id=current_user.id).first()
    
    employee = Employee.objects.filter(user_id=current_user.id)
    documents = Document.objects.filter(user_id=current_user.id)
    training = Training.objects.filter(user_id=current_user.id)
    payroll = Payroll.objects.filter(user_id=current_user.id)
    leave = Leave.objects.filter(user_id=current_user.id)
    attendance = Attendance.objects.filter(user_id=current_user.id)
    education = Education.objects.filter(user_id=current_user.id)
    depart = Department.objects.filter(user_id=current_user.id)
    return render(request, "profile.html", {"profile": profile, ' employee':  employee,
                                             'documents': documents,"payroll": payroll, "training": training,
                                             "leave": leave, "attendance": attendance, "education": education,
                                             'depart': depart})


@login_required(login_url='/accounts/login/')
def update_profile(request,id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user_id = user)
    form = UpdateProfileForm(instance=profile)
    if request.method == "POST":
            form = UpdateProfileForm(request.POST,request.FILES,instance=profile)
            if form.is_valid():  
                
                profile = form.save(commit=False)
                profile.save()
                return redirect('profile') 
            
    return render(request, 'update_profile.html', {"form":form})

