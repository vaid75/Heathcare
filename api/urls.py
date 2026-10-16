from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    DoctorViewSet,
    PatientDoctorMappingDetailView,
    PatientDoctorMappingListCreateView,
    PatientViewSet,
)


router = DefaultRouter()
router.register("patients", PatientViewSet, basename="patient")
router.register("doctors", DoctorViewSet, basename="doctor")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "mappings/",
        PatientDoctorMappingListCreateView.as_view(),
        name="mapping-list",
    ),
    path(
        "mappings/<int:patient_id>/",
        PatientDoctorMappingDetailView.as_view(),
        name="mapping-detail",
    ),
]
