from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("An email address is required.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields["is_staff"] is not True:
            raise ValueError("A superuser must have is_staff=True.")
        if extra_fields["is_superuser"] is not True:
            raise ValueError("A superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class Patient(models.Model):
    name = models.CharField(max_length=150)
    age = models.PositiveSmallIntegerField()
    gender = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patients")

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=150)
    specialization = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class PatientDoctorMapping(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="doctor_mappings")
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="patient_mappings")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["patient", "doctor"], name="unique_patient_doctor")
        ]

    def __str__(self):
        return f"{self.patient} - {self.doctor}"
