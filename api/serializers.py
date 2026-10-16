from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Doctor, Patient, PatientDoctorMapping, User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ["id", "name", "email", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ["id", "name", "age", "gender", "phone", "address"]
        read_only_fields = ["id"]


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ["id", "name", "specialization", "email", "phone"]
        read_only_fields = ["id"]


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDoctorMapping
        fields = ["id", "patient", "doctor"]
        read_only_fields = ["id"]

    def validate_patient(self, patient):
        if patient.created_by_id != self.context["request"].user.id:
            raise serializers.ValidationError("You can only assign doctors to your own patients.")
        return patient

    def validate(self, attrs):
        if PatientDoctorMapping.objects.filter(
            patient=attrs["patient"],
            doctor=attrs["doctor"],
        ).exists():
            raise serializers.ValidationError("This doctor is already assigned to this patient.")
        return attrs
