from bokeh.plotting import figure, output_file, show

from git import Repo
import sqlite3, sys
from datetime import datetime, date
from dateutil import parser

import numpy as np
import pandas as pd

from bokeh.plotting import *
from numpy import pi

from bokeh.models import ColumnDataSource, LabelSet
import colorsys

import matplotlib.pyplot as plt

# config file
import config

# local functions for sqlite operations on db
import functions_for_sql

# initializations
tab = config.table_in_db
repo = Repo(config.repo_path)

fig_folder = config.fig_folder

conn = sqlite3.connect(config.db_filename)
cursor = conn.cursor()

import webcolors

def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]

def get_colour_name(requested_colour):
    try:
        closest_name = actual_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
        actual_name = None
#    return actual_name, closest_name
    return closest_name

def plot_pie(labels, data, title=None, colors=[]):
  plot_height=200; plot_width=200
  TOOLS = "hover,pan,wheel_zoom,box_zoom,reset,save"

  N = len(data)
  
  if colors == []:
    HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
    RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)
    colors = ((255*np.array(RGB_tuples)).astype('int')).tolist()
    colors = [get_colour_name(x) for x in colors]
  if len(labels) != len(colors):
    print 'problema aqui, num de autores diferente do numero de cores.'

  data = np.array(data, dtype='float')
  # normalizar
  data = data/data.sum()
  
  labels_data = zip(labels, data)
  labels_data.sort(key=lambda x:x[1])
  labels_data = np.array(labels_data)
  
  labels = labels_data.T[0]
  percents = np.cumsum(labels_data.T[1].astype('float'))
  
  print labels, percents
  
  # define starts/ends for wedges from percentages of a circle
  starts = [p*2*pi for p in np.hstack((np.array([0]),percents[:-1].astype('float')))]
  ends = [p*2*pi for p in np.hstack((percents[1:].astype('float'), np.array([1])))]

  p = figure(plot_height=plot_height, plot_width=plot_width, tools=TOOLS, x_range=(-1.1,1.1), y_range=(-1.1,1.1), title=title)

  p.wedge(x=0, y=0, radius=1, start_angle=starts, end_angle=ends, color=colors)

  # display/save everything  
  output_file("pie.html")
  show(p)

## inicializando as cores pra cada autor ##
lst_colors = config.lst_colors

a = cursor.execute('SELECT DISTINCT autor FROM '+tab) # capturando os diferentes autores
autores = np.array(a.fetchall())[:,0].tolist()
print autores

d_autores_cor = {}
for i, autor in enumerate(autores):
  d_autores_cor[autor] = lst_colors[i]
##

# prj global statistics

a = cursor.execute(functions_for_sql.select_(tab, ['criado_em', 'insertions', 'deletions'], order='criado_em'))
b = np.array(a.fetchall())

insertions = b[:,1].astype('int').cumsum()
deletions = b[:,2].astype('int').cumsum()
size = insertions - deletions
criado = b[:,0].copy()

df = pd.DataFrame()

x = [parser.parse(d) for d in criado]  

df['datetime'] = x
df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
df['insert'] = b[:,1].astype('int').copy()
df['delet'] = b[:,2].astype('int').copy()
df['size'] = size.copy()

df2 = df.resample('M', on='datetime').mean()
df2['size'].fillna(method='ffill', inplace=True)
df2['insert'].fillna(0, inplace=True)
df2['delet'].fillna(0, inplace=True)
#df2.fillna(0, inplace=True)

x = df2.index.values

leg = list()
line, = plt.plot(x, df2['insert'], 'o-', linewidth=2, label='insertions')
leg.append(line)
line, = plt.plot(x, df2['delet'], 'o-', linewidth=2, label='deletions')
leg.append(line)
line, = plt.plot(x, df2['size'], 'o-', linewidth=2, label='size')
leg.append(line)

plt.legend(handles=leg)
plt.ylabel('Statistics by month')
plt.xlabel('Time (month)')
plt.savefig(fig_folder+'/global_stats_by_month.png', dpi=180)

