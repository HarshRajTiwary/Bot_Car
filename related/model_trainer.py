import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
import pickle

file_path = "dataset/color_data.csv"
try:
    data = pd.read_csv(file_path)
except FileNotFoundError:
    print(f"Error: {file_path} not found.")
    exit()

X = data[["R", "G", "B"]]
y = data["Label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Accuracy: {accuracy:.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred))

model_file = "model/color_knn_model.pkl"
with open(model_file, "wb") as f:
    pickle.dump(knn, f)
print(f"Model saved to {model_file}")
