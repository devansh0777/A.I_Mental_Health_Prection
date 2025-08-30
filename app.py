from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import joblib
import pandas as pd
import numpy as np
from model_predictor import MentalHealthPredictor
import logging
from datetime import datetime
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Initialize the predictor
try:
    predictor = MentalHealthPredictor('mental_health_model.pkl')
    logger.info("Model loaded successfully")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    predictor = None

@app.route('/')
def home():
    """Home page with project overview"""
    return render_template('index.html')

@app.route('/predict')
def predict_form():
    """Display the prediction form"""
    return render_template('predict.html')

@app.route('/submit_prediction', methods=['POST'])
def submit_prediction():
    """Handle form submission and make prediction"""
    try:
        if predictor is None:
            flash('Model not available. Please try again later.', 'error')
            return redirect(url_for('predict_form'))
        
        # Get form data
        form_data = {
            'Age': int(request.form.get('age', 30)),
            'gender': request.form.get('gender'),  # Will be converted to one-hot in predictor
            'self_employed': request.form.get('self_employed'),
            'family_history': request.form.get('family_history'),
            'work_interfere': request.form.get('work_interfere'),
            'remote_work': request.form.get('remote_work'),
            'tech_company': request.form.get('tech_company'),
            'benefits': request.form.get('benefits'),
            'care_options': request.form.get('care_options'),
            'wellness_program': request.form.get('wellness_program'),
            'seek_help': request.form.get('seek_help'),
            'mental_health_consequence': request.form.get('mental_health_consequence'),
            'phys_health_consequence': request.form.get('phys_health_consequence'),
            'coworkers': request.form.get('coworkers'),
            'supervisor': request.form.get('supervisor'),
            'mental_health_interview': request.form.get('mental_health_interview'),
            'phys_health_interview': request.form.get('phys_health_interview'),
            'mental_vs_physical': request.form.get('mental_vs_physical'),
        }
        
        # Make prediction
        prediction, confidence = predictor.predict(form_data)
        
        # Prepare result data
        result = {
            'prediction': 'Seeking Treatment' if prediction == 1 else 'Not Seeking Treatment',
            'confidence': round(confidence * 100, 2),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'form_data': form_data
        }
        
        return render_template('result.html', result=result)
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        flash('An error occurred while processing your request. Please try again.', 'error')
        return redirect(url_for('predict_form'))

@app.route('/api/predict', methods=['POST'])
def api_predict():
    """API endpoint for predictions"""
    try:
        if predictor is None:
            return jsonify({'error': 'Model not available'}), 500
        
        data = request.json
        prediction, confidence = predictor.predict(data)
        
        return jsonify({
            'prediction': int(prediction),
            'prediction_label': 'Seeking Treatment' if prediction == 1 else 'Not Seeking Treatment',
            'confidence': round(confidence * 100, 2),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"API prediction error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/about')
def about():
    """About page with project details"""
    return render_template('about.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings('ignore', category=UserWarning)
    app.run(debug=True, host='0.0.0.0', port=8081)
