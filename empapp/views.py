
from django.http import HttpResponseRedirect
from .models import *
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from .forms import *
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from empapp.serializers import *
from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from rest_framework.permissions import AllowAny, IsAuthenticated


class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User registered successfully.'})
        return Response(serializer.errors, status=400)

@permission_classes([AllowAny, ])
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'User logged in successfully.',
                             "user": UserRegistrationSerializer(user).data})
        return Response({'message': 'Invalid credentials.'}, status=401)
    


# To retrieve Company details
def index(request):
    return render(request, "index.html")

@api_view(['GET'])
def companies(request):
    if request.method == 'GET':
        companies = Company.objects.all()
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def educations(request):
    if request.method == 'GET':
        educations = Education.objects.all()
        serializer = EducationSerializer(educations, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def education_detail(request, id):
    try:
        education = Education.objects.get(id=id)
    except Education.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = EducationSerializer(education, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        education.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['GET'])
def employee_edu(request, id):
    try:
        education = Education.objects.get(id=id)
    except Education.DoesNotExist:
        return Response({'message': 'Employee Education not found.'}, status=404)

    if request.method == 'GET':
        serializer = EducationSerializer(education)
        return Response(serializer.data)

@api_view(['GET', 'POST'])
def roles(request):
    if request.method == 'GET':
        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def departs(request):
    if request.method == 'GET':
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def employees(request):
    if request.method == 'GET':
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def employee_detail(request, slug):
    try:
        employee = Employee.objects.get(slug=slug)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET', 'POST'])
def attendances(request):
    if request.method == 'GET':
        attendances = Attendance.objects.all()
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = AttendanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def leaves(request):
    if request.method == 'GET':
        leaves = Leave.objects.all()
        serializer = LeaveSerializer(leaves, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = LeaveSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def performances(request):
    if request.method == 'GET':
        performances = Performance.objects.all()
        serializer = PerformanceSerializer(performances, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PerformanceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def payrolls(request):
    if request.method == 'GET':
        payrolls = Payroll.objects.all()
        serializer = PayrollSerializer(payrolls, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PayrollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def trainings(request):
    if request.method == 'GET':
        trainings = Training.objects.all()
        serializer = TrainingSerializer(trainings, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TrainingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def documents(request):
    if request.method == 'GET':
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = DocumentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def profiles(request):
    if request.method == 'GET':
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)
    
@api_view(['GET'])
def user_profile(request, username):
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        return Response({'message': 'User profile not found.'}, status=404)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

@api_view(['PUT'])
def update_user_profile(request, username):
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        return Response({'message': 'User profile not found.'}, status=404)

    if request.method == 'PUT':
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
