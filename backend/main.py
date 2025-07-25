from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
# from auth import router as auth_router  # Temporarily disabled
from aks_utils import get_aks_credentials, list_namespaces, list_pods, get_pod_logs
from ai_utils import explain_logs_with_ai

app = FastAPI()
# app.include_router(auth_router)  # Temporarily disabled

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LogRequest(BaseModel):
    subscription_id: str
    resource_group: str
    cluster_name: str
    namespace: str
    pod_name: str
    grep_filter: str = None

@app.post("/get_logs")
async def get_logs(req: LogRequest):
    # Get AKS credentials and configure k8s client
    get_aks_credentials(req.subscription_id, req.resource_group, req.cluster_name)
    logs = get_pod_logs(req.namespace, req.pod_name, req.grep_filter)
    return {"logs": logs}

@app.get("/namespaces")
async def get_namespaces(subscription_id: str, resource_group: str, cluster_name: str):
    get_aks_credentials(subscription_id, resource_group, cluster_name)
    namespaces = list_namespaces()
    return {"namespaces": namespaces}

@app.get("/pods")
async def get_pods(subscription_id: str, resource_group: str, cluster_name: str, namespace: str):
    get_aks_credentials(subscription_id, resource_group, cluster_name)
    pods = list_pods(namespace)
    return {"pods": pods}

@app.post("/explain_logs")
async def explain_logs(logs: str):
    explanation = explain_logs_with_ai(logs)
    return {"explanation": explanation}
