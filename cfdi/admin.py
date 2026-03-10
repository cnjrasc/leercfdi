from django.contrib import admin
from .models import Contribuyente
#from .models import Cfdi
from import_export import resources
from import_export.admin import ImportExportModelAdmin

class ContribuyenteResource(resources.ModelResource):
    class Meta:
        model = Contribuyente
        
class ContribuyenteAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    search_fields = ['id']
    list_display = ('id', 'Nombre', 'Corto', 'RFC', 'CURP', 'Calle_No_Colonia', 'CODIGO_POSTAL', 'Entidad', 'Municipio_Alcaldía',)
    resources_class = ContribuyenteResource

#class CfdiResource(resources.ModelResource):
    #class Meta:
        #model = Cfdi
        
#class CfdiAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    #search_fields = ['id']
    #list_display = ('id', 'ruc', 'business_name', 'address', 'phone', 'email',)
    #resources_class = CfdiResource

# Register your models here.
admin.site.register(Contribuyente)
#admin.site.register(Cfdi)
