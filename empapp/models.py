from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db.models.fields import NullBooleanField, TextField
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.

class Company(models.Model):
    coName = models.CharField(primary_key='true',max_length=50,unique='true')
    coEmail = models.EmailField()
    coLogo = CloudinaryField("image",null=True)
    coAddress = models.CharField(max_length=100)

    def __str__(self):
        return self.coName

class Education(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='education',null=True)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, null=True)
    institution = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100, blank=True)
    completion_year = models.IntegerField(blank=True)

    def __str__(self):
        return f"{self.degree} from {self.institution}, {self.completion_year}"

class Role(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='role',null=True)
    name = models.CharField(max_length=50, null=False)
    level = models.CharField(max_length=50, blank=True)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    salary = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0, blank=True)
    def __str__(self):
        return self.name

class Department(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='depart',null=True)
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee',null=True)
    image = CloudinaryField("image", blank=True ,null=True)
    first_name = models.CharField(primary_key='true',max_length=50,unique='true')
    middle_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=15, null=True,choices=GENDER_CHOICES)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    marital_status = models.CharField(max_length=20, null=True, choices=MARITAL_STATUS_CHOICES)
    address = models.CharField(max_length=100, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(blank=True, null=True)
    
    def save_employee(self):
        self.save()
    
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='attendance',null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    check_in_time = models.DateTimeField()
    check_out_time = models.DateTimeField()
    date = models.DateField()

    def __str__(self):
        return f"{self.employee.first_name} - {self.date}"

class Leave(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='leave',null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.employee.first_name} - {self.start_date} to {self.end_date}"

class Performance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfomance',null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    feedback = models.TextField()

    def __str__(self):
        return f"{self.employee.name} - {self.year}"

class Payroll(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='payroll',null=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.PositiveIntegerField()
    year = models.PositiveIntegerField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def __str__(self):
        return f"{self.employee.first_name} - {self.month}/{self.year}"

class Training(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='training',null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=100)
    duration = models.PositiveIntegerField()
    employees = models.ManyToManyField(Employee)

    def __str__(self):
        return self.title

class Document(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='document',null=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    file = models.FileField(upload_to='documents/')
    date_uploaded = models.DateField()
    employees = models.ManyToManyField(Employee)

    def __str__(self):
        return self.title
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',null=True)
    profile_photo = CloudinaryField("image",null=True)
    about = models.TextField(max_length=300)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE,null=True)
    birthdate = models.DateField(null=True)
    nationality = models.CharField(max_length=100,null=True)
    emergency_contact_name = models.CharField(max_length=100, null=True)
    emergency_contact_relationship = models.CharField(max_length=100,null=True)
    emergency_contact_phone = models.CharField(max_length=20,null=True)
    emergency_contact_email = models.EmailField(null=True)
    interests = models.CharField(max_length=255, blank=True)

    updated_on = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return f'{self.user.username} profile'

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
