from __future__ import unicode_literals

from django.db import models
from model_utils.models import TimeStampedModel


class Country(models.Model):
    iso_code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return "{0}".format(self.name)


class Company(TimeStampedModel):
    companies_house_id = models.CharField(max_length=8, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    date_founded = models.DateField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Deal(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date_of_deal = models.DateField()
    amount_raised = models.FloatField()

    class Meta:
        ordering = ["-date_of_deal"]

    def __unicode__(self):
        return "{0} raised by {1} ({2})".format(
            self.amount_raised, self.company, self.date_of_deal
        )


class Employee(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    job_title = models.CharField(max_length=200)

    GENDERS = (
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    )
    gender = models.CharField(max_length=1, choices=GENDERS)

    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True)

    class Meta:
        ordering = ["name", "-created"]
        unique_together = ("company", "email")

    def __unicode__(self):
        return "{0} ({1})".format(self.name, self.company)
