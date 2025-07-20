from rest_framework import generics
from .models import User
from .serializers import UserRegistrationSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from rest_framework import status

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({
            "message": "User registered successfully",
            "user": serializer.data
        }, status=status.HTTP_201_CREATED)



class DummyUserView(APIView):
    def get(self, request):
        return Response({"message": "User API working"})