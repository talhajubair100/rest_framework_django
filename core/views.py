from django.db.models import manager
from core.models import Customer, Profession, DataSheet, Document
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import CustomerSerializer, ProfessionSerializer, DataSheetSerializer, DocumentSerializer
from django.http.response import HttpResponseNotAllowed

# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    def get_queryset(self):
        active_customer = Customer.objects.filter(active=True)
        return active_customer
    
    def list(self, request, *args, **kwargs):
        customers = Customer.objects.filter(id=3)
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = CustomerSerializer(obj)
        return Response(serializer.data)
        #return HttpResponseNotAllowed('not allowed')
    
    def create(self, request, *args, **kwargs):
        data = request.data
        customer = Customer.objects.create(name=data['name'], address=data['address'], data_sheet_id=data['data_sheet'])
        profession = Profession.objects.get(id=data['profession'])
        customer.profession.add(profession)
        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        customer = self.get_object()
        data = request.data
        customer.name = data['name']
        customer.address = data['address']
        customer.data_sheet_id = data['data_sheet']

        profession = Profession.objects.get(id=data['profession'])

        for p in customer.profession.all():
            customer.profession.remove(p)

        customer.profession.add(profession)
        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


    def partial_update(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.name = request.data.get('name', customer.name)
        customer.address = request.data.get('address', customer.address)
        customer.data_sheet_id = request.data.get('data_sheet', customer.data_sheet_id)

        customer.save()
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.delete()

        return Response("object remove")


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer

class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer