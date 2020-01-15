from dateutil.parser import parse as parsedate
from urllib.parse import urlparse
from datetime import datetime
import traceback
import requests
import wget
import time
import os

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def customWgetBar(instance, current, total, width=None):
  instance.status('%02d%% [%s / %s]' % (current / total * 100, sizeof_fmt(current), sizeof_fmt(total)))

def onData(instance, args):
  instance.status('Starting...')

  data = args[0].data
  start = time.process_time()

  try:
    if data is None or not isinstance(data, dict) or 'path' not in data:
      # No correct input
      if not 'url' in instance.options:
        return

      path = instance.options['url']
      enc = instance.options['encoding'] if 'encoding' in instance.options else 'UTF-8'
      targetPath = instance.options['targetPath'] if 'targetPath' in instance.options else os.path.basename(urlparse(path).path)
    else:
      path = data['path']
      enc = data['encoding'] if 'encoding' in data else (instance.options['encoding'] if 'encoding' in instance.options else 'UTF-8')
      targetPath = data['targetPath'] if 'targetPath' in data else (instance.options['targetPath'] if 'targetPath' in instance.options else os.path.basename(urlparse(path).path))

    targetPath = os.path.join('.flow/tmp/.webdownloader', targetPath)
    if not os.path.exists('.flow/tmp'):
      os.mkdir('.flow/tmp')
    if not os.path.exists('.flow/tmp/.webdownloader'):
      os.mkdir('.flow/tmp/.webdownloader')

    # Before downloading the file, check if we don't have it or if the remote file is newer
    skip = False
    instance.status('HEAD request')
    r = requests.head(path)
    if instance.options['debug']:
      instance.debug(r.headers)
    instance.status('HEAD request ended')
    if os.path.exists(targetPath):
      # File exists, check if the remote one is newer
      remoteLastModified = parsedate(r.headers['Last-Modified']) if 'Last-Modified' in r.headers else None
      if remoteLastModified is not None:
        remoteTimezone = remoteLastModified.tzinfo
        localLastModified = datetime.fromtimestamp(os.path.getmtime(targetPath)).replace(tzinfo=remoteTimezone)

        if instance.options['debug']:
          instance.debug('Timezone: ' + str(remoteTimezone))
          instance.debug('Comparing two dates: local [%s] remote [%s]' % (localLastModified, remoteLastModified))

        if remoteLastModified <= localLastModified:
          skip = True
        else:
          os.remove(targetPath)
      else:
        os.remove(targetPath)
    
    # Get file through net then encode it
    if not skip:
      wget.download(path, out=targetPath, bar=lambda c, t, w: customWgetBar(instance, c, t, w))

      currentEncoding = r.headers['Content-Type'].split('charset=')[1] if 'Content-Type' in r.headers and 'charset=' in r.headers['Content-Type'] else enc
      if currentEncoding.capitalize() != enc.capitalize():
        instance.status('Converting encoding')
        with open(targetPath, 'r', encoding=currentEncoding) as file:
          data = file.read()
          file.close()

          with open(targetPath, 'w', encoding='UTF-8') as file2:
            file2.write(data)
            file.close()
    else:
      instance.status('Using cache')

    end = time.process_time()
    delta = (end - start) * 1000.0 # In ms
    instance.flow.updateTraffic(instance.id, 'duration', delta)
    
    instance.send({
      'path': targetPath,
      'encoding': 'UTF-8'
    })
  except Exception as e:
    instance.throw(str(e) + '\n' + str(traceback.format_exc()))

def install(instance):
  instance.on('data', onData)

EXPORTS = {
  'id': 'webdownloader',
  'title': 'Web Downloader',
  'author': 'Arthur Chevalier',
  'color': '#989D78',
  'output': 1,
  'input': 1,
  'icon': 'globe',
  'version': '1.0.0',
  'group': 'Inputs',
  'options': {
    'URL': '',
    'append': True,
    'delimiter': '\\n'
  },
  'readme': """# Web File Reader

This component reads a file from a given URL then convert the encoding to UTF-8.

## Input
If incomming object has a path property then filename option is replaced.

Example of incomming object
\`\`\`javascript
{
	path: 'https://example.com/file',
	targetPath: 'toto.txt', // optional, default text
	encoding: 'utf8' // optional, default utf8
}
\`\`\`
""",
  'html': """<div class="padding">
	<div class="row">
		<div class="col-md-6">
			<div data-jc="textbox" data-jc-path="url" data-jc-config="placeholder:https://example.com/file">Filename</div>
			<div class="help m">URL of file</div>
		</div>
	</div>
	<div class="row">
		<div class="col-md-6">
			<div data-jc="textbox" data-jc-path="targetPath" data-jc-config="placeholder:toto.txt">Save as:</div>
		</div>
		<div class="col-md-6">
			<div data-jc="textbox" data-jc-path="encoding" data-jc-config="placeholder:utf8">Encoding (default 'utf8')</div>
			<div class="help m">Only for 'Read as text'</div>
		</div>
	</div>
</div>""",
  'install': install
}
