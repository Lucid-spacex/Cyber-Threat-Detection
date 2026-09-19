"""
Phase 2 Demo App: Hybrid IoT Intrusion Detection System
Flask backend for serving ML model predictions
"""

import os
import numpy as np
import pandas as pd
import joblib
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuration from environment variables
DEBUG = os.environ.get('FLASK_DEBUG', '0') == '1'
PORT = int(os.environ.get('PORT', 5000))
HOST = os.environ.get('HOST', '0.0.0.0')

# Global variables to store loaded models and preprocessing components
svm_model = None
rf_model = None
scaler = None
label_encoder = None
feature_info = None
sample_data = None

# Paths
MODELS_DIR = os.environ.get('MODELS_DIR', 'saved_models')
CSV_BASE_PATH = os.environ.get('CSV_BASE_PATH', 'CSV/CSV')

def load_models():
    """Load all trained models and preprocessing components"""
    global svm_model, rf_model, scaler, label_encoder, feature_info
    
    print("Loading models and preprocessing components...")
    
    try:
        # Load the trained models
        svm_model = joblib.load(os.path.join(MODELS_DIR, 'svm_model.pkl'))
        rf_model = joblib.load(os.path.join(MODELS_DIR, 'rf_model.pkl'))
        
        # Load preprocessing components
        scaler = joblib.load(os.path.join(MODELS_DIR, 'scaler_20.pkl'))
        label_encoder = joblib.load(os.path.join(MODELS_DIR, 'label_encoder.pkl'))
        feature_info = joblib.load(os.path.join(MODELS_DIR, 'feature_info.pkl'))
        
        print("Models loaded successfully!")
        print(f"Top features: {feature_info['top_features']}")
        
    except Exception as e:
        print(f"Error loading models: {e}")
        raise

def load_sample_data():
    """Load a small sample of data from the CSV files for the /sample endpoint"""
    global sample_data
    
    print("Loading sample data for examples...")
    
    try:
        # Check if CSV directory exists (may not in production)
        if not os.path.exists(CSV_BASE_PATH):
            print("CSV directory not found, using hardcoded sample data")
            # Use hardcoded sample data for production deployment
            sample_data = [
                {
                    'Header_Length': 64.0, 'Tot sum': 1200.0, 'AVG': 60.0, 'Protocol Type': 6.0,
                    'Max': 150.0, 'syn_flag_number': 0.0, 'fin_flag_number': 0.0, 'Variance': 25.0,
                    'psh_flag_number': 1.0, 'UDP': 1.0, 'IAT': 0.001, 'ack_count': 10.0,
                    'TCP': 0.0, 'ICMP': 0.0, 'Number': 5.0, 'Rate': 1000.0,
                    'ack_flag_number': 1.0, 'HTTP': 0.0, 'Min': 0.0, 'HTTPS': 0.0,
                    'label': 'Benign_Final'
                },
                {
                    'Header_Length': 20.0, 'Tot sum': 5000.0, 'AVG': 250.0, 'Protocol Type': 17.0,
                    'Max': 500.0, 'syn_flag_number': 1.0, 'fin_flag_number': 0.0, 'Variance': 100.0,
                    'psh_flag_number': 0.0, 'UDP': 0.0, 'IAT': 0.01, 'ack_count': 2.0,
                    'TCP': 1.0, 'ICMP': 0.0, 'Number': 10.0, 'Rate': 500.0,
                    'ack_flag_number': 0.0, 'HTTP': 0.0, 'Min': 50.0, 'HTTPS': 0.0,
                    'label': 'DDoS-ICMP_Flood'
                },
                {
                    'Header_Length': 40.0, 'Tot sum': 3000.0, 'AVG': 150.0, 'Protocol Type': 17.0,
                    'Max': 300.0, 'syn_flag_number': 1.0, 'fin_flag_number': 0.0, 'Variance': 50.0,
                    'psh_flag_number': 0.0, 'UDP': 0.0, 'IAT': 0.005, 'ack_count': 5.0,
                    'TCP': 1.0, 'ICMP': 0.0, 'Number': 8.0, 'Rate': 600.0,
                    'ack_flag_number': 0.0, 'HTTP': 0.0, 'Min': 30.0, 'HTTPS': 0.0,
                    'label': 'Mirai-udpplain'
                }
            ]
            print(f"Loaded {len(sample_data)} hardcoded sample rows")
            return
        
        # Load a few samples from different classes
        sample_rows = []
        
        # Define which classes to sample from (3-5 examples)
        sample_classes = [
            'Benign_Final',
            'DDoS-ICMP_Flood', 
            'Mirai-udpplain',
            'MITM-ArpSpoofing',
            'Recon-PortScan'
        ]
        
        for class_name in sample_classes:
            class_path = os.path.join(CSV_BASE_PATH, class_name)
            if os.path.exists(class_path):
                csv_files = [f for f in os.listdir(class_path) if f.endswith('.csv')]
                if csv_files:
                    # Load first sample from first file
                    file_path = os.path.join(class_path, csv_files[0])
                    df = pd.read_csv(file_path, nrows=1)
                    if len(df) > 0:
                        sample_rows.append(df.iloc[0].to_dict())
        
        if sample_rows:
            sample_data = sample_rows
            print(f"Loaded {len(sample_data)} sample rows from CSV files")
        else:
            print("Warning: No sample data loaded from CSV, using hardcoded samples")
            # Fallback to hardcoded samples
            sample_data = [
                {
                    'Header_Length': 64.0, 'Tot sum': 1200.0, 'AVG': 60.0, 'Protocol Type': 6.0,
                    'Max': 150.0, 'syn_flag_number': 0.0, 'fin_flag_number': 0.0, 'Variance': 25.0,
                    'psh_flag_number': 1.0, 'UDP': 1.0, 'IAT': 0.001, 'ack_count': 10.0,
                    'TCP': 0.0, 'ICMP': 0.0, 'Number': 5.0, 'Rate': 1000.0,
                    'ack_flag_number': 1.0, 'HTTP': 0.0, 'Min': 0.0, 'HTTPS': 0.0,
                    'label': 'Benign_Final'
                }
            ]
            
    except Exception as e:
        print(f"Error loading sample data: {e}")
        print("Using hardcoded sample data as fallback")
        # Fallback to hardcoded samples
        sample_data = [
            {
                'Header_Length': 64.0, 'Tot sum': 1200.0, 'AVG': 60.0, 'Protocol Type': 6.0,
                'Max': 150.0, 'syn_flag_number': 0.0, 'fin_flag_number': 0.0, 'Variance': 25.0,
                'psh_flag_number': 1.0, 'UDP': 1.0, 'IAT': 0.001, 'ack_count': 10.0,
                'TCP': 0.0, 'ICMP': 0.0, 'Number': 5.0, 'Rate': 1000.0,
                'ack_flag_number': 1.0, 'HTTP': 0.0, 'Min': 0.0, 'HTTPS': 0.0,
                'label': 'Benign_Final'
            }
        ]

