from __future__ import unicode_literals

import os
import sys

import multiprocessing

import gunicorn.app.base

from django.core.management.base import BaseCommand
from django.utils.translation import ugettext as _
from gunicorn import util
from gunicorn.six import iteritems

GUNICORN_SERVER_HELP = r"""
  Run Hue using the Gunicorn WSGI server in asynchronous mode.
"""

GUNICORN_SERVER_OPTIONS = {
  'access_log_format': None,
  'accesslog': '-',
  'args': ['desktop.wsgi:application'],
  'backlog': None,
  'bind': ['0.0.0.0:8088'],
  'ca_certs': None,
  'capture_output': None,
  'cert_reqs': None,
  'certfile': None,
  'chdir': None,
  'check_config': None,
  'ciphers': None,
  'config': None,
  'daemon': None,
  'do_handshake_on_connect': None,
  'enable_stdio_inheritance': None,
  'errorlog': '-',
  'forwarded_allow_ips': None,
  'graceful_timeout': None,
  'group': None,
  'initgroups': None,
  'keepalive': None,
  'keyfile': None,
  'limit_request_field_size': None,
  'limit_request_fields': None,
  'limit_request_line': None,
  'logconfig': None,
  'logger_class': None,
  'loglevel': 'debug',
  'max_requests': None,
  'max_requests_jitter': None,
  'paste': None,
  'pidfile': None,
  'preload_app': None,
  'proc_name': None,
  'proxy_allow_ips': None,
  'proxy_protocol': None,
  'pythonpath': None,
  'raw_env': None,
  'raw_paste_global_conf': None,
  'reload': None,
  'reload_engine': None,
  'sendfile': None,
  'spew': None,
  'ssl_version': None,
  'statsd_host': None,
  'statsd_prefix': None,
  'suppress_ragged_eofs': None,
  'syslog': None,
  'syslog_addr': None,
  'syslog_facility': None,
  'syslog_prefix': None,
  'threads': None,
  'timeout': None,
  'umask': None,
  'user': None,
  'worker_class': 'eventlet',
  'worker_connections': None,
  'worker_tmp_dir': None,
  'workers': 4
}

class Command(BaseCommand):
  help = _("Gunicorn Web server for Hue.")

  def handle(self, *args, **options):
    rungunicornserver()

  def usage(self, subcommand):
    return GUNICORN_SERVER_HELP

def number_of_workers():
  return (multiprocessing.cpu_count() * 2) + 1


def handler_app(environ, start_response):
  """
  response_body = b'Works fine'
  status = '200 OK'

  response_headers = [
    ('Content-Type', 'text/plain'),
  ]

  start_response(status, response_headers)

  return [response_body]"""
  ##from gunicorn.app.wsgiapp import WSGIApplication
  ##return WSGIApplication("%(prog)s [OPTIONS] [APP_MODULE]")
  import os

  os.environ.setdefault("DJANGO_SETTINGS_MODULE", "desktop.settings")
  from django.core.wsgi import get_wsgi_application
  return get_wsgi_application()


class StandaloneApplication(gunicorn.app.base.BaseApplication):

  def __init__(self, app, options=None):
    self.options = options or {}
    # self.application = app
    self.app_uri = 'desktop.wsgi:application'
    super(StandaloneApplication, self).__init__()

  def load_config(self):
    config = dict([(key, value) for key, value in iteritems(self.options)
                    if key in self.cfg.settings and value is not None])
    for key, value in iteritems(config):
      self.cfg.set(key.lower(), value)

  def chdir(self):
    # chdir to the configured path before loading,
    # default is the current dir
    os.chdir(self.cfg.chdir)

    # add the path to sys.path
    sys.path.insert(0, self.cfg.chdir)

  def load_wsgiapp(self):
    self.chdir()

    # load the app
    return util.import_app(self.app_uri)

  def load(self):
    # return self.application
    return self.load_wsgiapp()


def rungunicornserver():
  options = {
      'access_log_format': None,
      'accesslog': '-',
      'args': ['desktop.wsgi:application'],
      'backlog': None,
      'bind': ['0.0.0.0:8088'],
      'ca_certs': None,
      'capture_output': None,
      'cert_reqs': None,
      'certfile': None,
      'chdir': None,
      'check_config': None,
      'ciphers': None,
      'config': None,
      'daemon': None,
      'do_handshake_on_connect': None,
      'enable_stdio_inheritance': None,
      'errorlog': '-',
      'forwarded_allow_ips': None,
      'graceful_timeout': None,
      'group': None,
      'initgroups': None,
      'keepalive': None,
      'keyfile': None,
      'limit_request_field_size': None,
      'limit_request_fields': None,
      'limit_request_line': None,
      'logconfig': None,
      'logger_class': None,
      'loglevel': 'debug',
      'max_requests': None,
      'max_requests_jitter': None,
      'paste': None,
      'pidfile': None,
      'preload_app': None,
      'proc_name': None,
      'proxy_allow_ips': None,
      'proxy_protocol': None,
      'pythonpath': None,
      'raw_env': None,
      'raw_paste_global_conf': None,
      'reload': None,
      'reload_engine': None,
      'sendfile': None,
      'spew': None,
      'ssl_version': None,
      'statsd_host': None,
      'statsd_prefix': None,
      'suppress_ragged_eofs': None,
      'syslog': None,
      'syslog_addr': None,
      'syslog_facility': None,
      'syslog_prefix': None,
      'threads': None,
      'timeout': None,
      'umask': None,
      'user': None,
      'worker_class': 'eventlet',
      'worker_connections': None,
      'worker_tmp_dir': None,
      'workers': 4
  }
  StandaloneApplication(handler_app, options).run()

if __name__ == '__main__':
    rungunicornserver()