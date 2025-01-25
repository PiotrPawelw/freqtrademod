from freqtrade.ai import FreqAI
import pandas as pd

# Załaduj dane historyczne (tutaj przykład z pliku CSV, ale możesz użyć danych z Freqtrade)
data = pd.read_csv('path_to_your_historical_data.csv')

# Przygotowanie danych: wybierz odpowiednie kolumny
X_train = data[['open', 'high', 'low', 'close']]  # Przykład cech
y_train = data['target']  # 'target' może być kolumną np. 1 (kupno), 0 (sprzedaż)

# Tworzenie instancji modelu FreqAI
model = FreqAI()

# Trenowanie modelu
model.train(X_train, y_train)

# Zapisanie wytrenowanego modelu
model.save('my_trained_model.h5')
print("Model zapisany jako my_trained_model.h5")
