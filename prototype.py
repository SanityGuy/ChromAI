from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

data = Path("colors.txt").read_text(encoding="utf-8")

X = []
y = []

for line in data.strip().splitlines():
    if ":" not in line:
        continue
    name, rgb_str = line.split(":", 1)
    r, g, b = (int(v.strip()) for v in rgb_str.split(","))
    X.append((r, g, b))
    y.append(name.strip())

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

for rgb, actual, predicted in zip(X_test, y_test, predictions):
    print(f"RGB: {rgb} | Actual: {actual} | Predicted: {predicted}")

print(f"\nAccuracy: {model.score(X_test, y_test):.2f}")   