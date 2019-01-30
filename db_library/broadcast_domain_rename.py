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
module: broadcast_domain_rename
version_added: "1.0"
author: "Dan Burkland (@dburkland)"
short_description: Rename NetApp Broadcast Domain
description:
  - Ansible module to rename NetApp CDOT Broadcast Domains via the NetApp python SDK.
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
	val_certs:
    default: True
    description:
      - "Perform SSL certificate validation"
  bc_domain:
    required: True
    description:
      - "Name of the broadcast domain you want to rename"
  new_bc_domain:
    required: True
    description:
      - "New name for the broadcast domain"
'''

EXAMPLES = '''
# Rename broadcast domain
- name: Rename broadcast domain
    broadcast_domain_rename:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      bc_domain: "Default"
      new_bc_domain: "Default_0"

'''

def broadcast_domain_rename(module):

    bc_domain = module.params['bc_domain']
    new_bc_domain = module.params['new_bc_domain']

    results = {}
    results['changed'] = False

    api = NaElement("net-port-broadcast-domain-rename")
    api.child_add_string("broadcast-domain", bc_domain)
    api.child_add_string("new-name", new_bc_domain)
    connection = ntap_util.connect_to_api(module)
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
    argument_spec.update(dict(
        bc_domain=dict(required=True),
        new_bc_domain=dict(required=True),))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    results = broadcast_domain_rename(module)

    module.exit_json(**results)

from ansible.module_utils.basic import *
main()




