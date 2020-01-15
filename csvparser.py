from io import StringIO
import pandas as pd

def onData(instance, args):
  payload = args[0]
  text = payload.data

  data = StringIO(text)

  df = pd.read_csv(data, sep=';')

  instance.send(df)

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'csvparser',
  'title': 'CSV Parser',
  'author': 'Arthur Chevalier',
  'color': '#1797F0',
  'input': True,
  'output': True,
  'icon': 'file-csv',
  'version': '1.0.0',
  'group': 'Pandas',
  'readme': """# CSV Parser

  Transform input text data to CSV dataframe (pandas)""",
  'html': """<div class="padding">
    <div class="row">
    </div>
  </div>""",
  'install': install
}
