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
module: cifs_server_create
version_added: "1.0"
author: "Jeorry Balasabas (@jeorryb)"
short_description: Create CIFS Server
description:
  - Ansible module to create CIFS server on NetApp CDOT arrays via the NetApp python SDK.

requirements: ['NetApp Manageability SDK']

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
      - "name of the vserver"
  cifs_user:
    required: True
    description:
      - "Username of account used to add cifs server to active directory."
  cifs_pass:
    required: True
    description:
      - "Password of account used to add cifs server to active directory."
  cifs_server:
    required: True
    description:
      - "NETBIOS name of the CIFS server."
  domain:
    required: True
    description:
      - ""
  obj_overwrite:
    required: False
    description:
      - "Overwrite AD Computer Object if it already exists"
'''

EXAMPLES = '''
# Create CIFS Service
- name: Create CIFS Service
    cifs_service_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      vserver: "svm_cifs"
      cifs_user: "admin@testdomain.com"
      cifs_pass: "Password123"
      cifs_server: "svmcifs"
      domain: "testdomain.com"

'''

def cifs_service_create(module):

  cluster = module.params['cluster']
  user_name = module.params['user_name']
  password = module.params['password']
  vserver = module.params['vserver']
  cifs_server = module.params['cifs_server']
  cifs_user = module.params['cifs_user']
  cifs_pass = module.params['cifs_pass']
  domain = module.params['domain']
  obj_overwrite = module.params['obj_overwrite']

  results = {}

  results['changed'] = False

  api = NaElement("cifs-server-create")
  api.child_add_string("admin-username", cifs_user)
  api.child_add_string("admin-password", cifs_pass)
  api.child_add_string("cifs-server", cifs_server)
  api.child_add_string("domain", domain)
  api.child_add_string("force-account-overwrite", obj_overwrite)

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
    argument_spec.update(dict(
        cluster=dict(required=True),
        user_name=dict(required=True),
        password=dict(required=True),
        vserver=dict(required=True),
        cifs_user=dict(required=True),
        cifs_pass=dict(required=True),
        cifs_server=dict(required=True),
        domain=dict(required=True),
        obj_overwrite=dict(required=False, default=True),))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    results = cifs_service_create(module)
    module.exit_json(**results)


from ansible.module_utils.basic import *
main()