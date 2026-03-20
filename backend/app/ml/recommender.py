import pandas as pd
import numpy as np
from typing import List, Dict, Any
from sklearn.metrics.pairwise import cosine_similarity

class FitnessRecommender:
    """
    Content-Based Recommendation Engine using Scikit-Learn.
    Computes similarity scores between users based on their fitness profiles.
    """
    
    def __init__(self):
        self.user_data = None
        self.feature_matrix = None
        self.user_ids = []
        
    def _encode_multilabel(self, df: pd.DataFrame, column: str) -> pd.DataFrame:
        """Helper to create dummy variables for list-like columns (Multi-hot encoding)"""
        # Explode list column to separate rows, get dummies, then sum back by index
        df_exploded = df[[column]].explode(column)
        dummies = pd.get_dummies(df_exploded[column], prefix=column)
        return dummies.groupby(dummies.index).sum()

    def fit(self, profiles: List[Dict[str, Any]]):
        """
        Fit the model with current user profiles.
        Expects a list of dictionaries with profile data.
        """
        if not profiles:
            return
            
        df = pd.DataFrame(profiles)
        self.user_ids = df['user_id'].tolist()
        
        # Base features
        features = []
        
        # 1. Fitness Level (Ordinal encoding logic or One-hot)
        if 'fitness_level' in df.columns:
            level_map = {"beginner": 1, "intermediate": 2, "advanced": 3}
            df['level_numeric'] = df['fitness_level'].map(level_map).fillna(1)
            # Normalize to 0-1
            df['level_numeric'] = df['level_numeric'] / 3.0
            features.append(df[['level_numeric']])
            
        # 2. Preferred Schedule (One-hot)
        if 'preferred_schedule' in df.columns:
            schedule_dummies = pd.get_dummies(df['preferred_schedule'], prefix='schedule')
            features.append(schedule_dummies)
            
        # 3. Goals (Multi-hot)
        if 'goals' in df.columns:
            goals_df = self._encode_multilabel(df, 'goals')
            features.append(goals_df)
            
        # 4. Workout Types (Multi-hot)
        if 'workout_types' in df.columns:
            types_df = self._encode_multilabel(df, 'workout_types')
            features.append(types_df)
            
        # 5. Preferred Days (Multi-hot)
        if 'preferred_days' in df.columns:
            days_df = self._encode_multilabel(df, 'preferred_days')
            features.append(days_df)
            
        # Concatenate all features
        if features:
            self.user_data = pd.concat(features, axis=1).fillna(0)
            # Calculate similarity matrix
            self.feature_matrix = cosine_similarity(self.user_data)
        else:
            self.feature_matrix = np.array([])
            
    def get_recommendations(self, target_user_id: str, top_n: int = 10) -> List[Dict[str, float]]:
        """
        Get top N recommendations for a specific user ID based on fitted data.
        """
        if self.feature_matrix is None or len(self.feature_matrix) == 0:
            return []
            
        if target_user_id not in self.user_ids:
            return []
            
        user_index = self.user_ids.index(target_user_id)
        
        # Get similarity scores for the target user
        similarity_scores = list(enumerate(self.feature_matrix[user_index]))
        
        # Sort by similarity score descending (exclude self)
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for idx, score in similarity_scores:
            matched_user_id = self.user_ids[idx]
            if matched_user_id == target_user_id:
                continue
                
            # Convert np float to python float
            recommendations.append({
                "user_id": matched_user_id,
                "score": float(score) * 100.0  # Percentage
            })
            
            if len(recommendations) >= top_n:
                break
                
        return recommendations
