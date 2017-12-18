# encoding: utf-8

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os

os.chdir('/home/eli/pdi_avancado')

focos_vector_file = "focos/focos-2016.shp"

fshp = gpd.read_file(focos_vector_file) #le o shpe de focos pela biblioteca geopandas

fshp["timestamp"] = pd.to_datetime(fshp["timestamp"]) #transforma em arquivo datetime

fshp_toc09 = fshp[(fshp.estado=='Tocantins') & (fshp.timestamp>='2016-09-01') & (fshp.timestamp<'2016-10-01')] #seleciona focos de Tocatins em setembro/2016

mun_vector_file = "BR/BRMUE250GC_SIR.shp" #shape de municipios do IBGE

mun_shp = gpd.read_file(mun_vector_file) #carrega pelo geopandas

mun_toc = mun_shp[mun_shp.CD_GEOCMU.str[:2] == '17'] #seleciona apenas municipios do Tocatins (inicio do codigo = 17)

toc_join = gpd.sjoin(fshp_toc09, mun_toc, how="right", op='intersects') #associa o ponto do foco do arquivo focos-2016.shp com a geometria dada pelo IBGE e atribui cada foco ao respectivo municipio

toc09_nf=toc_join.groupby('NM_MUNICIP').size() #contagem de focos para cada municipio

toc09_nf = toc09_nf.to_frame(name="nfocos").reset_index() 

toc09_nf_pormun = pd.merge(mun_toc,nfpm, on='NM_MUNICIP',how='right') #junta o numero de focos com a geometria

#plot

f, ax = plt.subplots(1)
nfpms.plot(ax=ax, column='nfocos', scheme='fisher_jenks',k=10, legend=True)# cmap='Reds',
ax.set_title(u'Número de focos de queimada por município')
ax.set_xlim([-52,-42])

