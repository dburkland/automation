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
module: route_create
version_added: "1.0"
author: "Dan Burkland (@dburkland)"
short_description: Create interface
description:
  - Ansible module to create interfaces on NetApp CDOT arrays via the NetApp python SDK.
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
      - "vserver name"
  destination:
    required: True
    description:
      - "Destination of the route"
  gateway:
    required: True
    description:
      - "Gateway of the route"
  metric:
    required: False
    description:
      - "Metric of the route"
'''

EXAMPLES = '''
# Create default route pointing to the 192.168.1.1 gateway for the "test" SVM
- name: Create route
    route_create:
      cluster: "192.168.0.1"
      user_name: "admin"
      password: "Password1"
      vserver: "svm_nfs"
      destination: "0.0.0.0/0"
      gateway: "192.168.1.1"
      metric: "20"
'''

def route_create(module):

    destination = module.params['destination']
    gateway = module.params['gateway']
    metric = module.params['metric']
    vserver = module.params['vserver']

    results = {}
    results['changed'] = False

    api = NaElement('net-routes-create')
    api.child_add_string("destination", destination)
    api.child_add_string("gateway", gateway)
    api.child_add_string("metric", metric)

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
        destination=dict(required=True),
        gateway=dict(required=True),
        metric=dict(required=True, type='int'),))
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=False)

    results = route_create(module)
    module.exit_json(**results)


from ansible.module_utils.basic import *
main()
