#/bin/bash/env python

from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager

# set options for play
Options = namedtuple('Options', ['connection', 'module_path', 'forks',
                                 'become', 'become_method', 'become_user', 'check'])

#initialize needed objects
variable_manager = VariableManager()
loader = DataLoader()
options = Options(connection='local', module_path='', forks=100, become=True,
                  become_method='sudo', become_user='root', check=False)
passwords = dict(vault_pass='secret')

#create inventory and pass to var manager
inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list='/etc/ansible/hosts')
variable_manager.set_inventory(inventory)

#create play with tasks
play_src = dict(
            name="show openstack network details",
            hosts="192.168.10.238",
            gather_facts="no",
            become="true",
            tasks=[
		dict(name="Gather facts about previously created networks", action=dict(module="os_networks_facts", auth=dict(auth_url="http://192.168.10.238:5000/v2.0",
                username="<enter>", password="<enter>",project_name="<enter>"))),

                dict(name="Show openstack networks", action=dict(module="debug", var="openstack_networks")),

		dict(name="Gather facts about previously created subnets", action=dict(module="os_subnets_facts", auth=dict(auth_url="http://192.168.10.238:5000/v2.0",
                username="<enter>", password="<enter>",project_name="<enter>"))),

                dict(name="Show openstack subnets", action=dict(module="debug", var="openstack_subnets")),

		dict(name="Gather facts about previously created ports", action=dict(module="os_port_facts", auth=dict(auth_url="http://192.168.10.238:5000/v2.0",
                username="<enter>", password="<enter>",project_name="<enter>"))),

                dict(name="Show openstack ports", action=dict(module="debug", var="openstack_ports")),

		dict(name="Gather facts about previously created servers", action=dict(module="os_server_facts", auth=dict(auth_url="http://192.168.10.238:5000/v2.0",
                username="<enter>", password="<enter>",project_name="<enter>"))),

                dict(name="Show openstack servers", action=dict(module="debug", var="openstack_servers")),		

                dict(name="Gather facts about previously created router", action=dict(module="os_router_facts", auth=dict(auth_url="http://192.168.10.238:5000/v2.0",
                username="<enter>", password="<enter>",project_name="<enter>"))),
                
                dict(name="Show openstack routers", action=dict(module="debug", var="openstack_routers"))
	]            

       )
play = Play().load(play_src, variable_manager=variable_manager, loader=loader)

#actually run it
tqm = None
try:
    tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            passwords=passwords,
            stdout_callback="default",
        )
    result = tqm.run(play)
finally:
    if tqm is not None:
        tqm.cleanup()
