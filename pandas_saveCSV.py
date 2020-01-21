import pandas as pd
import traceback

def onData(instance, args):
  payload = args[0]
  df = payload.data

  if 'filename' not in instance.options:
    instance.throw('No filename specified !')
    return
  
  try:
    df.to_csv(instance.options['filename'], sep=';', index=None, header=True)
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'pandas_savecsv',
  'title': 'Save CSV',
  'author': 'Arthur Chevalier',
  'color': '#1797F0',
  'input': True,
  'icon': 'file-csv',
  'version': '1.0.0',
  'group': 'Pandas',
  'readme': """# Drop NA

  Drop all rows containing NaN in a specified column""",
  'html': """<div class="padding">
	<div class="row">
		<div class="col-md-12">
			<div data-jc="textbox" data-jc-path="filename" data-jc-config="placeholder:/public/robots.txt">Filename</div>
			<div class="help m">Filename relative to the application root.</div>
		</div>
	</div>
</div>""",
  'install': install
}
