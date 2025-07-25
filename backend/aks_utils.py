from azure.identity import DefaultAzureCredential
from azure.mgmt.containerservice import ContainerServiceClient
from kubernetes import client, config
import os

# Helper to get AKS credentials

def get_aks_credentials(subscription_id, resource_group, cluster_name):
    credential = DefaultAzureCredential()
    containerservice_client = ContainerServiceClient(credential, subscription_id)
    cred = containerservice_client.managed_clusters.list_cluster_admin_credentials(resource_group, cluster_name)
    kubeconfig = cred.kubeconfigs[0].value.decode()
    with open("/tmp/kubeconfig", "w") as f:
        f.write(kubeconfig)
    config.load_kube_config(config_file="/tmp/kubeconfig")

# Helper to list namespaces

def list_namespaces():
    v1 = client.CoreV1Api()
    namespaces = v1.list_namespace()
    return [ns.metadata.name for ns in namespaces.items]

# Helper to list pods grouped by name

def list_pods(namespace):
    v1 = client.CoreV1Api()
    pods = v1.list_namespaced_pod(namespace)
    pod_names = list(set([pod.metadata.name for pod in pods.items]))
    return pod_names

# Helper to get logs

def get_pod_logs(namespace, pod_name, grep_filter=None):
    v1 = client.CoreV1Api()
    logs = v1.read_namespaced_pod_log(name=pod_name, namespace=namespace)
    if grep_filter:
        logs = '\n'.join([line for line in logs.split('\n') if grep_filter in line])
    return logs
