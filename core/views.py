from django.db.models import manager
from core.models import Customer, Profession, DataSheet, Document
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import CustomerSerializer, ProfessionSerializer, DataSheetSerializer, DocumentSerializer
from rest_framework.decorators import action
from django.http.response import HttpResponseNotAllowed
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny

# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    filterset_fields = ['address']
    search_fields = ['name', 'address', 'data_sheet__description']
    ordering_fields = ['id', 'name']
    ordering = ['-id']
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication,]

    def get_queryset(self):
        address = self.request.query_params.get('address', None)

        if self.request.query_params.get('active') == 'False':
            status = False
        else:
            status = True

        #status = True if self.request.query_params['active'] == 'True' else False

        if address:
            customer = Customer.objects.filter(address__icontains=address, active=status)
        else:
            customer = Customer.objects.filter(active=status)
        return customer
    
    # def list(self, request, *args, **kwargs):
    #     customers = self.get_queryset()
    #     serializer = CustomerSerializer(customers, many=True)
    #     return Response(serializer.data)

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


    @action(detail=True)
    def deactivate(self, request, *args, **kwargs):
        customer = self.get_object()
        customer.active = False
        customer.save()

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)


    # @action(detail=True)
    # def activate(self, request, *args, **kwargs):
    #     customer = self.get_object()
    #     print(customer)
    #     customer.active = True
    #     customer.save()
    #     serializer = CustomerSerializer(customer)
    #     return Response(serializer.data)

    @action(detail=False)
    def deactivate_all(self, request, *args, **kwargs):
        customers = self.get_queryset()
        customers.update(active=False)
        
        serialzer = CustomerSerializer(customers, many=True)
        return Response(serialzer.data)

    
    @action(detail=False)
    def activate_all(self, request, *args, **kwargs):
        customers = self.get_queryset()
        customers.update(active=True)
        
        serialzer = CustomerSerializer(customers, many=True)
        return Response(serialzer.data)


    @action(detail=False, methods=['POST'])
    def chg_status(self, request, *args, **kwargs):
        status = True if request.data['active'] == 'True' else False

        customers = self.get_queryset()
        customers.update(active=status)

        serialzer = CustomerSerializer(customers, many=True)
        return Response(serialzer.data)



class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    authentication_classes = [TokenAuthentication,]


class DataSheetViewSet(viewsets.ModelViewSet):
    queryset = DataSheet.objects.all()
    serializer_class = DataSheetSerializer
    permission_classes = [AllowAny, ]

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer