import os
import re
import requests
import json
import logging
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)

from django.core.management.base import BaseCommand
from account.models import Team
from django.conf import settings
from django.utils import timezone
RANCHER_ACCESS_KEY = os.environ.get('RANCHER_ACCESS_KEY', None)
RANCHER_SECRET_KEY = os.environ.get('RANCHER_SECRET_KEY', None)


def safe_str(unsafe):
    unsafe = unsafe.replace(' ', '_')
    unsafe = re.sub('[^A-Za-z0-9_-]', '', unsafe)
    if len(unsafe) == 0:
        raise Exception("Empty result")
    return unsafe


def get_current_state():
    data = requests.get(
        'https://rancher.galaxians.org/v2-beta/projects/1a5/stacks/1st19/services',
        auth=(RANCHER_ACCESS_KEY, RANCHER_SECRET_KEY)
    ).json()
    state = {}
    for container in data['data']:
        labels = container['launchConfig']['labels']
        if 'org.galaxians.ctf' not in labels:
            continue

        state[container['launchConfig']['labels']['org.galaxians.ctf.team.name']] = {
            'id': container['id'],
        }
    return state


def update_load_balancer(routes):
    port_rules = []
    linked_services = {}

    priority = 1
    for (team_name, data) in routes.items():
        port_rules.append({
            "path" : "/galaxy-%s" % team_name,
            "priority" : priority,
            "protocol" : "http",
            "serviceId" : routes[team_name]['id'],
            "sourcePort" : 81,
            "targetPort" : 80,
            "type" : "portRule",
        })
        linked_services['galaxy-%s' % team_name] = routes[team_name]['id']
        priority += 1

    port_rules.append({
        "path": "/",
        "priority" : priority,
        "protocol": "http",
        "serviceId": "1s72",
        "sourcePort": 81,
        "targetPort": 80,
        "type": "portRule",
    })

    data = {
        "externalId" : None,
        "removed" : None,
        "uuid" : "41c43307-a6a6-4472-8112-979a774a877a",
        "assignServiceIpAddress" : False,
        "name" : "lb",
        "state" : "active",
        "type" : "loadBalancerService",
        "scalePolicy" : None,
        "launchConfig" : {
            "cpuPercent" : None,
            "ipcMode" : None,
            "vcpu" : 1,
            "memoryMb" : None,
            "stdinOpen" : False,
            "instanceTriggeredStop" : "stop",
            "networkMode" : "managed",
            "ioMaximumBandwidth" : None,
            "kind" : "container",
            "pidMode" : None,
            "count" : None,
            "cpuPeriod" : None,
            "healthState" : None,
            "pidsLimit" : None,
            "imageUuid" : "docker:rancher/lb-service-haproxy:v0.7.1",
            "userdata" : None,
            "diskQuota" : None,
            "usernsMode" : None,
            "memory" : None,
            "readOnly" : False,
            "ip" : None,
            "ioMaximumIOps" : None,
            "startOnCreate" : True,
            "ip6" : None,
            "shmSize" : None,
            "hostname" : None,
            "createIndex" : None,
            "ports" : [
                "81:81/tcp"
            ],
            "memorySwappiness" : None,
            "type" : "launchConfig",
            "labels" : {
                "io.rancher.container.agent.role" : "environmentAdmin",
                "io.rancher.container.create_agent" : "True"
            },
            "uts" : None,
            "healthCheck" : {
                "strategy" : None,
                "requestLine" : None,
                "responseTimeout" : 2000,
                "recreateOnQuorumStrategyConfig" : None,
                "type" : "instanceHealthCheck",
                "initializingTimeout" : 60000,
                "interval" : 2000,
                "healthyThreshold" : 2,
                "port" : 42,
                "reinitializingTimeout" : 60000,
                "unhealthyThreshold" : 3,
                "name" : None
            },
            "workingDir" : None,
            "kernelMemory" : None,
            "cpuShares" : None,
            "externalId" : None,
            "memorySwap" : None,
            "removed" : None,
            "uuid" : None,
            "isolation" : None,
            "memoryReservation" : None,
            "stopSignal" : None,
            "firstRunning" : None,
            "cpuSetMems" : None,
            "milliCpuReservation" : None,
            "cpuSet" : None,
            "expose" : [],
            "cpuCount" : None,
            "privileged" : False,
            "deploymentUnitUuid" : None,
            "networkLaunchConfig" : None,
            "tty" : False,
            "description" : None,
            "healthRetries" : None,
            "domainName" : None,
            "oomScoreAdj" : None,
            "requestedIpAddress" : None,
            "cpuQuota" : None,
            "volumeDriver" : None,
            "startCount" : None,
            "healthInterval" : None,
            "publishAllPorts" : False,
            "version" : "0",
            "system" : False,
            "blkioWeight" : None,
            "cgroupParent" : None,
            "healthTimeout" : None,
            "created" : None,
            "user" : None
        },
        "created" : "2017-05-06T22:02:09Z",
        "secondaryLaunchConfigs" : [],
        "baseType" : "service",
        "vip" : None,
        "startOnCreate" : True,
        "linkedServices" : linked_services,
        "transitioningProgress" : None,
        "publicEndpoints" : [
            {
                "instanceId" : "1i123",
                "type" : "publicEndpoint",
                "serviceId" : "1s30",
                "ipAddress" : "207.154.226.63",
                "port" : 81,
                "hostId" : "1h2"
            }
        ],
        "accountId" : "1a5",
        "selectorLink" : None,
        "system" : False,
        "retainIp" : None,
        "lbConfig" : {
            "certificateIds" : [],
            "portRules" : port_rules,
            "defaultCertificateId" : None,
            "type" : "lbConfig",
            "stickinessPolicy" : None,
            "config" : None
        },
        "scale" : 1,
        "healthState" : "healthy",
        "transitioningMessage" : None,
        "transitioning" : "no",
        "metadata" : None,
        "description" : None,
        "kind" : "loadBalancerService",
        "fqdn" : "lb.galaxy.galaxians.org.",
        "createdTS" : 1494108129000,
        "stackId" : "1st19",
        "upgrade" : None,
        "currentScale" : 1,
        "id" : "1s30"
    }

    resp = requests.put(
        'https://rancher.galaxians.org/v2-beta/projects/1a5/loadbalancerservices/1s30',
        auth=(RANCHER_ACCESS_KEY, RANCHER_SECRET_KEY),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        data=json.dumps(data),
    ).json()
    return resp