#sys.exit(0)

##

# count number of commits for each author
autores_ = list()
n_commits_ = list()
n_insertions_ = list()
n_deletions_ = list()
colors_ = list()
for i, autor in enumerate(autores):
  a = cursor.execute(functions_for_sql.select_where_(tab, ['criado_em', 'insertions', 'deletions'], ['autor', autor]))
  b = np.array(a.fetchall())
  
  autores_.append(autor)
  n_commits_.append(b.size)
  n_insertions_.append(b[:,1].astype('int').sum())
  n_deletions_.append(b[:,2].astype('int').sum())
  colors_.append(d_autores_cor[autor])
#plot_pie(autores_, n_commits_, title='Numero de commits por autor', colors=colors_)
# plotar histograma
plt.clf()
y_pos = np.arange(len(autores_))
plt.bar(y_pos, n_commits_)
plt.xticks(y_pos, autores_)
#for i in range(len(autores_)):
#  plt.text(x = r4[i]-0.5 , y = n_commits_[i]+0.1, s = [], size = 6)
plt.ylabel('# of commits')
#plt.show()
plt.savefig(fig_folder+'/n_commits_all.png')

plt.clf()
y_pos = np.arange(len(autores_))
plt.bar(y_pos, n_insertions_)
plt.xticks(y_pos, autores_)
#for i in range(len(autores_)):
#  plt.text(x = r4[i]-0.5 , y = n_commits_[i]+0.1, s = [], size = 6)
plt.ylabel('# of insertions')
#plt.show()
plt.savefig(fig_folder+'/n_insertions_all.png')

plt.clf()
y_pos = np.arange(len(autores_))
plt.bar(y_pos, n_deletions_)
plt.xticks(y_pos, autores_)
#for i in range(len(autores_)):
#  plt.text(x = r4[i]-0.5 , y = n_commits_[i]+0.1, s = [], size = 6)
plt.ylabel('# of deletions')
#plt.show()
plt.savefig(fig_folder+'/n_deletions_all.png')


'''
# count number of insertions for each author
autores_ = list()
n_insertions_ = list()
colors_ = list()
for i, autor in enumerate(autores):
  a = cursor.execute(functions_for_sql.select_where_(tab, ['criado_em', 'insertions'], ['autor', autor]))
  b = np.array(a.fetchall())
  
  autores_.append(autor)
  n_insertions_.append(b[:,1].astype('int').sum())
  colors_.append(d_autores_cor[autor])
plot_pie(autores_, n_insertions_, title='Numero de insercoes por autor', colors=colors_)
'''

# create a new plot with a title and axis labels
plt.clf()
plt.figure(figsize=(12,7))
leg = list()
for autor in autores:
  a = cursor.execute(functions_for_sql.select_where_(tab, ['criado_em', 'insertions'], ['autor', autor]))
  b = np.array(a.fetchall())

  x = [parser.parse(d) for d in b[:,0]]
  y = b[:,1]

  # add a line renderer with legend and line thickness
  line, = plt.plot(x, y, 'o-', linewidth=2, color=d_autores_cor[autor], label=autor)
  leg.append(line)
plt.legend(handles=leg)
plt.ylabel('Insertions')
plt.xlabel('Time')
plt.savefig(fig_folder+'/insertions_time_series.png', dpi=180)


# create a new plot with a title and axis labels
plt.clf()
plt.figure(figsize=(12,7))
leg = list()
for autor in autores:
  df = pd.DataFrame()
  a = cursor.execute(functions_for_sql.select_where_(tab, ['criado_em', 'insertions'], ['autor', autor]))
  b = np.array(a.fetchall())

  x = [parser.parse(d) for d in b[:,0]]  
  y = b[:,1].astype('int')
  
  df['datetime'] = x
  df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
  #df.index = df['datetime'] 
  df['y'] = y
  
  
  df2 = df.resample('M', on='datetime').sum()
  df2.fillna(0, inplace=True)
  y = df2.y.as_matrix()

  x = df2.index.values

  line, = plt.plot(x, y, 'o-', linewidth=2, color=d_autores_cor[autor], label=autor)
  leg.append(line)
