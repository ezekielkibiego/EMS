from django.db import IntegrityError
from django.forms import ValidationError
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Company

class CompanyModelTestCase(TestCase):
    def setUp(self):
        self.company_data = {
            'coName': 'Test Company',
            'coEmail': 'test@example.com',
            'coLogo': SimpleUploadedFile('logo.jpg', b'file_content', content_type='image/jpeg'),
            'coAddress': 'Test Address'
        }

    def test_create_company(self):
        company = Company.objects.create(**self.company_data)
        self.assertEqual(company.coName, self.company_data['coName'])
        self.assertEqual(company.coEmail, self.company_data['coEmail'])
        self.assertEqual(company.coAddress, self.company_data['coAddress'])

    def test_coName_as_primary_key(self):
        company = Company.objects.create(**self.company_data)
        self.assertEqual(company.pk, self.company_data['coName'])

    def test_coLogo_upload(self):
        company = Company.objects.create(**self.company_data)
        self.assertIsNotNone(company.coLogo)

    def test_coLogo_deletion(self):
        company = Company.objects.create(**self.company_data)
        company.coLogo.delete()
        self.assertIsNone(company.coLogo)

    def test_coEmail_validation(self):
        invalid_email = 'invalid_email'
        self.company_data['coEmail'] = invalid_email
        with self.assertRaises(ValidationError):
            Company.objects.create(**self.company_data)

    def test_coName_uniqueness(self):
        Company.objects.create(**self.company_data)
        with self.assertRaises(IntegrityError):
            Company.objects.create(**self.company_data)

    def test_str_representation(self):
        company = Company.objects.create(**self.company_data)
        self.assertEqual(str(company), self.company_data['coName'])
