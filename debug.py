import traceback
import logging

def onData(instance, args):
  if instance.options['enabled']:
    opt = instance.options
    payload = args[0]
    val = payload.data
    id = payload.id
    group = opt['group'] if 'group' in opt else None

    if opt['type'] == 'both':
      logging.debug('DEBUG[%s]: %s' % (instance.id, val))
      instance.debug(val, None, group, id)
    elif opt['type'] == 'logs':
      logging.debug('DEBUG[%s]: %s' % (instance.id, val))
    else:
      instance.debug(val, None, group, id)

def onOptions(instance, *args):
  instance.custom['status']()

def onClick(instance, *args):
  instance.options['enabled'] = not instance.options['enabled']
  customStatus(instance)
  instance.flow.save()

def customStatus(instance):
  instance.status('Enabled' if instance.options['enabled'] else 'Disabled')

def install(instance):
  instance.custom['status'] = (lambda: customStatus(instance))
  instance.on('options', onOptions)
  instance.on('click', onClick)
  instance.on('data', onData)

  customStatus(instance)

EXPORTS = {
  'id': 'debug',
  'title': 'Debug',
  'author': 'Arthur Chevalier',
  'color': '#967ADC',
  'click': True,
  'input': True,
  'icon': 'bug',
  'version': '2.0.3',
  'options': {
    'enabled': True,
    'repository': False,
    'type': 'data'
  },
  'readme': """# Debug

  Prints data to the debug tab.""",
  'html': """<div class="padding">
    <div class="row">
      <div class="col-md-12">
        <div data-jc="dropdown" data-jc-path="type" data-jc-config="items:Message data|data,App logs|logs,Message data + App logs|both;required:true" class="m">Output type</div>
        <div data-jc="textbox" data-jc-path="property" data-jc-config="placeholder: e.g. address.street" class="m">Path to the property (leave empty to show the whole data object)</div>
        <div data-jc="textbox" data-jc-path="group" data-jc-config="placeholder: e.g. Temperature" class="m">A group name</div>
        <div data-jc="checkbox" data-jc-path="enabled">Enabled</div>
      </div>
    </div>
  </div>""",
  'install': install
}