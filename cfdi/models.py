from django.db import models
from django.contrib.postgres.search import SearchQuery, SearchVector
from cfdi.templates.utils import convertir_fecha_iso
from simple_history.models import HistoricalRecords
# Create your models here.


class BaseModel(models.Model):
    id = models.AutoField(primary_key= True)
    state = models.BooleanField('State', default= True)
    created_date = models.DateField('Fecha de Creación', auto_now=False, auto_now_add= True)
    modified_date = models.DateField('Fecha de Modificación', auto_now=True, auto_now_add= False)
    deleted_date = models.DateField('Fecha de Eliminación', auto_now=True, auto_now_add= False)
    #historical = HistoricalRecords(inherit=True)
    history = HistoricalRecords(inherit=True)
    
    @property
    def _history_user(self):
        return self.changed_by
    
    @_history_user.setter
    def _history_user(self, value):
        self.changed_by = value
   
    class Meta:
        abstract = True
        verbose_name = 'Modelo Base'
        verbose_name_plural = 'Modelos Base' 

class Contribuyente(BaseModel):
    Nombre_Razon_Social = models.CharField(max_length=30, verbose_name='Nombre', unique=True)
    Nombre_Corto = models.CharField(max_length=3, verbose_name='Corto', default='')
    #Personalidad = models.CharField(max_length=2, choices=personalidad, default='', verbose_name='Personalidad')
    RFC = models.CharField(max_length=13)
    CURP = models.CharField(max_length=18,blank=True, null=True, verbose_name='CURP')
    Calle_No_Colonia = models.CharField(max_length=50, verbose_name='Calle_No_Colonia')
    CODIGO_POSTAL = models.CharField(max_length=5, verbose_name='CODIGO_POSTAL')
    #cp = models.ForeignKey(Set)
    Entidad = models.CharField(max_length=30, verbose_name='Entidad')
    Municipio_Alcaldía = models.CharField(max_length=30, verbose_name='Municipio_Alcaldía')

    class Meta:
        verbose_name = 'Contribuyente'
        verbose_name_plural = 'Contribuyentes'
        ordering = ['Nombre_Razon_Social']
 
    def __str__(self):
        return self.Nombre_Corto
    


#class Cfdi(BaseModel):
    #ruc = models.CharField(unique=True, max_length=11)
    #business_name = models.CharField('Razón Social', unique=True, max_length=150, null=False, blank=False)
    #address = models.CharField(max_length=200)
    #phone = models.CharField(max_length=15, null=True, blank=True)
    #email = models.EmailField(null=True)

    #class Meta:
        #ordering = ['id']
        #verbose_name = 'Cfdi'
        #verbose_name_plural = 'Cfdis'   

    #def __str__(self):
        #return self.business_name

    #def to_dict(self):
        #return {
            #'id': self.id,
            #'ruc': self.ruc,
            #'business_name': self.business_name,
            #'address': self.address,
            #'phone': self.phone,
            #'email': self.email
        #}
