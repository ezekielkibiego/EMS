
from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth.models import User
from django.db.models.fields import NullBooleanField, TextField
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils.text import slugify
import uuid
from django.utils.crypto import get_random_string

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)

    @classmethod
    def create_verification(cls, user):
        token = get_random_string(length=64)
        verification = cls.objects.create(user=user, token=token)
        return verification
    
class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    coName = models.CharField(max_length=50)  # Primary key for the company
    coEmail = models.EmailField()  # Email field for the company
    coLogo = CloudinaryField("image", null=True)  # Cloudinary image field for the company logo
    coAddress = models.CharField(max_length=100)  # Address field for the company

    def __str__(self):
        return self.coName



class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, null=False)  # Name field for role
    level = models.CharField(max_length=50, blank=True)  # Level field for role (optional)
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)  # Self-referential foreign key for manager
    salary = models.IntegerField(default=0)  # Salary field for role
    bonus = models.IntegerField(default=0, blank=True)  # Bonus field for role (optional)

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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # image = CloudinaryField("image", blank=True, null=True)  # Cloudinary image field for employee image (optional)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)    
    first_name = models.CharField( max_length=50, null=True) 
    middle_name = models.CharField(max_length=50, blank=True)  # Middle name field for employee (optional)
    last_name = models.CharField(max_length=50)  # Last name field for employee
    gender = models.CharField(max_length=15, null=True, choices=GENDER_CHOICES)  # Gender field for employee
    email = models.EmailField()  # Email field for employee
    phone = models.CharField(max_length=50)  # Phone field for employee
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True)  # Foreign key relationship with Role model for employee role
    manager = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)  # Self-referential foreign key for manager
    marital_status = models.CharField(max_length=20, null=True, choices=MARITAL_STATUS_CHOICES)  # Marital status field for employee
    address = models.CharField(max_length=100, null=True)  # Address field for employee
    start_date = models.DateField(null=True)  # Start date field for employee
    end_date = models.DateField(blank=True, null=True)  # End date field for employee (optional)

    def save_employee(self):
        self.save()

    def save(self, *args, **kwargs):
        # Generate a slug from the employee's full name when saving the model
        if not self.slug:
            full_name = f"{self.first_name} {self.last_name}"
            self.slug = slugify(full_name)

        super().save(*args, **kwargs)

    def create_employee(self):
        self.save()

    def update_employee(self):
        self.save()
        return self

    def delete_employee(self):
        self.delete()

    @classmethod
    def filter_by_id(cls, id):
        employee = Employee.objects.filter(user=id).first()
        return employee

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, null=True)  # Foreign key relationship with Employee model
    name = models.CharField(max_length=50, null=False)  # Name field for department
    location = models.CharField(max_length=180)  # Location field for department
    description = models.TextField()  # Description field for department

    def __str__(self):
        return self.name

class Education(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, null=True)  # Foreign key relationship with Employee model
    institution = models.CharField(max_length=100)  # Institution field for education
    degree = models.CharField(max_length=100)  # Degree field for education
    field_of_study = models.CharField(max_length=100, blank=True)  # Field of study for education (optional)
    completion_year = models.IntegerField(blank=True)  # Completion year for education (optional)

    def __str__(self):
        return f"{self.degree} from {self.institution}, {self.completion_year}"

class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Foreign key relationship with Employee model
    check_in_time = models.DateTimeField()  # Check-in time field for attendance
    check_out_time = models.DateTimeField()  # Check-out time field for attendance
    date = models.DateField()  # Date field for attendance

    def __str__(self):
        return f"{self.employee.first_name} - {self.date}"

class Leave(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Foreign key relationship with Employee model
    start_date = models.DateField()  # Start date field for leave
    end_date = models.DateField()  # End date field for leave
    reason = models.TextField()  # Reason field for leave
    status = models.CharField(max_length=20)  # Status field for leave

    def __str__(self):
        return f"{self.employee.first_name} - {self.start_date} to {self.end_date}"

class Performance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Foreign key relationship with Employee model
    year = models.PositiveIntegerField()  # Year field for performance
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)  # Rating field for performance
    feedback = models.TextField()  # Feedback field for performance

    def __str__(self):
        return f"{self.employee.first_name} - {self.year}"

class Payroll(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)  # Foreign key relationship with Employee model
    month = models.PositiveIntegerField()  # Month field for payroll
    year = models.PositiveIntegerField()  # Year field for payroll
    salary = models.DecimalField(max_digits=10, decimal_places=2)  # Salary field for payroll
    deductions = models.DecimalField(max_digits=10, decimal_places=2, blank=True)  # Deductions field for payroll (optional)
    net_pay = models.DecimalField(max_digits=10, decimal_places=2, blank=True)  # Net pay field for payroll (optional)

    def __str__(self):
        return f"{self.employee.first_name} - {self.month}/{self.year}"

class Training(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)  # Title field for training
    description = models.TextField()  # Description field for training
    date = models.DateField()  # Date field for training
    location = models.CharField(max_length=100)  # Location field for training
    duration = models.PositiveIntegerField()  # Duration field for training
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, null=True)  # Foreign key relationship with Employee model

    def __str__(self):

        return f"{self.title} - {self.duration} weeks"

class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee = models.ForeignKey('Employee', on_delete=models.CASCADE, null=True)  # Foreign key relationship with Employee model
    title = models.CharField(max_length=100)  # Title field for document
    description = models.TextField()  # Description field for document
    file = models.FileField(upload_to='documents/', blank=True)  # File field for document (uploaded to 'documents/' directory)
    date_uploaded = models.DateField()  # Date uploaded field for document

    def __str__(self):
        return self.title

class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')  # One-to-one relationship with User model for profile
    profile_photo = CloudinaryField("image", null=True)  # Cloudinary image field for profile photo (optional)
    about = models.TextField(max_length=300)  # About field for profile
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)  # Foreign key relationship with Employee model
    birthdate = models.DateField(null=True)  # Birthdate field for profile (optional)
    nationality = models.CharField(max_length=100, null=True)  # Nationality field for profile (optional)
    emergency_contact_name = models.CharField(max_length=100, null=True)  # Emergency contact name field for profile (optional)
    emergency_contact_relationship = models.CharField(max_length=100, null=True)  # Emergency contact relationship field for profile (optional)
    emergency_contact_phone = models.CharField(max_length=20, null=True)  # Emergency contact phone field for profile (optional)
    emergency_contact_email = models.EmailField(null=True)  # Emergency contact email field for profile (optional)
    interests = models.CharField(max_length=255, blank=True)  # Interests field for profile (optional)

    updated_on = models.DateTimeField(auto_now=True, null=True)  # Auto-updated timestamp field for profile

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