def launch_container(team_name, team_id, galaxy_password):
    data = {
        "removed" : None,
        "selectorLink" : None,
        "description" : None,
        "created" : None,
        "scale" : 1,
        "healthState" : None,
        "stackId" : "1st19",
        "uuid" : None,
        "name" : "galaxy-%s" % team_name,
        "type" : "service",
        "secondaryLaunchConfigs" : [],
        "launchConfig" : {
            "logConfig" : {
                "config" : {},
                "driver" : ""
            },
            "requestedIpAddress" : None,
            "userdata" : None,
            "isolation" : None,
            "cgroupParent" : None,
            "dns" : [],
            "healthCheck" : {
                "recreateOnQuorumStrategyConfig" : None,
                "responseTimeout" : 2000,
                "interval" : 2000,
                "unhealthyThreshold" : 3,
                "strategy" : "none",
                "port" : 80,
                "healthyThreshold" : 2,
                "reinitializingTimeout" : 60000,
                "initializingTimeout" : 60000,
                "name" : None,
                "type" : "instanceHealthCheck",
                "requestLine" : "GET \"/\" \"HTTP/1.0\""
            },
            "hostname" : None,
            "capAdd" : [],
            "healthTimeout" : None,
            "devices" : [],
            "memory" : 1258291200,
            "tty" : True,
            "stdinOpen" : True,
            "healthState" : None,
            "diskQuota" : None,
            "description" : None,
            "labels" : {
                "org.galaxians.ctf" : "gccctf2017",
                "org.galaxians.ctf.team.name" : team_name,
                "org.galaxians.ctf.team.id" : str(team_id),
                "io.rancher.scheduler.affinity:host_label" : "role=compute",
                "io.rancher.container.pull_image" : "always",
            },
            "cpuQuota" : None,
            "count" : None,
            "dnsSearch" : [],
            "dataVolumes" : [],
            "createIndex" : None,
            "cpuPercent" : None,
            "cpuPeriod" : None,
            "externalId" : None,
            "pidMode" : None,
            "restartPolicy" : {
                "name" : "always"
            },
            "workingDir" : None,
            "ports" : [],
            "privileged" : False,
            "kernelMemory" : None,
            "cpuSet" : None,
            "dataVolumesFromLaunchConfigs" : [],
            "memorySwappiness" : None,
            "instanceTriggeredStop" : "stop",
            "firstRunning" : None,
            "uts" : None,
            "ioMaximumIOps" : None,
            "usernsMode" : None,
            "capDrop" : [],
            "startOnCreate" : True,
            "secrets" : [],
            "blkioWeight" : None,
            "pidsLimit" : None,
            "ip" : None,
            "networkMode" : "managed",
            "memoryReservation" : None,
            "kind" : "container",
            "vcpu" : 1,
            "publishAllPorts" : False,
            "dataVolumesFrom" : [],
            "volumeDriver" : None,
            "uuid" : None,
            "deploymentUnitUuid" : None,
            "cpuShares" : None,
            "ioMaximumBandwidth" : None,
            "healthInterval" : None,
            "startCount" : None,
            "memoryMb" : None,
            "stopSignal" : None,
            "readOnly" : False,
            "memorySwap" : None,
            "ipcMode" : None,
            "ip6" : None,
            "shmSize" : None,
            "cpuSetMems" : None,
            "environment" : {
                "PROXY_PREFIX": "/galaxy-%s" % team_name,
                "GALAXY_DEFAULT_ADMIN_PASSWORD": galaxy_password,
                "GALAXY_CONFIG_OVERRIDE_STATSD_PREFIX": "galaxy-all",
                "GALAXY_CONFIG_OVERRIDE_STATSD_HOST": "127.0.0.1",
                "GALAXY_CONFIG_OVERRIDE_STATSD_PORT": 8125,
                "TEAM_ID" : str(team_id),
                "TEAM_NAME" : team_name,
            },
            "type" : "launchConfig",
            "user" : None,
            "networkLaunchConfig" : None,
            "cpuCount" : None,
            "created" : None,
            "milliCpuReservation" : None,
            "removed" : None,
            "domainName" : None,
            "oomScoreAdj" : None,
            "healthRetries" : None,
            "imageUuid" : "docker:quay.io/erasche/gccctf2017:master"
        },
        "assignServiceIpAddress" : False,
        "kind" : None,
        "externalId" : None,
        "vip" : None,
        "selectorContainer" : None,
        "fqdn" : None,
        "createIndex" : None,
        "startOnCreate" : True
    }
    resp = requests.post(
        'https://rancher.galaxians.org/v2-beta/projects/1a5/service',
        auth=(RANCHER_ACCESS_KEY, RANCHER_SECRET_KEY),
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
        data=json.dumps(data),
    ).json()
    return resp


class Command(BaseCommand):
    help = 'gx-manager'

    def handle(self, *args, **options):
        if RANCHER_ACCESS_KEY is None:
            raise Exception("Please set RANCHER_ACCESS_KEY")
        if RANCHER_SECRET_KEY is None:
            raise Exception("Please set RANCHER_SECRET_KEY")

        if not(settings.COMPETITION_STARTS < timezone.now() < settings.COMPETITION_ENDS):
            logging.info("Competition has not stated yet")
            sys.exit(0)

        current_state = get_current_state()
        stateChanged = False
        for team in Team.objects.all():

            safe_team_name = team.name
            safe_team_id = team.id
            safe_team_password = team.password

            if safe_team_name in current_state:
                logging.debug("Team [%s] container available, continuing", safe_team_name)
            else:
                stateChanged = True
                # Then launch an image
                logging.info("Team [%s] container not available, launching", safe_team_name)
                container = launch_container(safe_team_name, safe_team_id, safe_team_password)
                logging.info("Launched %s", container['id'])

        # Refetch current state and update LB
        if stateChanged:
            update_load_balancer(get_current_state())
