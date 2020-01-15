import logging
import json

def onClick(instance, *args):
  instance.send(instance.custom['value'])

def onOptions(instance, *args):
  if 'datatype' not in instance.options:
    instance.custom['value'] == ''
  elif instance.options['datatype'] == 'integer':
    instance.custom['value'] = int(instance.options['data'])
  elif instance.options['datatype'] == 'float':
    instance.custom['value'] == float(instance.options['data'])
  elif instance.options['datatype'] == 'boolean':
    instance.custom['value'] == bool(instance.options['data'])
  elif instance.options['datatype'] == 'object':
    try:
      instance.custom['value'] = json.loads(instance.options['data'])
    except Exception as e:
      instance.error(str(e))
      return
  elif instance.options['datatype'] == 'string':
    instance.custom['value'] = instance.options['data']
  else:
    instance.custom['value'] = ''

def install(instance):
  instance.custom['value'] = None

  instance.on('click', onClick)
  instance.on('options', onOptions)

  onOptions(instance)

EXPORTS = {
  'id': 'trigger',
  'title': 'Trigger',
  'author': 'Arthur Chevalier',
  'color': '#F6BB42',
  'click': True,
  'output': 1,
  'icon': 'play',
  'version': '1.1.0',
  'readme': """# Trigger

- Clicking on the component starts the chain
- Settings allows to set a data-type and a value""",
  'html': """<div class="padding">
	<div data-jc="dropdown__datatype__items:,String|string,Integer|integer,Float|float,Boolean|boolean,Date|date,Object|object,Base64 as Buffer|buffer" class="m">Data type (String by default)</div>
	<div data-jc="textbox__data__placeholder:e.g. Hello world or { hello: 'world'} or ['hello', 'world'])" class="m">Data</div>
	<div data-jc="checkbox__restart">Trigger 5s after initialization.</div>
	<div class="help">Useful when there's a need to run certain flow when the app restarts, etc.</div>
</div>""",
  'install': install
}
