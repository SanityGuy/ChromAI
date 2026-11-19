import math
from pathlib import Path


class ColorRecognizer:
    def __init__(self, filepath="colors.txt"):
        self.filepath = Path(filepath)
        self.colors = self.load_colors(self.filepath)
        self.d_max = math.sqrt(3 * 255 ** 2)

    @staticmethod
    def load_colors(filepath):
        loaded = {}
        with open(filepath, "r", encoding="utf-8") as file:
            for line_num, raw_line in enumerate(file, start=1):
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue

                if ":" not in line:
                    raise ValueError(f"Invalid format on line {line_num}: {line}")

                name, rgb_part = line.split(":", 1)
                parts = [p.strip() for p in rgb_part.split(",")]

                if len(parts) != 3:
                    raise ValueError(f"Expected 3 RGB values on line {line_num}: {line}")

                r, g, b = (int(val) for val in parts)
                if not all(0 <= c <= 255 for c in (r, g, b)):
                    raise ValueError(f"RGB out of range (0-255) on line {line_num}: {line}")

                loaded[name.strip()] = (r, g, b)

        if not loaded:
            raise ValueError(f"No colors found in {filepath}")

        return loaded

    def calculate_distance(self, rgb):
        closest_color = min(
            self.colors,
            key=lambda c: sum((a - b) ** 2 for a, b in zip(self.colors[c], rgb))
        )
        distance = math.sqrt(
            sum((a - b) ** 2 for a, b in zip(self.colors[closest_color], rgb))
        )
        return closest_color, distance


def main():
    recognizer = ColorRecognizer("colors.txt")

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

        if r > 255 or g > 255 or b > 255:
            print("Max RGB value is 255 lah!")
            continue

        if r < 0 or g < 0 or b < 0:
            print("Min RGB value is 0 silly!")
            continue

        color, distance = recognizer.calculate_distance((r, g, b))

        if distance < 100:
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