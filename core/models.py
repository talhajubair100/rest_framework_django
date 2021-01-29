from django.db import models

# Create your models here.

class Profession(models.Model):
    description = models.CharField(max_length=150)

    def __str__(self):
        return self.description

class DataSheet(models.Model):
    description = models.CharField(max_length=150)
    histoy_data = models.TextField()

    def __str__(self):
        return self.description


class Customer(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=150)
    profession = models.ManyToManyField(Profession)
    data_sheet = models.OneToOneField(DataSheet, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Document(models.Model):
    CHOICES = (
        ("PP", 'Passport'),
        ("ID", 'Id Card'),
        ("OT", 'Others'),
    )
    doc_type = models.CharField(choices=CHOICES, max_length=15)
    doc_name = models.CharField(max_length=50)
    customer = models.ForeignKey(Customer , on_delete=models.CASCADE)

    def __str__(self):
        return self.doc_name
