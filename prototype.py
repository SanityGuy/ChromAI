from pathlib import Path
from sklearn.model_selection import train_test_split

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

print(f"X_train: {len(X_train)}")
print(f"X_test:  {len(X_test)}")
print(f"y_train: {len(y_train)}")
print(f"y_test:  {len(y_test)}")   