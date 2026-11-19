print("ChromAI - AI that detects colors and announces it to you.")

while True:
    print("\n\n")
    try:
        r = int(input("Enter Red Value (RGB): "))
        g = int(input("Enter Green Value (RGB): "))
        b = int(input("Enter Blue Value (RGB): "))
    except ValueError:
        print("\nError! Try using numbers :)\n")
        continue
    except KeyboardInterrupt:
        "\nAwwh okay :(\n"
        break
    except:
        print("Huh, something might've happened!")
        continue
    
    color = None
    
    if r > 255 or g > 255 or b > 255:
        print("Max RGB value is 255 lah!")
        continue

    if r == 255 and g == 0 and b == 0:
        color = "Red"
    elif r == 255 and g == 255 and b == 0:
        color = "Yellow"
    elif r == 128 and g == 0 and b == 128:
        color = "Purple"
    elif r == 255 and g == 165 and b == 0:
        color = "Orange"
    elif r == 0 and g == 255 and b == 0:
        color = "Green"
    elif r == 0 and g == 0 and b == 255:
        color = "Blue"
    elif r == 255 and g == 255 and b == 255:
        color = "White"
    elif r == 0 and g == 0 and b == 0:
        color = "Black"
    else:
        print(f"""
    Our logic is dumb so the colors you entered are invalid :(
    This is what you entered though: ({r}, {g}, {b})
    """)
        continue
        
    print(f"\nYour color is: {color}!")
    choice = input("Try again? (y/n) ")
    if choice == "y":
        continue
    else:
        break
    