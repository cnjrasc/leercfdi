from django.urls import path
from django.contrib import admin
from . import views
from cfdi.views import *
from cfdi.views import convert_cfdi_view
from cfdi.views import procesar_zip_view
from cfdi.views import historial_cfdis_view, eliminar_cfdi_view

from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('inicio', views.inicio, name='inicio'),
    path('admin/', admin.site.urls),
    path('contribuyente', views.contribuyente, name='contribuyente'),
    path('contribuyente/altaem', views.altaem, name='altaem'),
    path('contribuyente/editarem', views.editarem, name='editarem'),
    path('contribuyente/eliminarem/<int:id>',views.eliminarem, name='eliminarem'),
    path('contribuyente/editarem/<int:id>',views.editarem, name='editarem'),
    #path('cfdi', views.cfdi, name='cfdi'),
    #path('cfdi/altaem', views.altaem, name='altaem'),
    #path('cfdi/editarem', views.editarem, name='editarem'),
    #path('cfdi/eliminarem/<int:id>',views.eliminarem, name='eliminarem'),
    #path('cfdi/editarem/<int:id>',views.editarem, name='editarem'),
    path('convert-cfdi/', convert_cfdi_view, name='convert-cfdi'),
    path('procesar-zip/', procesar_zip_view, name='procesar-zip'),
    path('historial_cfdis/', historial_cfdis_view, name='historial_cfdis'),
    path('historial/eliminar_cfdi/<str:nombre>/', eliminar_cfdi_view, name='eliminar_cfdi'),
                
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)