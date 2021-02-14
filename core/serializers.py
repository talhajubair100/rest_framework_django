from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Customer, Profession, DataSheet, Document

class CustomerSerializer(serializers.ModelSerializer):
    number_profession = serializers.SerializerMethodField()
    class Meta:
        model = Customer
        fields = ('name', 'address', 'profession', 'data_sheet', 'active', 'status_message', 'number_profession')

    def get_number_profession(self, obj):
        return obj.num_profesion()

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('description')

class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = ('description', 'histoy_data')

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('doc_type', 'doc_name', 'customer')