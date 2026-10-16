from rest_framework.test import APITestCase

from .models import Patient, User


class HealthcareApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            name="Owner",
            password="SecurePassword123!",
        )
        self.client.force_authenticate(user=self.user)

    def test_registration_and_login(self):
        self.client.force_authenticate(user=None)
        register_response = self.client.post(
            "/api/auth/register/",
            {
                "name": "New User",
                "email": "new@example.com",
                "password": "AnotherSecurePassword123!",
            },
            format="json",
        )
        self.assertEqual(register_response.status_code, 201)

        login_response = self.client.post(
            "/api/auth/login/",
            {
                "email": "new@example.com",
                "password": "AnotherSecurePassword123!",
            },
            format="json",
        )
        self.assertEqual(login_response.status_code, 200)
        self.assertIn("access", login_response.data)
        self.assertIn("refresh", login_response.data)

    def test_patient_doctor_and_mapping_endpoints(self):
        patient_data = {
            "name": "Patient One",
            "age": 35,
            "gender": "Female",
            "phone": "1234567890",
            "address": "1 Health Street",
        }
        patient_response = self.client.post("/api/patients/", patient_data, format="json")
        self.assertEqual(patient_response.status_code, 201)
        patient_id = patient_response.data["id"]

        self.assertEqual(self.client.get("/api/patients/").status_code, 200)
        self.assertEqual(self.client.get(f"/api/patients/{patient_id}/").status_code, 200)

        doctor_data = {
            "name": "Doctor One",
            "specialization": "Cardiology",
            "email": "doctor@example.com",
            "phone": "0987654321",
        }
        doctor_response = self.client.post("/api/doctors/", doctor_data, format="json")
        self.assertEqual(doctor_response.status_code, 201)
        doctor_id = doctor_response.data["id"]
        self.assertEqual(self.client.get("/api/doctors/").status_code, 200)
        self.assertEqual(self.client.get(f"/api/doctors/{doctor_id}/").status_code, 200)

        mapping_response = self.client.post(
            "/api/mappings/",
            {"patient": patient_id, "doctor": doctor_id},
            format="json",
        )
        self.assertEqual(mapping_response.status_code, 201)
        mapping_id = mapping_response.data["id"]
        self.assertEqual(self.client.get("/api/mappings/").status_code, 200)
        assigned_doctors = self.client.get(f"/api/mappings/{patient_id}/")
        self.assertEqual(assigned_doctors.status_code, 200)
        self.assertEqual(assigned_doctors.data[0]["id"], doctor_id)
        self.assertEqual(
            self.client.post(
                "/api/mappings/",
                {"patient": patient_id, "doctor": doctor_id},
                format="json",
            ).status_code,
            400,
        )
        self.assertEqual(
            self.client.delete(f"/api/mappings/{mapping_id}/").status_code,
            204,
        )

        patient_update = {**patient_data, "name": "Updated Patient"}
        self.assertEqual(
            self.client.put(
                f"/api/patients/{patient_id}/",
                patient_update,
                format="json",
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.delete(f"/api/patients/{patient_id}/").status_code,
            204,
        )
        self.assertEqual(
            self.client.put(
                f"/api/doctors/{doctor_id}/",
                {**doctor_data, "name": "Updated Doctor"},
                format="json",
            ).status_code,
            200,
        )
        self.assertEqual(
            self.client.delete(f"/api/doctors/{doctor_id}/").status_code,
            204,
        )

    def test_patient_records_are_private(self):
        patient = Patient.objects.create(
            name="Private Patient",
            age=40,
            gender="Male",
            phone="1234567890",
            address="2 Health Street",
            created_by=self.user,
        )
        other_user = User.objects.create_user(
            email="other@example.com",
            name="Other User",
            password="SecurePassword123!",
        )
        self.client.force_authenticate(user=other_user)
        self.assertEqual(self.client.get("/api/patients/").data, [])
        self.assertEqual(self.client.get(f"/api/patients/{patient.id}/").status_code, 404)
