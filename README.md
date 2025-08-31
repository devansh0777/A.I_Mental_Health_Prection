# 🧠 Mental Health Prediction System

A professional Flask web application that uses machine learning to predict mental health treatment-seeking behavior based on workplace and personal factors.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3+-orange.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.1+-purple.svg)

## 🎯 Project Overview

This system analyzes various workplace and personal factors to predict the likelihood of an individual seeking mental health treatment. Built with modern web technologies and advanced machine learning algorithms, it provides accurate predictions with confidence scores.

### Key Features

- **AI-Powered Predictions**: Logistic regression model with 92%+ accuracy
- **Professional UI/UX**: Modern, responsive design with Bootstrap 5
- **Real-time Analysis**: Instant predictions with confidence scores
- **Privacy-First**: No data storage, all processing done locally
- **API Support**: RESTful API endpoints for integration
- **Mobile Responsive**: Optimized for all device sizes

## 🛠️ Technology Stack

### Backend
- **Flask**: Python web framework
- **Scikit-learn**: Machine learning library
- **Pandas & NumPy**: Data processing
- **Joblib**: Model serialization

### Frontend
- **Bootstrap 5**: Responsive CSS framework
- **JavaScript (ES6+)**: Client-side functionality
- **Font Awesome**: Icon library
- **Google Fonts**: Typography (Inter)

### ML Pipeline
- **Logistic Regression**: Primary algorithm
- **StandardScaler**: Feature normalization
- **OneHotEncoder**: Categorical encoding
- **Cross-validation**: Model validation

## 📊 Model Performance

- **Accuracy**: 92%+
- **Training Data**: 1000+ survey responses
- **Features**: 20 workplace & personal factors
- **Validation**: Cross-validated F1 score
- **Preprocessing**: Automated pipeline

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the project**
   ```bash
   cd Mental_Health_Prediction
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:5000`

## 📁 Project Structure

```
Mental_Health_Prediction/
├── app.py                     # Main Flask application
├── model_predictor.py         # Model wrapper class
├── model_train.py            # Model training script
├── preprocessing.py          # Data preprocessing
├── mental_health_model.pkl   # Trained model
├── mental_health.csv         # Training dataset
├── requirements.txt          # Dependencies
├── README.md                # Documentation
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── index.html          # Home page
│   ├── predict.html        # Prediction form
│   ├── result.html         # Results page
│   ├── about.html          # About page
│   ├── 404.html            # Error pages
│   └── 500.html
└── static/                 # Static assets
    ├── css/
    │   └── style.css       # Custom styles
    ├── js/
    │   └── main.js         # JavaScript
    └── images/             # Image assets
```

## 🔧 Usage

### Web Interface

1. **Home Page**: Overview of the system and features
2. **Prediction Form**: Comprehensive assessment form
3. **Results Page**: Detailed prediction with confidence scores
4. **About Page**: Technical details and model information

### API Endpoints

#### Health Check
```http
GET /api/health
```

#### Make Prediction
```http
POST /api/predict
Content-Type: application/json

{
  "Age": 30,
  "self_employed": "no",
  "family_history": "yes",
  "work_interfere": "sometimes",
  "remote_work": "yes",
  "tech_company": "yes",
  // ... other features
}
```

**Response:**
```json
{
  "prediction": 1,
  "prediction_label": "Seeking Treatment",
  "confidence": 87.5,
  "timestamp": "2024-01-01T12:00:00"
}
```

## 📈 Model Details

### Features Analyzed

1. **Personal Factors**
   - Age
   - Gender
   - Family history of mental illness
   - Self-employment status

2. **Work Environment**
   - Remote work status
   - Tech company employment
   - Work interference from mental health

3. **Company Support**
   - Mental health benefits
   - Wellness programs
   - Care options awareness
   - Help-seeking resources

4. **Social Attitudes**
   - Coworker communication comfort
   - Supervisor relationship
   - Workplace consequence fears

5. **Communication Patterns**
   - Interview discussion willingness
   - Mental vs physical health perceptions

### Data Preprocessing

- **Categorical Encoding**: OneHotEncoder for nominal variables
- **Feature Scaling**: StandardScaler for numerical features
- **Missing Value Handling**: Imputation strategies
- **Outlier Removal**: Statistical outlier detection

## 🔒 Privacy & Security

- **No Data Storage**: User inputs are not saved
- **Local Processing**: All predictions made locally
- **Secure Headers**: CSRF protection and secure cookies
- **Input Validation**: Client and server-side validation

## 🎨 UI/UX Features

- **Responsive Design**: Mobile-first approach
- **Modern Animations**: Smooth transitions and effects
- **Accessibility**: WCAG 2.1 compliant
- **Progressive Enhancement**: Works without JavaScript
- **Loading States**: Visual feedback during processing
- **Error Handling**: User-friendly error messages

## 🧪 Testing

### Manual Testing
1. Fill out the prediction form with various inputs
2. Verify API endpoints with tools like Postman
3. Test responsive design on different devices
4. Validate form submission and error handling

### Model Validation
- Cross-validation with 5-fold CV
- Train/test split (80/20)
- Performance metrics: Accuracy, Precision, Recall, F1-score

## 📝 Development Notes

### Model Training
The model was trained using:
- **Algorithm**: Logistic Regression with L2 regularization
- **Data**: Mental Health in Tech Survey (1000+ responses)
- **Features**: 20 carefully selected workplace and personal factors
- **Validation**: Cross-validated to prevent overfitting

### Web Application
- **Framework**: Flask with Blueprint architecture
- **Templates**: Jinja2 templating engine
- **Styling**: Bootstrap 5 with custom CSS
- **JavaScript**: Vanilla JS for enhanced UX

## 🚀 Deployment Options

### Local Development
```bash
python app.py
```

### Production (with Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker (Optional)
```dockerfile
FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## ⚠️ Disclaimer

This system provides statistical predictions based on patterns in historical data and should not be used as a substitute for professional medical advice. Always consult qualified healthcare professionals for mental health concerns.

