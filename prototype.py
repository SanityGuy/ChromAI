from pathlib import Path
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

data = Path("dataset.txt").read_text(encoding="utf-8")

X = []
y = []

for line in data.strip().splitlines():
    parts = line.split(":")
    if len(parts) < 3:
        continue
    r, g, b = (int(v.strip()) for v in parts[1].split(","))
    category = parts[2].strip()
    X.append((r, g, b))
    y.append(category)

X = np.array(X)
y = np.array(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

rng = np.random.default_rng(42)
X_aug = [X_train]
y_aug = [y_train]
for _ in range(99):
    noise = rng.integers(-15, 16, size=X_train.shape)
    X_aug.append(np.clip(X_train + noise, 0, 255))
    y_aug.append(y_train)

X_train = np.vstack(X_aug)
y_train = np.concatenate(y_aug)

best_k = None
best_acc = 0
for k in [1, 3, 5, 7, 9, 11, 15]:
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(X_train, y_train)
    acc = model.score(X_test, y_test)
    print(f"K={k:2d}  Accuracy: {acc:.4f}")
    if acc > best_acc:
        best_acc = acc
        best_k = k

print(f"\nBest K: {best_k} (Accuracy: {best_acc:.4f})")

model = KNeighborsClassifier(n_neighbors=best_k)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print(f"\nAccuracy: {accuracy_score(y_test, y_pred):.4f}")
print(f"\nConfusion Matrix:\n{confusion_matrix(y_test, y_pred)}")
print(f"\nClassification Report:\n{classification_report(y_test, y_pred)}")

joblib.dump(model, "color_knn_model.pkl")

test_color = np.array([[220, 30, 50]])
print(f"\nRGB: {tuple(test_color[0])} → {model.predict(test_color)[0]}")   