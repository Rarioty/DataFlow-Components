import pandas as pd
import traceback

def onData(instance, args):
  try:
    payload = args[0]
    df = payload.data

    index = payload.toIdx

    if 'dataframes' not in instance.custom:
      instance.custom['dataframes'] = {}

    if index not in instance.custom['dataframes']:
      instance.custom['dataframes'][index] = None
    instance.custom['dataframes'][index] = df

    nbReceived = len([y for y in instance.custom['dataframes'].values() if y is not None])
    instance.status('%d/2 received' % (nbReceived,))

    if nbReceived == 2:
      instance.status('Merging')
      df = pd.concat(instance.custom['dataframes'].values())

      instance.send(df)

      instance.status('Resetting')
      instance.custom['dataframes'] = {}
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

  instance.status('0/2 received')

EXPORTS = {
  'id': 'pandas_mergedf',
  'title': 'Merge Dataframes',
  'author': 'Arthur Chevalier',
  'color': '#1797F0',
  'input': 2,
  'output': True,
  'icon': 'file-csv',
  'version': '1.0.0',
  'group': 'Pandas',
  'readme': """# Merge Dataframes

  Merge two dataframes to a unique one""",
  'html': """<div class="padding">
	<div class="row">
	</div>
</div>""",
  'install': install
}
