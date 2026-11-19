import math

colors = {
    "Red":         (255, 0, 0),
    "Green":       (0, 255, 0),
    "Blue":        (0, 0, 255),
    "White":       (255, 255, 255),
    "Black":       (0, 0, 0),
    "Orange":      (255, 165, 0),
    "Yellow":      (255, 255, 0),
    "Purple":      (128, 0, 128),
    "Cyan":        (0, 255, 255),
    "Magenta":     (255, 0, 255),
    "Pink":        (255, 192, 203),
    "Brown":       (165, 42, 42),
    "Navy":        (0, 0, 128),
    "Teal":        (0, 128, 128),
    "Gold":        (255, 215, 0),
    "Coral":       (255, 127, 80),
    "Lavender":    (230, 230, 250),
    "Olive":       (128, 128, 0),
    "Turquoise":   (64, 224, 208),
    "Crimson":     (220, 20, 60),
    "Maroon":      (128, 0, 0),
    "Lime":        (0, 255, 0),
    "Silver":      (192, 192, 192),
    "Gray":        (128, 128, 128),
    "Khaki":       (195, 176, 145),
    "Indigo":      (75, 0, 130),
    "Violet":      (238, 130, 238),
    "Salmon":      (250, 128, 114),
    "Scarlet":     (255, 36, 0),
    "Cerulean":    (0, 123, 167),
}   

while True:
    print("\nChromAI - AI that detects colors and announces it to you.")
    print("\n")
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
    except:
        print("Huh, something might've happened!")
        continue
    
    color = None
    
    if r > 255 or g > 255 or b > 255:
        print("Max RGB value is 255 lah!")
        continue
    
    if r < 0 or g < 0 or b < 0:
        print("Min RGB value is 0 silly!")
        continue

    color = min(colors, key=lambda c:sum((a - b) ** 2 for a,b in zip(colors[c], (r,g,b))))
    distance = math.sqrt(sum((a - b) ** 2 for a,b in zip(colors[color], (r,g,b))))

    if distance < 100:
        print(f"\nYour color is: {color}! (distance: {distance:.1f})")
    else:
        print(f"""
    Our logic is dumb so the colors you entered are invalid :(
    This is what you entered though: ({r}, {g}, {b})
    Closest guess: {color} (distance: {distance:.1f})
    """)
        continue
    
    choice = input("Try again? (y/n) ")
    if choice == "n":
        break
    else:
        continue
    