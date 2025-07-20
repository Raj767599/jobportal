from rest_framework import generics
from .models import Application
from .serializers import ApplicationSerializer
from .permissions import IsJobSeeker, IsEmployer
from rest_framework.permissions import IsAuthenticated
from apps.jobs.models import JobPost
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404

# Job seeker applies to a job
class ApplyToJobView(generics.CreateAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsJobSeeker]

    def create(self, request, *args, **kwargs):
        job_id = self.kwargs['job_id']
        job = get_object_or_404(JobPost, pk=job_id)

        if Application.objects.filter(job=job, applicant=self.request.user).exists():
            return Response({'detail': 'You have already applied to this job.'}, status=400)

        data = request.data.copy()
        data['job'] = job_id  # set the FK for serializer

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save(applicant=self.request.user, job=job)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# Seeker views their applications
class MyApplicationsView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsJobSeeker]

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user)

# Employer views applicants for a job
class ApplicantsForJobView(generics.ListAPIView):
    serializer_class = ApplicationSerializer
    permission_classes = [IsAuthenticated, IsEmployer]

    def get_queryset(self):
        job_id = self.kwargs['job_id']
        job = JobPost.objects.get(id=job_id)
        if job.employer != self.request.user:
            raise ValidationError("Unauthorized access.")
        return Application.objects.filter(job_id=job_id)

# Dummy
class DummyApplicationView(APIView):
    def get(self, request):
        return Response({"message": "Applications API working"})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsEmployer])
def update_application_status(request, pk):
    application = get_object_or_404(Application, id=pk)

    if application.job.employer != request.user:
        return Response({'detail': 'Unauthorized'}, status=403)

    new_status = request.data.get('status')
    if new_status not in ['shortlisted', 'rejected']:
        return Response({'detail': 'Invalid status'}, status=400)

    application.status = new_status
    application.save()
    return Response({'message': f"Application {new_status} successfully."})