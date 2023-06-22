from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.

class Company(models.Model):
    coName = models.CharField(primary_key='true',max_length=50,unique='true')
    coEmail = models.EmailField()
    coLogo = CloudinaryField("image",null=True)
    coAddress = models.CharField(max_length=100)

    def __str__(self):
        return self.coName

class Education(models.Model):
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    completion_year = models.IntegerField()

    def __str__(self):
        return f"{self.degree} from {self.institution}, {self.completion_year}"

class Role(models.Model):
    name = models.CharField(max_length=50, null=False)
    level = models.CharField(max_length=50, blank=True)
    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=50, null=False)
    location = models.CharField(max_length=180)
    description = models.TextField()

    def __str__(self):
        return self.name

class Employee(models.Model):
    MARITAL_STATUS_CHOICES = [
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widowed', 'Widowed'),
        ('other', 'Other'),
        ('not_specified', 'Prefer Not to Say'),
    ]
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
        ('not_specified', 'Prefer Not to Say'),
    ]
    image = CloudinaryField("image", blank=True ,null=True)
    first_name = models.CharField(primary_key='true',max_length=50,unique='true')
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=15, null=True,choices=GENDER_CHOICES)
    education = models.ManyToManyField(Education)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    depart = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    salary = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    marital_status = models.CharField(max_length=20, null=True, choices=MARITAL_STATUS_CHOICES)
    address = models.CharField(max_length=100, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Check if the user is an admin before saving
        if self.user.is_admin:
            super().save(*args, **kwargs)
        else:
            raise PermissionError("Only admins can edit the salary field.")

    def create_employee(self):
        self.save()

    def update_employee(self):
        self.save()

    def delete_employee(self):
        self.delete()

    @classmethod
    def filter_by_id(cls, id):
        employee = Employee.objects.filter(user=id).first()
        return employee

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField()
    date = models.DateField()

    def __str__(self):
        return f"{self.employee.first_name} - {self.date}"

class Leave(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.employee.first_name} - {self.start_date} to {self.end_date}"

# class Performance(models.Model):
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
#     year = models.PositiveIntegerField()
#     rating = models.DecimalField(max_digits=3, decimal_places=2)
#     feedback = models.TextField()

#     def __str__(self):
#         return f"{self.employee.name} - {self.year}"

class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.employee.first_name} - {self.month}/{self.year}"

class Training(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    employees = models.ManyToManyField(Employee)

    def __str__(self):
        return self.title

class Document(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='documents/')
    date_uploaded = models.DateField()
    employees = models.ManyToManyField(Employee)

    def __str__(self):
        return self.title