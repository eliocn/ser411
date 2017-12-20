# encoding: utf-8

# importando bibliotecas e scripts necessarios

# biblioteca com funcionalidades do sistema (pasta/caminhos)
import sys
# biblioteca com as funcionalidades do sistema operacional
import os
# biblioteca NumPy para criar de matrizes
import numpy as np
# biblioteca gdal -> retorna erro se nao estiver instalada
try:
    from osgeo import gdal, ogr, osr
except:
    sys.exit("Erro: a biblioteca GDAL não foi encontrada!")
# script utils 
from utils import *

# habilita exceções caso tenha erros nas rotinas da gdal/ogr
gdal.UseExceptions()
ogr.UseExceptions()
osr.UseExceptions()

# define nome do arquico incluindo caminho do SO
vector_file = "/home/labgeo3/eliana/dados/Queimadas/focos/focos-2016.shp"
vector_file_base_name = os.path.basename(vector_file) # armazena o nome do arquivo
layer_name = os.path.splitext(vector_file_base_name)[0] #armazena o caminho do arquivo

# dimensoes para criar a grade
spatial_extent = { 'xmin': -89.975, 'ymin': -59.975,
                   'xmax': -29.975, 'ymax': 10.025 }
spatial_resolution = { 'x': 0.05, 'y': 0.05 }
grid_dimensions = { 'cols': 1200, 'rows': 1400 }

# formato do arquivo de saida e caminho
file_format = "GTiff"
output_file_name = "/home/labgeo3/eliana/dados/Queimadas/focos/grade-2016.tiff"

# abre arquivo vetorial 
shp_focos = ogr.Open(vector_file)
if shp_focos is None:
    sys.exit("Erro: não foi possivel abrir o arquivo {0} !".format(vector_file)) #mensagem de erro

# pega apenas o layer (conjunto de feicoes)
layer_focos = shp_focos.GetLayer(layer_name)
if layer_focos is None:
    sys.exit("Erro: não foi possível acessar a camada '{0}' no arquivo {1}!".format(layer_name, vector_file))

# criando a matriz numerica 
matriz = np.zeros((grid_dimension['rows'],grid_dimension['cols']),np.uint16)

# calcula numero de focos em cada celula - associa cada foco com a localizacao geografica
for foco in layer_focos:
    location = foco.GetGeometryRef()
    col, row = Geo2Grid(location, grid_dimensions,
                        spatial_resolution, spatial_extent)
    matriz[row, col] += 1

# cria raster de saida - formato geotiff  
driver = gdal.GetDriverByName(file_format)
if driver is None:
    sys.exit("Erro: não foi possível identificar o driver '{0}'.".format(file_format))

raster = driver.Create(output_file_name,
                       grid_dimensions['cols'], grid_dimensions['rows'],
                       1, gdal.GDT_UInt16)
if raster is None:
    sys.exit("Erro: não foi possível criar o arquivo '{0}'.".format(output_file_name))

# transforma coordenada
raster.SetGeoTransform((spatial_extent['xmin'], spatial_resolution['x'], 0,
                        spatial_extent['ymax'], 0, -spatial_resolution['y']))

# usa a informacao que ja ta pronta (layer focos) pra pra definir a grade de saida
srs_focos = layer_focos.GetSpatialRef()
raster.SetProjection(srs_focos.ExportToWkt())

band = raster.GetRasterBand(1)
band.WriteArray(matriz, 0, 0)
band.FlushCache()

# garantia
raster = None
del raster, band
