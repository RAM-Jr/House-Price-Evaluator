from django.contrib import admin
from.models import Imovel,Tipologia,Design,Bairro,Avaliacao

# Register your models here.
admin.site.register(Imovel)
admin.site.register(Tipologia)
admin.site.register(Design)
admin.site.register(Bairro)
admin.site.register(Avaliacao)