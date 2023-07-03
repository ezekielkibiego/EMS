from rest_framework import serializers
from .models import *

from django.contrib.auth.models import User

from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserRegistrationSerializer(serializers.ModelSerializer):
    repeat_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'repeat_password']

    def validate(self, attrs):
        password = attrs.get('password')
        repeat_password = attrs.pop('repeat_password')

        if password != repeat_password:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'slug', 'first_name', 'middle_name', 'last_name', 'gender', 'phone', 'email', 'role', 'manager', 'marital_status', 'address', 'start_date', 'end_date']


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class LeaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leave
        fields = '__all__'


class PerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = '__all__'


class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = '__all__'


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = '__all__'


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    employee = EmployeeSerializer()
    class Meta:
        model = Profile
        fields = '__all__'

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['profile_phote', 'about', 'birthdata', 'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_email', 'emergency_contact_relationship', 'interests', 'nationality']



