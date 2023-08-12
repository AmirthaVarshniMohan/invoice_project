# invoice_app/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Invoice, InvoiceDetail

class InvoiceTests(APITestCase):

    def test_create_invoice(self):
        url = reverse('invoice-list')
        data = {
            'date': '2023-08-01',
            'invoice_no': 'INV001',
            'customer_name': 'Ami Varsh'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(Invoice.objects.get().invoice_no, 'INV001')

    def test_get_invoice_list(self):
        url = reverse('invoice-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invoice_detail(self):
        invoice = Invoice.objects.create(date='2023-08-01', invoice_no='INV001', customer_name='John Doe')
        url = reverse('invoice-detail', args=[invoice.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class InvoiceDetailTests(APITestCase):

    def test_create_invoice_detail(self):
        invoice = Invoice.objects.create(date='2023-08-01', invoice_no='INV001', customer_name='John Doe')
        url = reverse('invoicedetail-list')
        data = {
            'invoice': invoice.id,
            'description': 'Product A',
            'quantity': 2,
            'unit_price': '50.00',
            'price': '100.00'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InvoiceDetail.objects.count(), 1)
        self.assertEqual(InvoiceDetail.objects.get().description, 'Product A')

    def test_get_invoice_detail_list(self):
        url = reverse('invoicedetail-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invoice_detail_detail(self):
        invoice = Invoice.objects.create(date='2023-08-01', invoice_no='INV001', customer_name='John Doe')
        detail = InvoiceDetail.objects.create(invoice=invoice, description='Product A', quantity=2, unit_price='50.00', price='100.00')
        url = reverse('invoicedetail-detail', args=[detail.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

