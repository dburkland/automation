#!/usr/bin/python

import sys
import json
from  ansible.module_utils import ntap_util

try:
    from NaServer import *
    NASERVER_AVAILABLE = True
except ImportError:
    NASERVER_AVAILABLE = False

if not NASERVER_AVAILABLE:
    module.fail_json(msg="The NetApp Manageability SDK library is not installed")

DOCUMENTATTION = '''
---
module: dns_create
version_added: "1.0"
author: "Dan Burkland (@dburkland)"
short_description: Set date, time and timezone for NetApp cDOT array.
description:
  - Ansible module to create dns server entries for a NetApp CDOT array via the NetApp python SDK.
requirements:
  - NetApp Manageability SDK
options:
  cluster:
    required: True
    description:
      - "The ip address or hostname of the cluster"
  user_name:
    required: True
    description:
      - "Administrator user for the cluster/node"
  password:
    required: True
    description:
      - "password for the admin user"
  vserver:
    required: True
    description:
      - "vserver that DNS entries are being created on"
  domains:
    required: True
    description:
      - "Comma separated list of domains (FQDN) that the servers are responsible for"
  dns_servers:
    required: True
    description:
      - "Comma separated list of dns servers"
  skip_config_validation:
    required: True
    description:
      - "True/False to skip DNS check"

'''

EXAMPLES = '''
# Create DNS servers for cluster vserver
- name: Create dns servers
    dns_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      vserver: "atlcdot"
      domains: "netapp.com"
      dns_servers: "8.8.8.8, 4.2.2.2"
      skip_config_validation: true

'''

def dns_create(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  vserver = module.params['vserver']
  domains = module.params['domains']
  dns_servers = module.params['dns_servers']
  skip_config_validation = module.params['skip_config_validation']

  results = {}

  results['changed'] = False

  api = NaElement("net-dns-create")
#  api.child_add_string("domains", domains)
#  api.child_add_string("name-servers", dns_servers)
  api.child_add_string("skip-config-validation", skip_config_validation)

  xi = NaElement('domains')
  api.child_add(xi)
  if module.params['domains']:
    for domain in domains:
      xi.child_add_string('string', domain)
  xi1 = NaElement('name-servers')
  api.child_add(xi1)
  if module.params['dns_servers']:
    for dns_server in dns_servers:
      xi1.child_add_string('ip-address', dns_server)

  connection = ntap_util.connect_to_api_svm(module, vserver=vserver)
  xo = connection.invoke_elem(api)

  if(xo.results_errno() != 0):
    r = xo.results_reason()
    module.fail_json(msg=r)
    results['changed'] = False

  else:
    results['changed'] = True

  return results

def main():

    argument_spec = ntap_util.ntap_argument_spec()
    #argument_spec.update(dict(
    argument_spec.update(dict(
        cluster=dict(required=True),
        user_name=dict(required=True),
        password=dict(required=True),
        vserver=dict(required=True),
        domains=dict(required=True, type='list'),
        dns_servers=dict(required=True, type='list'),
        skip_config_validation=dict(required=True),))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    results = dns_create(module)
    module.exit_json(**results)

from ansible.module_utils.basic import *
main()