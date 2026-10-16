from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Doctor, Patient, PatientDoctorMapping
from .serializers import (
    DoctorSerializer,
    PatientDoctorMappingSerializer,
    PatientSerializer,
    RegisterSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer

    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class PatientDoctorMappingListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientDoctorMappingSerializer

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(patient__created_by=self.request.user)


class PatientDoctorMappingDetailView(APIView):
    def get(self, request, patient_id):
        patient = get_object_or_404(Patient, id=patient_id, created_by=request.user)
        doctors = Doctor.objects.filter(patient_mappings__patient=patient)
        return Response(DoctorSerializer(doctors, many=True).data)

    def delete(self, request, patient_id):
        mapping = get_object_or_404(
            PatientDoctorMapping,
            id=patient_id,
            patient__created_by=request.user,
        )
        mapping.delete()
        return Response(status=204)
