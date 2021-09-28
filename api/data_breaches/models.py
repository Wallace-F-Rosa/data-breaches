from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
class Source(models.Model):
    """
    Model storing url's of midia sources covering data breaches.

    Attributes:
        url (URLField) : url of the midia source.
        data_breach (ForeignKey) : wich data breach the source covers.

    Relations:
        * Source - DataBreach (N:1) : one data breach can have many midia sources as reference.
    """
    url = models.URLField()
    data_breach = models.ForeignKey('DataBreach', related_name='databreach',on_delete=models.PROTECT)

class OrganizationType(models.Model):
    """
    Model storing entity organization type. Represents the sphere of action
    of an entity.

    Attributes:
        organization_type (CharField) : string representing sphere of action.
        entity (ForeignKey) : foreign key relationship with Entity Model.

    Relations:
        * OrganizationType - Entity (N:1) : one entity can act in many fields of work.
    """
    organization_type = models.CharField(max_length=30)
    entity = models.ForeignKey('Entity', on_delete=models.PROTECT)
    
    class Meta:
        unique_together = ('organization_type', 'entity')

class Entity(models.Model):
    """
    Model storing the data of entities involved on data breaches.

    Attributes:
        name (CharField) : string containing entity name.

    Relations :
        * Entity - DataBreach (1:N) : one entity can be involved in many data breaches(yikes).
        * Entity - OrganizationType (1:N) : one entity can have a broad sphere of action with many fields of work.
    """
    name = models.CharField(max_length=500, unique=True)

class DataBreach(models.Model):
    """
    Model that stores data breaches data.

    Attributes:
        year (PositiveSmallIntegerField) : integer of the year when the data breach happened.
        records (PositiveIntegerField) : integer containing the amount of compromised records.
        method (CharField): string containing the method used in the breaching process.

    Relations:
        * DataBreach - Entity (N:1) : one data breach involves one entity. but an entity can be
        involved in many data breaches.
        * DataBreach - OrganizationType (1:N) : The entity related to the data breach can have
    """
    entity = models.ForeignKey('Entity', related_name='entity',on_delete=models.PROTECT)
    year = models.PositiveSmallIntegerField(validators=[MinValueValidator(1970)])
    records = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    method = models.CharField(max_length=30)
