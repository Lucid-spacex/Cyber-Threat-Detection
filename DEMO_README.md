# Phase 2 Demo App: Hybrid IoT Intrusion Detection System

This is a lightweight local demo application for the Hybrid ML-based Intrusion Detection System trained on the CICIoT2023 dataset. It allows you to submit traffic samples and see predictions from SVM, Random Forest, and Hybrid models side by side.

## Prerequisites

- Python 3.7 or higher installed
- Phase 1 models already trained (saved_models/ directory should exist)
- Original CSV dataset should be present in CSV/CSV/ directory

## Installation

1. **Install required dependencies:**

```bash
pip install -r requirements.txt
```

This will install Flask and Flask-CORS in addition to the existing dependencies from Phase 1.

## Running the Demo

### Step 1: Start the Backend Server

Open a terminal/command prompt in the project directory and run:

```bash
python app.py
```

**What to expect:**
- You should see messages indicating that models are being loaded
- After a few seconds, you'll see: "Starting Flask server..."
- Finally: "Access the demo at: http://localhost:5000"
- The server will remain running and show request logs when you use the app

**Example successful startup:**
```
Loading models and preprocessing components...
Models loaded successfully!
Top features: ['Header_Length', 'Tot sum', 'AVG', ...]
Loading sample data for examples...
Loaded 5 sample rows
Starting Flask server...
Access the demo at: http://localhost:5000
 * Running on http://0.0.0.0:5000
```

### Step 2: Open the Frontend

Open your web browser and navigate to:

```
http://localhost:5000
```

This will open the demo interface where you can:
- Select from pre-loaded example traffic samples
- Optionally enter manual feature values (advanced mode)
- Click "Classify Traffic" to get predictions
- View results from SVM, Random Forest, and Hybrid models

## Using the Demo

### Basic Usage (Recommended)

1. **Select a sample** from the dropdown menu (e.g., "Sample 1: Benign_Final")
2. Click the **"Classify Traffic"** button
3. View the results:
   - **SVM Model**: Shows SVM prediction and confidence
   - **Random Forest Model**: Shows RF prediction and confidence  
   - **Hybrid Model**: Shows the combined prediction (highlighted as the final decision)

### Advanced Usage (Manual Entry)

1. Click **"Advanced: Manual Feature Entry"** to expand the manual input section
2. Enter values for all 20 features (these are the top features selected during training)
3. Click **"Classify Traffic"** to get predictions

## Understanding the Results

- **Prediction**: The attack type or "Benign_Final" classification
- **Confidence**: Percentage indicating how confident the model is (0-100%)
- **Hybrid Model**: Combines SVM and RF predictions using soft voting (probability averaging) for more robust classification

## Stopping the Demo

To stop the backend server:
- Go to the terminal where `python app.py` is running
- Press `Ctrl+C` to stop the server

## Troubleshooting

### "No module named 'flask'" error
```bash
pip install flask flask-cors
```

### "Error loading models" error
- Ensure the `saved_models/` directory exists and contains all .pkl files
- Make sure you completed Phase 1 training first

### "No sample data available" error
- Ensure the `CSV/CSV/` directory exists with the original dataset
- Check that at least some CSV files are present

### Port 5000 already in use
If you get an error about port 5000 being in use, you can modify the port in `app.py`:
- Change `port=5000` to another port like `port=5001`
- Then access the demo at `http://localhost:5001`

## Technical Details

### Backend (app.py)
- Flask web server running on port 5000
- Loads trained SVM and Random Forest models from saved_models/
- Implements hybrid prediction logic: `hybrid_pred = argmax((svm_probs + rf_probs) / 2)`
- Two main endpoints:
  - `GET /sample` - Returns example traffic samples
  - `POST /predict` - Accepts feature values and returns predictions

### Frontend (index.html)
- Single HTML file with embedded CSS and JavaScript
- No build tools or frameworks required
- Responsive design for different screen sizes
- Primary interaction: Sample selection dropdown
- Secondary interaction: Manual feature entry (collapsed by default)

### Feature Information
- Uses 20 pre-selected features from the original 39 features
- Features were selected based on Random Forest importance ranking
- Features are standardized using the same scaler from training
- Feature order must match the order used during training

## Important Notes

- This is a **local demo only** - it does not connect to real networks or IoT devices
- All processing happens on your local machine
- No data is sent to external servers
- The demo uses a small subset of the original dataset for examples
- Models were trained on a stratified sample of ~47,935 rows from the original 46.7M row dataset

## For Academic Presentations

This demo is designed for oral defense and academic presentations:
- Shows the hybrid approach combining two ML models
- Demonstrates confidence scores for each model
- Highlights the hybrid model as the final decision
- Simple, clean interface suitable for projector display
- Fast response time for live demonstrations

## File Structure

```
Cyber-Threat-Detection/
├── app.py                    # Flask backend server
├── index.html                # Frontend interface
├── requirements.txt          # Python dependencies (updated with Flask)
├── saved_models/             # Trained models from Phase 1
│   ├── svm_model.pkl
│   ├── rf_model.pkl
│   ├── scaler.pkl
│   ├── label_encoder.pkl
│   └── feature_info.pkl
├── CSV/CSV/                  # Original dataset (for sample data)
└── DEMO_README.md           # This file
```

## Support

If you encounter any issues:
1. Check that all Phase 1 models are trained and saved
2. Verify the CSV dataset is in the correct location
3. Ensure all dependencies are installed
4. Check the terminal output for specific error messages