#!/usr/bin/env python

if __name__ == "__main__":
  from ownSyncUtils import *
  import argparse, sys, getpass
  from argparse import RawTextHelpFormatter
  if len(sys.argv) <=1:
    sys.argv.append("--help")
  else:
    sys.argv.pop(0)

  t = "type of sync to do. (Default: both)\nThe options are:\n\tto   - Local is seen as the master repo, everything remote is replaced, updated or deleted from.\n\tfrom - Remote is seen as the master repo, everything local will be replaces, updated or deleted till it looks exactly like whats on the server.\n\tboth - Local and Remote paths are compared and merged.  The newest file will be used in both places."
  parser = argparse.ArgumentParser(description='Command line tool used to sync your ownCloud files to and from local directory', formatter_class=RawTextHelpFormatter)
  parser.add_argument('--url', help='url to use to connect to ownCloud (IE https://myCloud.com/owncloud/)', type=str, required=True)
  parser.add_argument('--user', help='Username to use to connect', type=str, required=True)
  parser.add_argument('--pass', help='Password to use to connect (will be prompted if omitted)', type=str, default=None)
  parser.add_argument('--local', help='local path to sync into', type=str, required=True)
  parser.add_argument('--rpath', help='remote path to sync into (Default: /)', type=str, required=False, default = "/")
  parser.add_argument('--disable-ssl', action=store_true, default=False, help="Don't check TLS/SSL certs (warning: dumb)")
  parser.add_argument('--type', default='both', help=t, required=False)
  Args = vars(parser.parse_args(sys.argv))

  print "Checking URL...  ",
  Args['url'] = getOwn(Args['url'])
  if Args['url'] == None:
    print "Problem with URL!"
    sys.exit(1)
  else:
    print "GOOD: %s"%(Args['url'])

  if Args['pass'] is None:
    Args['pass'] = getpass.getpass("Password: ")

  logging.basicConfig(format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
  log = logging.getLogger("root")
  log.setLevel(logging.DEBUG)

  X = ownClient(Args['url'], disable_ssl=Args['disable-ssl'])
  X.set_auth(Args['user'], Args['pass'])

  {
    'both': X.syncBOTH,
    'to': X.syncTO,
    'from': X.syncFROM
  }[Args['type'].lower()](Args['local'], base=Args['rpath'])
