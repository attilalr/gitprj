#coding=utf-8

# script para pegar as informações dos commits de um repositorio

from git import Repo
import sqlite3, sys
from datetime import datetime, date
from functions_for_sql import sql_cmds_fields

output_db = 'rep.db'

tab = 'commits'

repo = Repo('./Projeto_versionamento_geostat')

#repo.remotes.origin.refs
#hexshas = g.log('--all', '--pretty=%H','--follow','--',filename).split('\n') 

'''
for commit in repo.iter_commits():
  print commit
'''
'''
>>> print c.stats.total
{'deletions': 0, 'lines': 1, 'insertions': 1, 'files': 1}
'''
'''
>>> comm.hexsha
u'85c9d97b73e1337096cdf6b49512c8d9141c1cd7'
'''
'''
>>> c.committed_datetime
datetime.datetime(2018, 8, 20, 10, 55, 3, tzinfo=<git.objects.util.tzoffset object at 0x7f1e889d8790>)
>>> print c.committed_datetime
2018-08-20 10:55:03-03:00
'''
'''
UPDATE commits
SET nota = 10
WHERE hash = '4b5d57bfaffa14097d1c2e6422414ce7d9e55c23';
'''

lst_fields_names = [
  'id',
  'hash',
  'branch',
  'commiter',
  'autor',
  'criado_em',
  'commit_em',
  'nota',
  'mensagem',
  'insertions',
  'deletions',
  'tag',
  ]

lst_fields_types = [
  'INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT',
  'TEXT NOT NULL',
  'TEXT NOT NULL',
  'TEXT NOT NULL',
  'TEXT NOT NULL',
  'DATETIME NOT NULL',
  'DATETIME NOT NULL',
  'INTEGER',
  'TEXT NOT NULL',
  'INTEGER',
  'INTEGER',
  'TEXT NOT NULL',
  ]

if len(lst_fields_names) != len(lst_fields_types):
  print 'problemas nas listas de campos. saindo do script...'
  sys.exit(0)

# obj
fields_obj = sql_cmds_fields()
# adicionando as colunas
for f,t in zip(lst_fields_names, lst_fields_types):
  fields_obj.add_field(f, t)
print 'Definida tabela '+tab+':'
print fields_obj  
  

conn = sqlite3.connect(output_db)
cursor = conn.cursor()

# apagando a tabela anterior
try:
  cursor.execute('DROP TABLE '+tab+';')
except:
  print 'Tabela '+tab+' nao existe para ser apagada.'

print fields_obj.create_table_str(tab)
try:
  cursor.execute(fields_obj.create_table_str(tab))
except:
  print 'Tabela ja existe.'

for id_, commit in enumerate(repo.iter_commits('--all')):

  # primeiro achar o branch
  branch_str = commit.name_rev
  if '/' in branch_str:
    branch_str = branch_str.split('/')[-1]
    if '~' in branch_str:
      branch_str = branch_str.split('~')[0]
    if '^' in branch_str:
      branch_str = branch_str.split('^')[0]
  else:
    branch_str = branch_str.split(' ')[-1]
    if '~' in branch_str:
      branch_str = branch_str.split('~')[0]
    if '^' in branch_str:
      branch_str = branch_str.split('^')[0]

#  if id_==9:
#    sys.exit(0)

  string_exec = "INSERT INTO commits ("+', '.join(lst_fields_names[1:])+") VALUES ("
  string_exec = string_exec + '"' + str(commit.hexsha) + '", ' # hash
#  string_exec = string_exec + '"' + str('master') + '", ' # hash
  string_exec = string_exec + '"' + branch_str + '", ' # hash
#  string_exec = string_exec + '"' + str(commit.committer.name.encode('utf-8')) + '", ' # autor
  string_exec = string_exec + '"' + unicode(commit.committer.name) + '", ' # commiter
  string_exec = string_exec + '"' + unicode(commit.author.name) + '", ' # author
  string_exec = string_exec + '"' + str(commit.committed_datetime) + '", ' # criado datetime
  string_exec = string_exec + '"' + str(commit.committed_datetime) + '", ' # committed datetime
  string_exec = string_exec + '"' + str(-1) + '", ' # nota
  string_exec = string_exec + '"' + (commit.message) + '", ' # msg
  string_exec = string_exec + '"' + str(commit.stats.total['insertions']) + '", ' # insertions
  string_exec = string_exec + '"' + str(commit.stats.total['deletions']) + '",' # deletions
  string_exec = string_exec + '"' + str(-1) + '" ' # tag
  
  string_exec = string_exec + ')'
  
  cursor.execute(string_exec)
  
  #cursor.execute("INSERT INTO commits ("+', '.join(lst_fields_names)+") VALUES "+', '.join(['{'+x+'_}' for x  in lst_fields_names])+"".format(hash_='"'+str(commit.hexsha)+'"', branch_='"master"', autor_='"'+commit.committer.name.encode('utf-8')+'"', criado_em_='"'+str(commit.committed_datetime)+'"', commit_em_='"'+str(commit.committed_datetime)+'"', message_='"'+commit.message+'"')
#  cursor.execute("INSERT INTO commits ("hash, branch, autor, criado_em, commit_em, mensagem") VALUES ({hash_}, {branch}, {autor}, {criado_em}, {commit_em}, {message})".format(hash_='"'+str(commit.hexsha)+'"', branch='"master"', autor='"'+commit.committer.name.encode('utf-8')+'"', criado_em='"'+str(commit.committed_datetime)+'"', commit_em='"'+str(commit.committed_datetime)+'"', message='"'+commit.message+'"'))

conn.commit()
conn.close()

