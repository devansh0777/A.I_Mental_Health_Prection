import joblib
import pandas as pd
import numpy as np
import logging
import warnings
from typing import Dict, Tuple, Any

# Suppress sklearn version warnings
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

logger = logging.getLogger(__name__)

class MentalHealthPredictor:
    """
    A wrapper class for the mental health prediction model that handles
    data preprocessing and predictions.
    """
    
    def __init__(self, model_path: str):
        """
        Initialize the predictor with a trained model.
        
        Args:
            model_path (str): Path to the saved model file
        """
        self.model_path = model_path
        self.model = None
        self.feature_names = None
        self._load_model()
        self._setup_feature_mapping()
    
    def _load_model(self):
        """Load the trained model from file"""
        try:
            self.model = joblib.load(self.model_path)
            logger.info(f"Model loaded successfully from {self.model_path}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def _setup_feature_mapping(self):
        """Setup feature names and mapping for the model"""
        # These should match the features used during training
        self.categorical_mappings = {
            'self_employed': {'no': 0, 'yes': 1},
            'family_history': {'no': 0, 'yes': 1},
            'work_interfere': {
                'never': 0, 'rarely': 1, 'sometimes': 2, 'often': 3
            },
            'remote_work': {'no': 0, 'yes': 1},
            'tech_company': {'no': 0, 'yes': 1},
            'benefits': {
                'no': 0, 'yes': 1, "don't know": 2, 'not sure': 2
            },
            'care_options': {
                'no': 0, 'yes': 1, "don't know": 2, 'not sure': 2
            },
            'wellness_program': {
                'no': 0, 'yes': 1, "don't know": 2, 'not sure': 2
            },
            'seek_help': {
                'no': 0, 'yes': 1, "don't know": 2, 'not sure': 2
            },
            'mental_health_consequence': {
                'no': 0, 'maybe': 1, 'yes': 2
            },
            'phys_health_consequence': {
                'no': 0, 'maybe': 1, 'yes': 2
            },
            'coworkers': {
                'no': 0, 'some of them': 1, 'yes': 2
            },
            'supervisor': {
                'no': 0, 'some of them': 1, 'yes': 2
            },
            'mental_health_interview': {
                'no': 0, 'maybe': 1, 'yes': 2
            },
            'phys_health_interview': {
                'no': 0, 'maybe': 1, 'yes': 2
            },
            'mental_vs_physical': {
                'no': 0, "don't know": 1, 'yes': 2
            }
        }
    
    def _preprocess_input(self, input_data: Dict[str, Any]) -> pd.DataFrame:
        """
        Preprocess input data to match training format.
        
        Args:
            input_data (Dict): Raw input data from form
            
        Returns:
            pd.DataFrame: Preprocessed data ready for prediction
        """
        try:
            # Create a copy of input data and extract Age
            age = input_data.get('Age', 30)  # Default to 30 if missing
            gender_female = input_data.get('Gender_female', 0)
            gender_male = input_data.get('Gender_male', 0)
            gender_other = input_data.get('Gender_other', 0)
            
            # Handle gender if it's a single field
            if 'gender' in input_data:
                gender_value = str(input_data['gender']).lower().strip()
                gender_female = 1 if gender_value == 'female' else 0
                gender_male = 1 if gender_value == 'male' else 0
                gender_other = 1 if gender_value == 'other' else 0
            
            # One-hot encode all categorical features
            processed_data = {
                'Age': age,
                'Gender_female': gender_female,
                'Gender_male': gender_male,
                'Gender_other': gender_other,
            }
            
            # Binary one-hot encodings (features with Yes/No values)
            binary_features = {
                'self_employed': 'self_employed_yes',
                'family_history': 'family_history_yes',
                'remote_work': 'remote_work_yes',
                'tech_company': 'tech_company_yes'
            }
            
            for original_name, encoded_name in binary_features.items():
                if original_name in input_data:
                    value = str(input_data[original_name]).lower().strip()
                    processed_data[encoded_name] = 1.0 if value == 'yes' else 0.0
                else:
                    processed_data[encoded_name] = 0.0
            
            # Handle work_interfere (never, rarely, sometimes, often)
            work_interfere_values = ['often', 'rarely', 'sometimes']
            if 'work_interfere' in input_data:
                value = str(input_data['work_interfere']).lower().strip()
                for option in work_interfere_values:
                    processed_data[f'work_interfere_{option}'] = 1.0 if value == option else 0.0
            else:
                for option in work_interfere_values:
                    processed_data[f'work_interfere_{option}'] = 0.0
            
            # Handle benefits (no, yes, don't know)
            if 'benefits' in input_data:
                value = str(input_data['benefits']).lower().strip()
                processed_data['benefits_no'] = 1.0 if value == 'no' else 0.0
                processed_data['benefits_yes'] = 1.0 if value == 'yes' else 0.0
            else:
                processed_data['benefits_no'] = 0.0
                processed_data['benefits_yes'] = 0.0
            
            # Handle care_options (no, yes, not sure)
            if 'care_options' in input_data:
                value = str(input_data['care_options']).lower().strip()
                processed_data['care_options_not sure'] = 1.0 if value == 'not sure' else 0.0
                processed_data['care_options_yes'] = 1.0 if value == 'yes' else 0.0
            else:
                processed_data['care_options_not sure'] = 0.0
                processed_data['care_options_yes'] = 0.0
            
            # Handle wellness_program (no, yes)
            if 'wellness_program' in input_data:
                value = str(input_data['wellness_program']).lower().strip()
                processed_data['wellness_program_no'] = 1.0 if value == 'no' else 0.0
                processed_data['wellness_program_yes'] = 1.0 if value == 'yes' else 0.0
            else:
                processed_data['wellness_program_no'] = 0.0
                processed_data['wellness_program_yes'] = 0.0
            
            # Handle seek_help (no, yes)
            if 'seek_help' in input_data:
                value = str(input_data['seek_help']).lower().strip()
                processed_data['seek_help_no'] = 1.0 if value == 'no' else 0.0
                processed_data['seek_help_yes'] = 1.0 if value == 'yes' else 0.0
            else:
                processed_data['seek_help_no'] = 0.0
                processed_data['seek_help_yes'] = 0.0
            
            # Handle mental_health_consequence (no, yes)
            if 'mental_health_consequence' in input_data:
                value = str(input_data['mental_health_consequence']).lower().strip()
                processed_data['mental_health_consequence_no'] = 1.0 if value == 'no' else 0.0
                processed_data['mental_health_consequence_yes'] = 1.0 if value == 'yes' else 0.0
            else:
                processed_data['mental_health_consequence_no'] = 0.0
                processed_data['mental_health_consequence_yes'] = 0.0
            
            # Handle phys_health_consequence (no, yes)
            if 'phys_health_consequence' in input_data:
                value = str(input_data['phys_health_consequence']).lower().strip()
                processed_data['phys_health_consequence_no'] = 1.0 if value == 'no' else 0.0
                processed_data['phys_health_consequence_yes'] = 1.0 if value == 'yes' else 0.0
            else:
                processed_data['phys_health_consequence_no'] = 0.0
                processed_data['phys_health_consequence_yes'] = 0.0
            
            # Handle coworkers (no, some of them, yes)
            if 'coworkers' in input_data:
                value = str(input_data['coworkers']).lower().strip()
                processed_data['coworkers_some of them'] = 1.0 if value == 'some of them' else 0.0
                processed_data['coworkers_yes'] = 1.0 if value == 'yes' else 0.0
            else:
                processed_data['coworkers_some of them'] = 0.0
                processed_data['coworkers_yes'] = 0.0
            
            # Handle supervisor (no, some of them, yes)
            if 'supervisor' in input_data:
                value = str(input_data['supervisor']).lower().strip()
                processed_data['supervisor_some of them'] = 1.0 if value == 'some of them' else 0.0
                processed_data['supervisor_yes'] = 1.0 if value == 'yes' else 0.0
            else:
                processed_data['supervisor_some of them'] = 0.0
                processed_data['supervisor_yes'] = 0.0
            
            # Handle mental_health_interview (no, yes)
            if 'mental_health_interview' in input_data:
                value = str(input_data['mental_health_interview']).lower().strip()
                processed_data['mental_health_interview_no'] = 1.0 if value == 'no' else 0.0
                processed_data['mental_health_interview_yes'] = 1.0 if value == 'yes' else 0.0
            else:
                processed_data['mental_health_interview_no'] = 0.0
                processed_data['mental_health_interview_yes'] = 0.0
            
            # Handle phys_health_interview (no, yes)
            if 'phys_health_interview' in input_data:
                value = str(input_data['phys_health_interview']).lower().strip()
                processed_data['phys_health_interview_no'] = 1.0 if value == 'no' else 0.0
                processed_data['phys_health_interview_yes'] = 1.0 if value == 'yes' else 0.0
            else:
                processed_data['phys_health_interview_no'] = 0.0
                processed_data['phys_health_interview_yes'] = 0.0
            
            # Handle mental_vs_physical (no, yes)
            if 'mental_vs_physical' in input_data:
                value = str(input_data['mental_vs_physical']).lower().strip()
                processed_data['mental_vs_physical_no'] = 1.0 if value == 'no' else 0.0
                processed_data['mental_vs_physical_yes'] = 1.0 if value == 'yes' else 0.0
            else:
                processed_data['mental_vs_physical_no'] = 0.0
                processed_data['mental_vs_physical_yes'] = 0.0
            
            # Create DataFrame
            df = pd.DataFrame([processed_data])
            
            # Expected feature list (order matters for the model)
            expected_features = [
                'Age', 'Gender_female', 'Gender_male', 'Gender_other',
                'self_employed_yes', 'family_history_yes', 'work_interfere_often',
                'work_interfere_rarely', 'work_interfere_sometimes', 'remote_work_yes',
                'tech_company_yes', 'benefits_no', 'benefits_yes', 'care_options_not sure',
                'care_options_yes', 'wellness_program_no', 'wellness_program_yes',
                'seek_help_no', 'seek_help_yes', 'mental_health_consequence_no',
                'mental_health_consequence_yes', 'phys_health_consequence_no',
                'phys_health_consequence_yes', 'coworkers_some of them', 'coworkers_yes',
                'supervisor_some of them', 'supervisor_yes', 'mental_health_interview_no',
                'mental_health_interview_yes', 'phys_health_interview_no',
                'phys_health_interview_yes', 'mental_vs_physical_no', 'mental_vs_physical_yes'
            ]
            
            # Ensure all expected features are present (add any missing ones)
            for feature in expected_features:
                if feature not in df.columns:
                    df[feature] = 0.0
            
            # Reorder columns to match the expected order
            df = df[expected_features]
            
            logger.info(f"Input preprocessed successfully. Shape: {df.shape}")
            return df
            
        except Exception as e:
            logger.error(f"Preprocessing error: {e}")
            raise
    
    def predict(self, input_data: Dict[str, Any]) -> Tuple[int, float]:
        """
        Make a prediction for mental health treatment seeking.
        
        Args:
            input_data (Dict): Input features
            
        Returns:
            Tuple[int, float]: Prediction (0 or 1) and confidence score
        """
        try:
            if self.model is None:
                raise ValueError("Model not loaded")
            
            # Preprocess the input
            processed_df = self._preprocess_input(input_data)
            
            # Make prediction
            prediction = self.model.predict(processed_df)[0]
            
            # Get prediction probabilities for confidence
            try:
                probabilities = self.model.predict_proba(processed_df)[0]
                confidence = max(probabilities)
            except:
                # If predict_proba is not available, use decision function
                try:
                    decision_score = abs(self.model.decision_function(processed_df)[0])
                    confidence = min(max(decision_score / 10, 0.5), 1.0)  # Normalize to 0.5-1.0
                except:
                    confidence = 0.7  # Default confidence
            
            logger.info(f"Prediction made: {prediction}, Confidence: {confidence}")
            return int(prediction), float(confidence)
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise
    
    def get_feature_importance(self) -> Dict[str, float]:
        """
        Get feature importance if available from the model.
        
        Returns:
            Dict[str, float]: Feature importance scores
        """
        try:
            if hasattr(self.model, 'feature_importances_'):
                importance = self.model.feature_importances_
            elif hasattr(self.model, 'coef_'):
                importance = abs(self.model.coef_[0])
            else:
                return {}
            
            expected_features = [
                'Age', 'self_employed', 'family_history', 'work_interfere',
                'remote_work', 'tech_company', 'benefits', 'care_options',
                'wellness_program', 'seek_help', 'mental_health_consequence',
                'phys_health_consequence', 'coworkers', 'supervisor',
                'mental_health_interview', 'phys_health_interview',
                'mental_vs_physical', 'Gender_female', 'Gender_male', 'Gender_other'
            ]
            
            return dict(zip(expected_features, importance))
            
        except Exception as e:
            logger.error(f"Feature importance error: {e}")
            return {}