plt.legend(handles=leg)
plt.ylabel('Insertions by month')
plt.xlabel('Time (month)')
plt.savefig(fig_folder+'/insertions_time_series_by_month.png', dpi=180)


##
plt.clf()
plt.figure(figsize=(12,7))
leg = list()
for autor in autores:
  df = pd.DataFrame()
  a = cursor.execute(functions_for_sql.select_where_(tab, ['criado_em', 'insertions'], ['autor', autor]))
  b = np.array(a.fetchall())

  x = [parser.parse(d) for d in b[:,0]]  
  y = b[:,1].astype('int')
  
  df['datetime'] = x
  df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
  #df.index = df['datetime'] 
  df['y'] = y
  
  
  df2 = df.resample('W', on='datetime').sum()
  df2.fillna(0, inplace=True)
  y = df2.y.as_matrix()

  x = df2.index.values

  line, = plt.plot(x, y, 'o-', linewidth=2, color=d_autores_cor[autor], label=autor)
  leg.append(line)
plt.legend(handles=leg)
plt.ylabel('Insertions by week')
plt.xlabel('Time (week)')
plt.savefig(fig_folder+'/insertions_time_series_by_week.png', dpi=180)

##
plt.clf()
plt.figure(figsize=(12,7))
leg = list()
for autor in autores:
  df = pd.DataFrame()
  a = cursor.execute(functions_for_sql.select_where_(tab, ['criado_em', 'insertions'], ['autor', autor]))
  b = np.array(a.fetchall())

  x = [parser.parse(d) for d in b[:,0]]  
  y = b[:,1].astype('int')
  
  df['datetime'] = x
  df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
  #df.index = df['datetime'] 
  df['y'] = y
  
  
  df2 = df.resample('2W', on='datetime').sum()
  df2.fillna(0, inplace=True)
  y = df2.y.as_matrix()

  x = df2.index.values

  line, = plt.plot(x, y, 'o-', linewidth=2, color=d_autores_cor[autor], label=autor)
  leg.append(line)
plt.legend(handles=leg)
plt.ylabel('Insertions by 2 weeks')
plt.xlabel('Time (2 weeks)')
plt.savefig(fig_folder+'/insertions_time_series_by_2weeks.png', dpi=180)

##
plt.clf()
plt.figure(figsize=(12,7))
leg = list()
for autor in autores:
  df = pd.DataFrame()
  a = cursor.execute(functions_for_sql.select_where_(tab, ['criado_em', 'insertions', 'deletions'], ['autor', autor]))
  b = np.array(a.fetchall())

  x = [parser.parse(d) for d in b[:,0]]  
  y = b[:,1].astype('int') + b[:,2].astype('int')
  
  df['datetime'] = x
  df['datetime'] = pd.to_datetime(df['datetime'], utc=True)
  #df.index = df['datetime'] 
  df['y'] = y
  
  df2 = df.resample('2W', on='datetime').sum()
  df2.fillna(0, inplace=True)
  y = df2.y.as_matrix()

  x = df2.index.values

  line, = plt.plot(x, y, 'o-', linewidth=2, color=d_autores_cor[autor], label=autor)
  leg.append(line)
plt.legend(handles=leg)
plt.ylabel('Activity by 2 weeks')
plt.xlabel('Time (2 weeks)')
plt.savefig(fig_folder+'/activity_time_series_by_2weeks.png', dpi=180)

sys.exit(0)

'''
SELECT
 trackid,
 name,
 composer,
 unitprice
FROM
 tracks
ORDER BY
 criado_em;
'''

'''
# prepare some data
x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]

# output to static HTML file
output_file("lines.html")

# create a new plot with a title and axis labels
p = figure(title="simple line example", x_axis_label='x', y_axis_label='y')

# add a line renderer with legend and line thickness
p.line(x, y, legend="Temp.", line_width=2)

# show the results
show(p)
'''
