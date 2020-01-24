import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','toca.settings')

import django
django.setup()

from lugar.models import Region, Provincia, Comuna
from lugar.divpoladmchile import regiones, provincias, comunas

def carga_regiones(datosRegion):
    '''
    DOCSTRING: Inserta region y codigo de region en la tabla region
    INPUT: Tupla de codigo y region
    OUTPUT: Region desde tabla
    '''
    region = Region.objects.get_or_create(
        codigo=datosRegion[0],
        nombre=datosRegion[1])[0]
    region.save()

    return region

def carga_provincias(datosProvincia, region):
    '''
    DOCSTRING: Inserta provincia y codigo de provincia en la tabla provincia
    INPUT: Tupla de codigo y provincia; y region a la que pertenece
    OUTPUT: Provincia desde tabla
    '''
    provincia = Provincia.objects.get_or_create(
        codigo=datosProvincia[0],
        nombre=datosProvincia[1],
        region=region)[0]
    provincia.save()

    return provincia

def carga_comunas(datosComuna, region, provincia):
    '''
    DOCSTRING: Inserta comuna y codigo de comuna en la tabla comuna
    INPUT: Tupla de codigo y comuna; la region y provincia a la que pertenece
    OUTPUT: Comuna desde tabla
    '''
    comuna = Comuna.objects.get_or_create(
        codigo=datosComuna[0],
        nombre=datosComuna[1],
        region=region,
        provincia=provincia)[0]
    comuna.save()

    return comuna

def cargar_datos():
    for reg in regiones:
        region = carga_regiones(reg)
        print('Region '+region.nombre+' agregada')
        for pro in provincias:
            if reg[0] == pro[0][0:2]:
                provincia = carga_provincias(pro,region=region)
                print('Provincia '+provincia.nombre+' agregada')
                for com in comunas:
                    if pro[0] == com[0][0:3]:
                        comuna = carga_comunas(com,region=region, provincia=provincia)
                        print('Comuna '+comuna.nombre+' agregada')



if __name__ == '__main__':
    print('Cargando datos ...')
    cargar_datos()
    print('Carga finalizada!!!')
