st.set_page_config(page_title="AKS Log Explorer", layout="wide")
st.title("AKS Log Explorer")
st.markdown("""
import streamlit as st
import requests
from streamlit_authenticator import Authenticate
import os

st.set_page_config(page_title="AKS Log Explorer", layout="wide")
st.title("AKS Log Explorer")

st.markdown(
st.markdown("""
This app lets you log in with Microsoft SSO, select AKS details, namespace, pod, and view logs with AI explanations.
""")

# --- Authentication ---
users = {"usernames": ["user1"], "passwords": ["pass1"], "names": ["User One"]}
authenticator = Authenticate(users["usernames"], users["names"], users["passwords"], "some_cookie", "some_key", cookie_expiry_days=1)
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    st.success(f"Welcome {name}!")
    # --- AKS Details ---
    subscription_id = st.text_input("Azure Subscription ID")
    resource_group = st.text_input("Resource Group")
    cluster_name = st.text_input("AKS Cluster Name")
    if subscription_id and resource_group and cluster_name:
        # Namespaces
        ns_url = f"http://localhost:8000/namespaces?subscription_id={subscription_id}&resource_group={resource_group}&cluster_name={cluster_name}"
        namespaces = requests.get(ns_url).json()["namespaces"]
        namespace = st.selectbox("Select Namespace", namespaces)
        if namespace:
            # Pods
            pods_url = f"http://localhost:8000/pods?subscription_id={subscription_id}&resource_group={resource_group}&cluster_name={cluster_name}&namespace={namespace}"
            pods = requests.get(pods_url).json()["pods"]
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
                    logs = requests.post("http://localhost:8000/get_logs", json=payload).json()["logs"]
                    st.text_area("Pod Logs", logs, height=300)
                    if st.button("Explain with AI"):
                        explanation = requests.post("http://localhost:8000/explain_logs", json={"logs": logs}).json()["explanation"]
                        st.markdown(f"**AI Explanation:** {explanation}")
else:
    st.warning("Please log in to use the app.")