@app.route('/')
def index():
    """Serve the frontend HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/sample', methods=['GET'])
def get_sample():
    """Return example feature samples for the frontend"""
    if sample_data is None or len(sample_data) == 0:
        return jsonify({'error': 'No sample data available'}), 404
    
    # Return the samples with their feature values
    # We need to format them according to the expected feature order
    top_features = feature_info['top_features']
    
    formatted_samples = []
    for i, sample in enumerate(sample_data):
        # Extract only the top features in the correct order
        feature_values = []
        for feature in top_features:
            value = sample.get(feature, 0)
            # Handle any potential NaN or infinite values
            if pd.isna(value) or np.isinf(value):
                value = 0
            feature_values.append(float(value))
        
        formatted_samples.append({
            'id': i,
            'class': sample.get('label', 'Unknown'),
            'features': feature_values
        })
    
    return jsonify({
        'samples': formatted_samples,
        'feature_names': top_features
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Make predictions using SVM, RF, and Hybrid models"""
    try:
        # Get feature values from request
        data = request.get_json()
        
        if 'features' not in data:
            return jsonify({'error': 'No features provided'}), 400
        
        features = data['features']
        
        # Validate that we have the correct number of features
        expected_features = feature_info['top_features']
        if len(features) != len(expected_features):
            return jsonify({
                'error': f'Expected {len(expected_features)} features, got {len(features)}'
            }), 400
        
        # Convert to numpy array and reshape
        X = np.array(features).reshape(1, -1)
        
        # Handle any NaN or infinite values
        X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
        
        # Apply the same scaler transformation used in training
        X_scaled = scaler.transform(X)
        
        # Get probability predictions from both models
        svm_probs = svm_model.predict_proba(X_scaled)
        rf_probs = rf_model.predict_proba(X_scaled)
        
        # Get class predictions
        svm_pred = svm_model.predict(X_scaled)[0]
        rf_pred = rf_model.predict(X_scaled)[0]
        
        # Compute hybrid prediction by averaging probabilities
        hybrid_probs = (svm_probs + rf_probs) / 2
        hybrid_pred = np.argmax(hybrid_probs, axis=1)[0]
        
        # Get confidence scores (max probability for each prediction)
        svm_confidence = float(np.max(svm_probs))
        rf_confidence = float(np.max(rf_probs))
        hybrid_confidence = float(np.max(hybrid_probs))
        
        # Convert numeric predictions back to class names
        svm_class = label_encoder.inverse_transform([svm_pred])[0]
        rf_class = label_encoder.inverse_transform([rf_pred])[0]
        hybrid_class = label_encoder.inverse_transform([hybrid_pred])[0]
        
        return jsonify({
            'svm_prediction': svm_class,
            'svm_confidence': svm_confidence,
            'rf_prediction': rf_class,
            'rf_confidence': rf_confidence,
            'hybrid_prediction': hybrid_class,
            'hybrid_confidence': hybrid_confidence
        })
        
    except Exception as e:
        print(f"Prediction error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'models_loaded': svm_model is not None and rf_model is not None,
        'feature_count': len(feature_info['top_features']) if feature_info else 0
    })

# Load models on startup
load_models()
load_sample_data()

if __name__ == '__main__':
    print("Starting Flask server...")
    print(f"Access the demo at: http://{HOST}:{PORT}")
    print(f"Debug mode: {DEBUG}")
    app.run(host=HOST, port=PORT, debug=DEBUG)