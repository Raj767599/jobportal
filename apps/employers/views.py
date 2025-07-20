from rest_framework import generics, permissions
from .models import EmployerProfile
from .serializers import EmployerProfileSerializer
from .permissions import IsEmployer
from rest_framework.views import APIView
from rest_framework.response import Response

class EmployerProfileView(generics.RetrieveUpdateAPIView):
    queryset = EmployerProfile.objects.all()
    serializer_class = EmployerProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsEmployer]

    def get_object(self):
        return EmployerProfile.objects.get(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Dummy route for Swagger test
class DummyEmployerView(APIView):
    def get(self, request):
        return Response({"message": "Employer API working"})
