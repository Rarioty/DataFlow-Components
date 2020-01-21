import pandas as pd
import traceback

def onData(instance, args):
  try:
    payload = args[0]
    df = payload.data

    if 'filter' not in instance.options:
      instance.send(df)
      return

    if ';' in instance.options['filter']:
      columns = instance.options['filter'].split(';')
    else:
      columns = [instance.options['filter']]

    df = df[columns]

    instance.send(df)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'pandas_filtercolumns',
  'title': 'Filter Columns',
  'author': 'Arthur Chevalier',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'file-csv',
  'version': '1.0.0',
  'group': 'Pandas',
  'readme': """# Filter Column

  Filter Columns of a DataFrame""",
  'html': """<div class="padding">
  <div class="row">
    <div class="col-md-6">
      <div data-jc="textbox" data-jc-path="filter" data-jc-config="placeholder:toto;tutu;tata">Filename</div>
      <div class="help m">Columns to keep separated by semi-column</div>
    </div>
  </div>
</div>""",
  'install': install
}
