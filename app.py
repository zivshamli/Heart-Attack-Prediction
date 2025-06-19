#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import json
import time
from confluent_kafka import Producer, Consumer

# Kafka Configuration
KAFKA_TOPIC_INPUT = "test"
KAFKA_TOPIC_OUTPUT = "prediction"  # Topic where predictions are received
producer_config = {'bootstrap.servers': 'localhost:9092'}
consumer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'streamlit-consumer-' + str(time.time()),  # Unique for each run
    'auto.offset.reset': 'latest'
}
producer = Producer(producer_config)
consumer = Consumer(consumer_config)
consumer.subscribe([KAFKA_TOPIC_OUTPUT])

# Streamlit UI
st.title("Kafka Data Submission and Prediction System")

# Input Fields
age = st.number_input("Age (age)", min_value=0, max_value=120, step=1)
sex = st.toggle("Gender: Male (On) / Female (Off) (sex)")
trestbps = st.number_input("Resting Blood Pressure (trestbps)", min_value=80, max_value=200, step=1)
chol = st.number_input("Cholesterol Level (chol)", min_value=100, max_value=600, step=1)
fbs = st.toggle("Fasting Blood Sugar > 120 mg/dL (Yes: On, No: Off) (fbs)")
restecg = st.selectbox("Resting ECG Result (restecg)", ["normal", "lv hypertrophy", "st-t abnormality"])
thalch = st.number_input("Maximum Heart Rate Achieved (thalch)", min_value=50, max_value=220, step=1)
exang = st.toggle("Exercise Induced Angina (Yes: On, No: Off) (exang)")
oldpeak = st.number_input("ST Depression Induced by Exercise (oldpeak)", min_value=0.0, max_value=6.2, step=0.1)
cp = st.selectbox("Chest Pain Type (CP) (cp)", ['asymptomatic', 'non-anginal', 'atypical angina', 'typical angina'])

# Mapping categorical values to numerical values
restecg_mapping = {"normal": 0, "lv hypertrophy": 1, "st-t abnormality": 2}
cp_mapping = {'asymptomatic': 0, 'non-anginal': 1, 'atypical angina': 2, 'typical angina': 3}

data = {
    "age": age,
    "sex": 1 if sex else 0,
    "trestbps": trestbps,
    "chol": chol,
    "fbs": 1 if fbs else 0,
    "restecg": restecg_mapping[restecg],  
    "thalch": thalch,
    "exang": 1 if exang else 0,
    "oldpeak": oldpeak,
    "cp": cp_mapping[cp]  
}

# Kafka Delivery Report Callback
def delivery_report(err, msg):
    if err:
        st.error(f"Error sending message: {err}")
    else:
        st.info(f"Message successfully delivered to topic {msg.topic()} (partition {msg.partition()})")

# Send Data to Kafka & Receive Prediction
if st.button("Submit Data and Receive Prediction"):
    try:
        # Send input data to Kafka
        producer.produce(KAFKA_TOPIC_INPUT, json.dumps(data).encode('utf-8'), callback=delivery_report)
        producer.flush()
        st.info("Data was successfully sent to Kafka.")

        # Wait for prediction from Kafka
        prediction = None
        with st.spinner("Waiting for model prediction..."):
            start_time = time.time()
            while time.time() - start_time < 120:  # Wait up to 120 seconds
                msg = consumer.poll(1.0)
                if msg is None:
                    continue
                if msg.error():
                    st.error(f"Kafka error: {msg.error()}")
                    break

                # Decode message and ensure it's a number
                result = json.loads(msg.value().decode('utf-8'))
                print(f"📩 Received from Kafka: {result}")  # Debugging print
                if "prediction" in result and isinstance(result["prediction"], (int, float)):
                    prediction = result["prediction"]
                    break

        # Display Prediction
        if prediction is not None:
            print(f"✅ Prediction to display: {prediction}")  # Debugging print
            st.success(f"Model Prediction: {int(prediction) if isinstance(prediction, int) or prediction.is_integer() else prediction}")
        else:
            print("⚠ No prediction received!")  # Debugging print
            st.warning("No prediction received. Please try again.")

    except Exception as e:
        st.error(f"An error occurred: {e}")


# In[ ]:





# In[ ]:




