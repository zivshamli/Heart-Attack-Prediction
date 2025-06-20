# ❤️ Real-Time Heart Attack Prediction System

This project presents a **real-time heart attack prediction pipeline** using **Apache Kafka**, **Apache Spark**, and a **custom GUI built with Streamlit**. It streams live health data, performs machine learning-based inference, and delivers the prediction to an interactive user interface.

---

## 🧠 Project Overview

Modern healthcare demands fast, intelligent decision-making. This system leverages machine learning and real-time data streaming to assess the risk of a heart attack based on key patient health parameters—**instantly and automatically**.

---

## 🔧 System Architecture

```plaintext
┌────────────┐     Kafka      ┌───────────────┐     Kafka       ┌────────────────────┐
│  Producer  │ ─────────────> │ Spark Analyzer│ ─────────────>  │  Streamlit GUI     │
└────────────┘                └───────────────┘                 └────────────────────┘
   (Simulates patient         (Consumes data, predicts,          (Sends input data,
    data stream)               and sends prediction)              displays results)

## ⚙ Technologies

- **Apache Kafka** – Real-time data streaming and inter-service communication  
- **Apache Spark** – Distributed data processing and machine learning inference  
- **Python** – Main development language  
- **Streamlit** – Lightweight GUI for user interaction  
- **ML Model** – Trained externally on medical datasets to detect heart attack risk  

---

## 🧩 Features

- Real-time prediction of heart attack likelihood  
- End-to-end streaming architecture (producer → Spark → GUI)  
- Lightweight and user-friendly interface  
- Extendable for additional medical use cases  

---

## 💻 How to Run

### 1. Start Kafka & Zookeeper

```bash
# Start Zookeeper
bin/zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka broker
bin/kafka-server-start.sh config/server.properties
```

### 2. Launch the Producer

Simulate data input to the Kafka topic (via script or notebook):

```bash
python data_heart_producer.py
```

### 3. Run Spark Consumer with Model

Run your Spark job that:

- Listens to Kafka topic `test`  
- Loads the trained ML model  
- Sends prediction to topic `prediction`  

```bash
spark-submit consumer_predictor.py
```

### 4. Start the Streamlit GUI

```bash
streamlit run app.py
```

Use the GUI to enter patient data and receive a prediction in real-time.

---

## 🩺 Input Features

- **Age**  
- **Sex**  
- **Chest pain type** (`cp`)  
- **Resting blood pressure** (`trestbps`)  
- **Cholesterol** (`chol`)  
- **Fasting blood sugar** (`fbs`)  
- **Resting ECG results** (`restecg`)  
- **Max heart rate achieved** (`thalch`)  
- **Exercise induced angina** (`exang`)  
- **ST depression induced by exercise** (`oldpeak`)  

---

## 🧠 Output

The system provides a binary prediction:

- `0`: No immediate heart attack risk  
- `1`: High risk of heart attack  

---

## 🔮 Future Enhancements

- Add persistent storage for predictions (e.g., database)  
- Improve model accuracy with more features or deep learning  
- Deploy GUI as a cloud web app  
- Enable REST API access for mobile or remote clients  
- Add real-time alerts and historical dashboards  

---

## 📌 Notes

- Ensure Kafka topics `test` and `prediction` are created and monitored  
- The ML model should be pre-trained and saved (e.g., `heart_model.pkl`)  
- Streamlit app and Spark consumer should be running simultaneously for full functionality  

---

## 🙏 Acknowledgments

Thanks to:

- The UCI Heart Disease Dataset  
- Apache Kafka and Spark communities  
- Streamlit for fast and beautiful app interfaces  

