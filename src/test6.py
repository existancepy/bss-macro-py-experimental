from PIL import Image

# Load image
for i in range(2, 11):
    image = Image.open(f"images/buffs/counts-old/{i}.png").convert("RGBA")
    pixels = image.load()

    width, height = image.size

    # Target RGB color to keep
    target_rgb = (243, 243, 243)

    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if (r, g, b) != target_rgb:
                # Make it fully transparent
                pixels[x, y] = (0, 0, 0, 0)

    # Save the result
    image.save(f"{i}.png")
    print(f"Saved {i}.png")
