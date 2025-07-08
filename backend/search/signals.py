from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from companies.models import Company, Employee
from search_service.indexing import (
    index_company,
    index_employee,
    delete_company,
    delete_employee,
)


@receiver(post_save, sender=Company)
def handle_company_save(sender, instance, **kwargs):
    """Index company when saved."""
    index_company(instance)


@receiver(post_delete, sender=Company)
def handle_company_delete(sender, instance, **kwargs):
    """Remove company from index when deleted."""
    delete_company(instance.id)


@receiver(post_save, sender=Employee)
def handle_employee_save(sender, instance, **kwargs):
    """Index employee when saved."""
    index_employee(instance)


@receiver(post_delete, sender=Employee)
def handle_employee_delete(sender, instance, **kwargs):
    """Remove employee from index when deleted."""
    delete_employee(instance.id)
