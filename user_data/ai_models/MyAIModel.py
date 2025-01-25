import logging
from typing import Any
from xgboost import XGBRFRegressor
from sklearn.model_selection import train_test_split
from freqtrade.freqai.base_models.BaseRegressionModel import BaseRegressionModel
from freqtrade.freqai.data_kitchen import FreqaiDataKitchen
import numpy as np
from sklearn.metrics import mean_absolute_error

logger = logging.getLogger(__name__)

class EnhancedXGBoostRFRegressor(BaseRegressionModel):
    """
    Ulepszony model predykcyjny na bazie XGBoost Random Forest.
    Model ten dodaje zaawansowaną inżynierię cech i optymalizację.
    """

    def fit(self, data_dictionary: dict, dk: FreqaiDataKitchen, **kwargs) -> Any:
        """
        Trenuje model XGBoost RF z dodatkowymi parametrami i technikami optymalizacji
        :param data_dictionary: słownik zawierający dane do treningu, testu oraz etykiety
        :param dk: Obiekt FreqaiDataKitchen
        """
        
        # Przygotowanie danych treningowych
        X = data_dictionary["train_features"]
        y = data_dictionary["train_labels"]

        # Inżynieria cech (możemy dodać więcej cech lub normalizować dane)
        X = self.feature_engineering(X)
        
        # Podział danych na zestawy treningowe i walidacyjne
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42)
        
        # Definiowanie parametrów modelu
        model_params = {
            'n_estimators': 100, 
            'max_depth': 6, 
            'learning_rate': 0.05,
            'subsample': 0.9,
            'colsample_bytree': 0.8,
            'random_state': 42
        }
        
        model = XGBRFRegressor(**model_params)

        # Trenowanie modelu
        model.fit(
            X=X_train,
            y=y_train,
            eval_set=[(X_val, y_val)],
            early_stopping_rounds=10,  # Zatrzymanie treningu przy braku poprawy
            verbose=True
        )

        # Monitorowanie wydajności
        y_pred = model.predict(X_val)
        mae = mean_absolute_error(y_val, y_pred)
        logger.info(f"Mean Absolute Error (MAE): {mae}")
        
        # Zwrócenie wytrenowanego modelu
        return model

    def feature_engineering(self, X: np.ndarray) -> np.ndarray:
        """
        Funkcja inżynierii cech. Można tu dodać dodatkowe cechy lub normalizację danych.
        :param X: macierz cech
        :return: zmodyfikowana macierz cech
        """
        # Przykład: normalizacja danych
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)
        
        # Można dodać dodatkowe cechy, np. logarytmiczne przekształcenia, różnice cen, itp.
        # Przykład dodania różnic cenowych
        X_diff = np.diff(X_scaled, axis=0)
        X_final = np.hstack((X_scaled[1:], X_diff))  # Łączenie skalowanych danych i różnic

        return X_final

    def predict(self, model: Any, data_dictionary: dict) -> np.ndarray:
        """
        Funkcja predykcji wykorzystująca wytrenowany model
        :param model: wytrenowany model
        :param data_dictionary: słownik zawierający dane do predykcji
        :return: prognozy modelu
        """
        X = data_dictionary["test_features"]
        X = self.feature_engineering(X)  # Zastosowanie tej samej inżynierii cech do danych testowych
        return model.predict(X)

    def decide(self, predictions: np.ndarray, threshold: float = 0.5) -> int:
        """
        Funkcja decyzyjna na podstawie predykcji modelu.
        :param predictions: prognozy modelu (np. zmiana ceny)
        :param threshold: próg decyzyjny
        :return: 1 - zakup, -1 - sprzedaż, 0 - brak decyzji
        """
        if np.mean(predictions) > threshold:
            return 1  # Sygnał kupna
        elif np.mean(predictions) < -threshold:
            return -1  # Sygnał sprzedaży
        else:
            return 0  # Brak decyzji

