class sql_cmds_fields:
  fields = list()

  def clean(self):
    self.fields = list()
    
  def add_field(self, name, type_):
    self.fields.append({'field': name, 'type': type_})
  
  def show_fields(self):
    print self.fields
    
  def create_table_str(self, table_name):
    string = 'CREATE TABLE '+table_name+ ' (\n '
    for i, field_d in enumerate(self.fields):
      if i<len(self.fields)-1:
        string = string + field_d['field']+' '+field_d['type'] + ',\n '
      else:
        string = string + field_d['field']+' '+field_d['type'] + '\n'
    string = string + ');'
    return string
    
  def __str__(self):
    string = ''
    for i, field_d in enumerate(self.fields):
      if i<len(self.fields)-1:
        string = string + field_d['field']+' '+field_d['type'] + ',\n'
      else:
        string = string + field_d['field']+' '+field_d['type'] + '\n'
    return string

def select_(tab, lst_fields, order=None):
  string = 'SELECT '
  for i, f in enumerate(lst_fields):
    if i<len(lst_fields)-1:
      string = string + f + ', '
    else:
      string = string + f + ' '
  if order:
    string = string + 'FROM ' + tab + ' '
  else:
    string = string + 'FROM ' + tab + ';'
  if order:
    string = string + 'ORDER BY ' + order + ';'
  return string

def select_where_(tab, lst_fields, lst_where_field_key, order=None):
  string = 'SELECT '
  for i, f in enumerate(lst_fields):
    if i<len(lst_fields)-1:
      string = string + f + ', '
    else:
      string = string + f + ' '
  string = string + 'FROM ' + tab + ' '
  if order:
    string = string + 'WHERE ' + lst_where_field_key[0] + '="'+lst_where_field_key[1]+'" '
  else:
    string = string + 'WHERE ' + lst_where_field_key[0] + '="'+lst_where_field_key[1]+'";'
  if order:
    string = string + 'ORDER BY ' + order + ';'
  return string

