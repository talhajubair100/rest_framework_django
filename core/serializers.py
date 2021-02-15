from django.db import models
from django.db.models import fields
from rest_framework import serializers
from .models import Customer, Profession, DataSheet, Document


class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = ('description', 'histoy_data')


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('description', )



class CustomerSerializer(serializers.ModelSerializer):
    number_profession = serializers.SerializerMethodField()
    #data_sheet = serializers.StringRelatedField()
    #data_sheet = serializers.SerializerMethodField()  
    data_sheet = DataSheetSerializer() #for nested relationship
    #profession = serializers.StringRelatedField(many=True)
    profession = ProfessionSerializer(many=True)  #for nested relationship
    document_set = serializers.StringRelatedField(many=True)

    class Meta:
        model = Customer
        fields = ('name', 'address', 'profession', 'data_sheet', 'active', 'status_message', 'number_profession', 'document_set')

    def get_number_profession(self, obj):
        return obj.num_profesion()

    def get_data_sheet(self, obj):
        return obj.data_sheet.description

# class ProfessionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profession
#         fields = ('description')



class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('doc_type', 'doc_name', 'customer')


# class DataSheetSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DataSheet
#         fields = ('description', 'histoy_data')
        