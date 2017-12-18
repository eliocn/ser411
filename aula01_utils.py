# encoding: utf-8
#

# Carrega a Biblioteca GDAL/OGR
from osgeo import ogr

def Geo2Grid (location,dimensions,resolution,extent):

    """
    Converte um ponto geografico (lon x lat) na posicao da matriz (coluna x linha)
    considerando que o zero e no canto superior esquerdo
    
    Parametros:
    :param location (Geometry):
    :param dimensions (dict):
    :param resoution (Dict):
    :param extent (Dict):
    :return: (int,int) - retorna o numero da linha e da coluna
    """
    
    x = location.GetX()
    y = location.GetY()

    col = int((x-extent['xmin'])/resolution['x'])
    row = int(dimensions['rows']-((y-extent['ymin'])/resolution['y']))

return col,row
