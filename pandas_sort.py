import pandas as pd
import traceback

def onData(instance, args):
  try:
    payload = args[0]
    df = payload.data

    if 'sort' not in instance.options:
      instance.send(df)
      return
    
    if ';' in instance.options['sort']:
      options = instance.options['sort'].split(';')
    else:
      options = [instance.options['sort']]
    sortingColumns = []
    sortingOrder = []
    toRemove = []

    for opt in options:
      if ',' not in opt:
        tmp = [opt, True]
      else:
        tmp = opt.split(',')
      
      sortingColumns.append(tmp[0] + '.Lower')
      if tmp[1].lower() == 'asc':
        sortingOrder.append(True)
      else:
        sortingOrder.append(False)

      df[tmp[0] + '.Lower'] = df[tmp[0]].str.lower()
      toRemove.append(tmp[0] + '.Lower')

    if 'debug' in instance.options and instance.options['debug']:
      instance.debug("%s - %s" % (sortingColumns, sortingOrder))
    df = df.sort_values(by=sortingColumns, ascending=sortingOrder, na_position='first')
    
    for r in toRemove:
      del df[r]

    instance.send(df)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'pandas_sort',
  'title': 'Sort Dataframe',
  'author': 'Arthur Chevalier',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'file-csv',
  'version': '1.0.0',
  'group': 'Pandas',
  'readme': """# Sort Dataframes

  Sort a Dataframe""",
  'html': """<div class="padding">
  <div class="row">
    <div class="col-md-6">
      <div data-jc="textbox" data-jc-path="sort" data-jc-config="placeholder:toto,asc;tutu,desc;tata,asc">Filename</div>
      <div class="help m">Sorting columns. Dataframe will be sort with these columns and by order.</div>
    </div>
  </div>
</div>""",
  'install': install
}
