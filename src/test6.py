from PIL import Image

# Load image
image = Image.open(f"honeybar-built-in.png").convert("RGBA")
pixels = image.load()

width, height = image.size

# Target RGB color to keep
target_rgb = (27, 42, 53)

for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        if (r, g, b) != target_rgb:
            # Make it fully transparent
            pixels[x, y] = (0, 0, 0, 0)

# Save the result
image.save(f"output.png")
print(f"Saved ouput.png")
