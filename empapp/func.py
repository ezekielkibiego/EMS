from rest_framework.views import APIView
from .serializers import EmployeeSerializer, ProfileSerializer
from .models import Profile
from rest_framework.response import Response


class UpdateEmployeeProfile(APIView):
    def post(self, request, username, *args, **kwargs):
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return Response({'message': 'User profile not found.'}, status=404)
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            employee = serializer.save()
            profile.employee = employee
            profile.save()
            return Response(ProfileSerializer(profile).data, status=200)
        return Response(serializer.errors, statu=400)
    def put(self, request, username, *args, **kwargs):
        try:
            profile = Profile.objects.get(user__username=username)
        except Profile.DoesNotExist:
            return Response({'message': 'User profile not found.'}, status=404)
        serializer = EmployeeSerializer(profile.employee, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(ProfileSerializer(profile).data, status=200)
        return Response(serializer.errors, status=400)