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













