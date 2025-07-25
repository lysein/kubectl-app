import streamlit as st
import requests
# from streamlit_authenticator import Authenticate  # Temporarily disabled
import os

st.set_page_config(page_title="AKS Log Explorer", layout="wide")
st.title("AKS Log Explorer")

st.markdown("""
This app lets you connect to AKS, select namespace, pod, and view logs with AI explanations.
""")

# --- Temporarily skip authentication for testing ---
st.success("Ready to explore AKS logs!")

# --- AKS Details ---
subscription_id = st.text_input("Azure Subscription ID")
resource_group = st.text_input("Resource Group")
cluster_name = st.text_input("AKS Cluster Name")
if subscription_id and resource_group and cluster_name:
    # Namespaces
    ns_url = f"http://localhost:8001/namespaces?subscription_id={subscription_id}&resource_group={resource_group}&cluster_name={cluster_name}"
    try:
        namespaces_response = requests.get(ns_url)
        namespaces = namespaces_response.json()["namespaces"]
        namespace = st.selectbox("Select Namespace", namespaces)
        if namespace:
            # Pods
            pods_url = f"http://localhost:8001/pods?subscription_id={subscription_id}&resource_group={resource_group}&cluster_name={cluster_name}&namespace={namespace}"
            pods_response = requests.get(pods_url)
            pods = pods_response.json()["pods"]
            pod_name = st.selectbox("Select Pod", pods)
            if pod_name:
                grep_filter = st.text_input("Grep Filter (e.g. error)")
                if st.button("Get Logs"):
                    payload = {
                        "subscription_id": subscription_id,
                        "resource_group": resource_group,
                        "cluster_name": cluster_name,
                        "namespace": namespace,
                        "pod_name": pod_name,
                        "grep_filter": grep_filter
                    }
                    logs_response = requests.post("http://localhost:8001/get_logs", json=payload)
                    logs = logs_response.json()["logs"]
                    st.text_area("Pod Logs", logs, height=300)
                    if st.button("Explain with AI"):
                        explanation_response = requests.post("http://localhost:8001/explain_logs", json=logs)
                        explanation = explanation_response.json()["explanation"]
                        st.markdown(f"**AI Explanation:** {explanation}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to backend: {e}")
    except KeyError as e:
        st.error(f"Error parsing response: {e}")
