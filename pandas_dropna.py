import pandas as pd
import traceback

def onData(instance, args):
  payload = args[0]
  df = payload.data

  if 'columns' not in instance.options:
    instance.throw('No columns specified !')
    return
  
  try:
    columns = instance.options['columns'].split(';')

    df = df.dropna(subset=columns)

    instance.send(df)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'pandas_dropna',
  'title': 'Drop NA',
  'author': 'Arthur Chevalier',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'file-csv',
  'version': '1.0.0',
  'group': 'Pandas',
  'readme': """# Drop NA

  Drop all rows containing NaN in a specified column""",
  'html': """<div class="padding">
	<div class="row">
		<div class="col-md-12">
			<div data-jc="textbox" data-jc-path="columns" data-jc-config="placeholder:toto;tata;tutu">Columns</div>
			<div class="help m">Columns where to search NaN (semi-colon separated).</div>
		</div>
	</div>
</div>""",
  'install': install
}
