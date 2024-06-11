from django.db import models
from django.urls import reverse
import uuid

class LunchboxModel(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    lunchbox_name = models.CharField(max_length=20, help_text='Enter lunchbox name')
    lunchbox_summary = models.TextField(default="summary", max_length=100, help_text="Enter lunchbox summary")
    lunchbox_cost = models.IntegerField(help_text='Enter lunchbox cost')
    # …

    # Metadata
    class Meta:
        ordering = ['lunchbox_name']

    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('lunchbox-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.lunchbox_name

class BuyingModel(models.Model):
    """A typical class defining a model, derived from the Model class."""

    # Fields
    uuid = models.UUIDField( default=uuid.uuid4,
                          help_text="Unique ID for Buy Info")
    customer_name = models.CharField(max_length=20, help_text='Enter customer name')
    customer_phone = models.CharField(max_length=10, help_text='Enter customer phone number')
    meat_num = models.IntegerField(help_text='Enter lunchbox number')
    vege_num = models.IntegerField(help_text='Enter lunchbox number')
    total_cost = models.IntegerField(help_text='Enter total cost')
    buytime = models.DateField(null=True, blank=True)
    # …

    # Metadata
    class Meta:
        ordering = ['id']

    # Methods
    def get_absolute_url(self):
        """Returns the URL to access a particular instance of MyModelName."""
        return reverse('buying-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the MyModelName object (in Admin site etc.)."""
        return self.customer_name + "訂單"