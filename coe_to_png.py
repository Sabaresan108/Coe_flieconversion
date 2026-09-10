from PIL import Image

input_coe = '640x480.coe'         # Your original 24-bit COE file
output_image = 'real_colors.png'  # The image file we will generate

pixels = []

print(f"Reading {input_coe} and extracting RGB values...")
with open(input_coe, 'r') as f:
    for line in f:
        line = line.strip()
        # Skip the Vivado initialization headers
        if line.startswith('memory_initialization') or not line:
            continue
            
        # Strip away commas and semicolons
        hex_str = line.rstrip(',;')
        
        # If it's a 24-bit hex value, slice it into Red, Green, and Blue
        if len(hex_str) == 6:
            r = int(hex_str[0:2], 16)
            g = int(hex_str[2:4], 16)
            b = int(hex_str[4:6], 16)
            pixels.append((r, g, b))

print(f"Extracted {len(pixels)} pixels. Rebuilding image...")

# Create a new 640x480 RGB image
width, height = 640, 480
img = Image.new('RGB', (width, height))

# Slot the pixels into the image and save it
img.putdata(pixels[:width*height])
img.save(output_image)

print(f"Success! Open {output_image} to see the exact original colors.")
