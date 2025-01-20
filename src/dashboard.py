import streamlit as st
import requests

# Title of the dashboard
st.title("Customer Segmentation Dashboard")

# Input fields for user data
quantity = st.number_input("Quantity", min_value=0.0, value=1.0, step=1.0)
unit_price = st.number_input("Unit Price", min_value=0.0, value=1.0, step=0.1)
country = st.text_input("Country", value="")

# Button to trigger customer segmentation
if st.button("Predict Cluster"):
    # Data to send to the API
    payload = {
        "quantity": quantity,
        "unit_price": unit_price,
        "country": country
    }

    # Call the FastAPI endpoint
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Cluster: {result['predicted_cluster']}")
        else:
            st.error(f"Error: {response.status_code} - {response.json()}")
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to the API: {e}")
