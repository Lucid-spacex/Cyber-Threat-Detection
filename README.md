# Enhanced Hybrid ML-Based Intrusion Detection System for IoT Networks

## Phase 1: Core Research Pipeline

This project implements a hybrid machine learning approach combining Support Vector Machine (SVM) and Random Forest (RF) for IoT network traffic classification using the CICIoT2023 dataset.

### Project Overview

**Goal**: Classify IoT network traffic as benign or malicious (33 attack types across 7 categories: DDoS, DoS, Recon, Web-based, Brute Force, Spoofing, Mirai)

**Dataset**: CICIoT2023 - ~46.7 million records, 39 flow-level features, 34 classes (Benign + 33 attack types)

### Project Structure

```
Cyber-Threat-Detection/
├── CSV/                          # CICIoT2023 dataset (8.33 GB)
│   └── CSV/                      # 34 class folders with CSV files
├── intrusion_detection_pipeline.ipynb  # Main Jupyter notebook (Phase 1)
├── requirements.txt              # Python dependencies
├── saved_models/                 # Trained models (created after running notebook)
└── README.md                     # This file
```

### Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Launch Jupyter notebook:
```bash
jupyter notebook intrusion_detection_pipeline.ipynb
```

### Phase 1 Deliverables

- **Complete ML Pipeline**: Data loading, preprocessing, feature selection, model training, and evaluation
- **Three Models**: SVM baseline, Random Forest baseline, and Hybrid (SVM+RF) with soft voting fusion
- **Comprehensive Evaluation**: Accuracy, precision, recall, F1-score, false positive rate, and prediction time
- **Benchmark Comparison**: Results compared against published literature
- **Academic Report Ready**: Detailed comments and results suitable for seminar project documentation

### Key Features

1. **Stratified Sampling**: Handles 46.7M rows by creating a representative 50K sample that preserves all 34 classes
2. **Smart Preprocessing**: Handles duplicates, missing values, encoding, and standardization
3. **Feature Selection**: Correlation-based filtering + Random Forest importance ranking
4. **Class Imbalance Handling**: Uses class weighting (computationally efficient) instead of resampling
5. **Hybrid Approach**: Soft voting fusion combines SVM and RF probability estimates

### Dataset Statistics

- **Total Records**: 46,776,700 rows
- **Classes**: 34 (1 Benign + 33 attack types)
- **Features**: 39 flow-level features
- **Class Imbalance**: ~5,751:1 ratio (largest:smallest)
- **Severe Imbalance**: DDoS-ICMP_Flood (7.2M rows) vs Uploading_Attack (1,252 rows)

### Results Summary

The notebook produces comprehensive performance metrics for all three models, including:
- Accuracy, Precision, Recall, F1-Score
- False Positive Rate
- Prediction time (total and per-sample)
- Detailed classification reports per class
- Comparison with published benchmarks

### Next Steps (Phase 2)

After successfully running Phase 1 and training the models, Phase 2 will implement a lightweight demo application:
- Flask/FastAPI backend to load trained models
- Simple HTML frontend for interactive predictions
- Demonstration of the hybrid model on sample inputs

### Academic Use

This project is designed as an HND (undergraduate-level) seminar project. The notebook includes:
- Beginner-friendly comments explaining each step
- Clear documentation of methodology and rationale
- Results formatted for academic report inclusion
- Honest discussion of limitations and computational constraints

### References

- CICIoT2023 Dataset: https://www.unb.ca/cic/datasets/iotdataset-2023.html
- Chen & Feng (2026), CNN-LSTM hybrid: >97% accuracy
- Obeidat & Shehab (2025), SVM+DNN hybrid: 96.38% detection rate

### Notes

- The notebook is designed to run on standard laptop hardware
- Training time: ~15-30 minutes depending on CPU
- Memory usage: ~2-4 GB during training
- All models are saved to disk for potential reuse in Phase 2