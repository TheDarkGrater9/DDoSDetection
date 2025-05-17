import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from app.schemas import InputData
import os

TRAIN_FEATURES = [
    "Flow Iat Mean", "Idle Mean", "Fwd Iat Mean", "Packet Length Mean",
    "Fwd Packet Length Mean", "Flow Iat Std", "Fwd Packet Length Min",
    "Idle Min", "Flow Iat Min", "Init Fwd Win Bytes", "Packet Length Variance",
    "Cwe Flag Count", "Protocol_0", "Protocol_6", "Protocol_17",
    "Flow Packets Per S", "Fwd Packets Per S", "Fwd Psh Flags", "Fwd Act Data Packets",
    "Fwd Iat Std", "Avg Fwd Segment Size", "Flow Iat Max", "Total Fwd Packets",
    "Subflow Fwd Packets", "Fwd Iat Min", "Urg Flag Count", "Ack Flag Count",
    "Rst Flag Count", "Fwd Packet Length Std", "Fwd Iat Max", "Packet Length Min",
    "Active Max"
]

RENAME_MAP = {
    "flow_iat_mean": "Flow Iat Mean",
    "idle_mean": "Idle Mean",
    "fwd_iat_mean": "Fwd Iat Mean",
    "packet_length_mean": "Packet Length Mean",
    "fwd_packet_length_mean": "Fwd Packet Length Mean",
    "flow_iat_std": "Flow Iat Std",
    "fwd_packet_length_min": "Fwd Packet Length Min",
    "idle_min": "Idle Min",
    "flow_iat_min": "Flow Iat Min",
    "init_fwd_win_bytes": "Init Fwd Win Bytes",
    "packet_length_variance": "Packet Length Variance",
    "cwe_flag_count": "Cwe Flag Count",
    "flow_packets_per_s": "Flow Packets Per S",
    "fwd_packets_per_s": "Fwd Packets Per S",
    "fwd_psh_flags": "Fwd Psh Flags",
    "fwd_act_data_packets": "Fwd Act Data Packets",
    "fwd_iat_std": "Fwd Iat Std",
    "avg_fwd_segment_size": "Avg Fwd Segment Size",
    "flow_iat_max": "Flow Iat Max",
    "total_fwd_packets": "Total Fwd Packets",
    "subflow_fwd_packets": "Subflow Fwd Packets",
    "fwd_iat_min": "Fwd Iat Min",
    "urg_flag_count": "Urg Flag Count",
    "ack_flag_count": "Ack Flag Count",
    "rst_flag_count": "Rst Flag Count",
    "fwd_packet_length_std": "Fwd Packet Length Std",
    "fwd_iat_max": "Fwd Iat Max",
    "packet_length_min": "Packet Length Min",
    "active_max": "Active Max",
    "protocol": "Protocol"
}


_model = None
_scaler = None

def load_artifacts():
    global _model, _scaler
    if _model is None or _scaler is None:
        _scaler = joblib.load("app/model/minmax_scaler.pkl")
        _model = joblib.load("app/model/model.pkl")
    return _model, _scaler

def preprocess_input(data: InputData):
    _, scaler = load_artifacts()
    df = pd.DataFrame([data.dict()])
    df.rename(columns=RENAME_MAP, inplace=True)
    df = pd.get_dummies(df, columns=["Protocol"])
    for proto in ["Protocol_0", "Protocol_6", "Protocol_17"]:
        if proto not in df.columns:
            df[proto] = 0
    final_df = df.reindex(columns=TRAIN_FEATURES, fill_value=0)
    final_scaled = scaler.transform(final_df)
    return final_scaled

def predict_label(processed_data):
    model, _ = load_artifacts()
    prediction = model.predict(processed_data)
    return int(prediction[0])
