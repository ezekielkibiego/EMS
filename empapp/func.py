from rest_framework.views import APIView
from .serializers import EmployeeSerializer, ProfileSerializer, ChangePasswordSerializer, UpdateEmployeeRoleManagerSerializer, UpdateEmployeeSerializer
from .models import Profile, Employee
from rest_framework.response import Response
from django.contrib.auth import authenticate


class UpdateEmployeeProfile(APIView):
    def post(self, request, username, *args, **kwargs):
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return Response({'message': 'User profile not found.'}, status=404)
        serializer = UpdateEmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            profile.employee = employee
            profile.save()
            return Response(ProfileSerializer(profile).data, status=200)
        return Response(serializer.errors, status=400)
    def put(self, request, username, *args, **kwargs):
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return Response({'message': 'User profile not found.'}, status=404)
        serializer = UpdateEmployeeSerializer(profile.employee, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(ProfileSerializer(profile).data, status=200)
        return Response(serializer.errors, status=400)
    
class ChangePassword(APIView):
    def put(self, request, username, *args, **kwargs):
        serializer = ChangePasswordSerializer(data = request.data)
        if serializer.is_valid():
            user = authenticate(username=username, password = request.data['old_password'])
            if user is not None:
                user.set_password(request.data['new_password'])
                user.save()
                return Response({'Msg': 'Success'}, status=200)
            return Response({'Msg': 'Wrong Credentials'}, status=404)
        return Response(serializer.errors, status=400)

class ChangeEmployeeRoleManager(APIView):
    def put(self, request, id, *args, **kwargs):
        try:
            employee = Employee.objects.filter(id = id).first()
        except:
            return Response({'message': 'Employee not found'}, status=404)
        serializer = UpdateEmployeeRoleManagerSerializer(employee, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Msg: Success'}, status=200)
        return Response(serializer.errors, status=400)
        