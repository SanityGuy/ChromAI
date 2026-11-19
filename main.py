import math
from pathlib import Path


class DatasetError(Exception):
    """Raised when the color dataset file is missing or malformed."""


class ColorRecognizer:
    def __init__(self, filepath="colors.txt", threshold=80.0):
        if isinstance(threshold, bool) or not isinstance(threshold, (int, float)) or threshold < 0:
            raise ValueError("Threshold must be a non-negative number.")

        self.filepath = Path(filepath)
        self.threshold = float(threshold)
        self.colors = self.load_colors(self.filepath)

    @staticmethod
    def validate_rgb(rgb):
        if not isinstance(rgb, (tuple, list)) or len(rgb) != 3:
            raise ValueError("RGB must contain exactly 3 values: (R, G, B).")

        r, g, b = rgb
        for channel, label in zip((r, g, b), ("Red", "Green", "Blue")):
            if isinstance(channel, bool) or not isinstance(channel, int):
                raise ValueError(f"{label} value must be an integer, got {channel!r}.")
            if channel < 0:
                raise ValueError(f"Min {label} value is 0 silly! (got {channel})")
            if channel > 255:
                raise ValueError(f"Max {label} value is 255 lah! (got {channel})")

        return (r, g, b)

    @classmethod
    def load_colors(cls, filepath):
        path = Path(filepath)
        try:
            raw_text = path.read_text(encoding="utf-8")
        except FileNotFoundError as exc:
            raise DatasetError(
                f"Color dataset not found at '{path.resolve()}'. "
                "Create 'colors.txt' or pass a valid file path."
            ) from exc
        except OSError as exc:
            raise DatasetError(f"Unable to read color dataset '{path}': {exc}") from exc

        loaded = {}
        for line_num, raw_line in enumerate(raw_text.splitlines(), start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue

            if ":" not in line:
                raise DatasetError(
                    f"Line {line_num} is missing ':'. Expected 'Name: R, G, B', got: {raw_line!r}"
                )

            name_part, rgb_part = line.split(":", 1)
            name = name_part.strip()
            if not name:
                raise DatasetError(
                    f"Line {line_num} has an empty color name. Expected 'Name: R, G, B', got: {raw_line!r}"
                )

            parts = [p.strip() for p in rgb_part.split(",")]
            if len(parts) != 3 or any(p == "" for p in parts):
                raise DatasetError(
                    f"Line {line_num} ('{name}') must have 3 comma-separated RGB values, got: {rgb_part!r}"
                )

            try:
                parsed_rgb = tuple(int(val) for val in parts)
            except ValueError as exc:
                raise DatasetError(
                    f"Line {line_num} ('{name}') has non-integer RGB values: {rgb_part!r}"
                ) from exc

            try:
                validated_rgb = cls.validate_rgb(parsed_rgb)
            except ValueError as exc:
                raise DatasetError(f"Line {line_num} ('{name}') failed RGB check: {exc}") from exc

            loaded[name] = validated_rgb

        if not loaded:
            raise DatasetError(
                f"No valid color entries found in '{path}'. Add lines formatted as 'Name: R, G, B'."
            )

        return loaded

    def calculate_distance(self, rgb):
        r, g, b = self.validate_rgb(rgb)
        target = (r, g, b)

        closest_color = min(
            self.colors,
            key=lambda c: sum((a - b_val) ** 2 for a, b_val in zip(self.colors[c], target))
        )
        distance = math.sqrt(
            sum((a - b_val) ** 2 for a, b_val in zip(self.colors[closest_color], target))
        )
        return closest_color, distance

    def classify(self, rgb):
        color, distance = self.calculate_distance(rgb)
        is_match = distance < self.threshold
        return color, distance, is_match


def main():
    try:
        recognizer = ColorRecognizer("colors.txt", threshold=80.0)
    except (DatasetError, ValueError) as exc:
        print(f"\nStartup Error: {exc}\n")
        return

    while True:
        print("\nChromAI - AI that detects colors and announces it to you.\n")
        try:
            r = int(input("Enter Red Value (RGB): "))
            g = int(input("Enter Green Value (RGB): "))
            b = int(input("Enter Blue Value (RGB): "))
        except ValueError:
            print("\nError! Try using numbers :)\n")
            continue
        except KeyboardInterrupt:
            print("\nAwwh okay :(\n")
            break

        try:
            color, distance, is_match = recognizer.classify((r, g, b))
        except ValueError as exc:
            print(f"\n{exc}\n")
            continue

        if is_match:
            print(f"\nYour color is: {color}! (distance: {distance:.1f})")
        else:
            print(f"""
    Our logic is dumb so the colors you entered are invalid :(
    This is what you entered though: ({r}, {g}, {b})
    Closest guess: {color} (distance: {distance:.1f})
    """)
            continue

        choice = input("Try again? (y/n) ").strip().lower()
        if choice == "n":
            break


if __name__ == "__main__":
    main()