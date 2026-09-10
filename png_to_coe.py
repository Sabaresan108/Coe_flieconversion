from PIL import Image

input_image_path = 'real_colors.png' # Double-check this points to the COLOR version!
output_coe = 'image_640x480_custom.coe'

print("Loading and converting image...")
img = Image.open(input_image_path).convert("RGB")
img = img.resize((640, 480))

# USE THIS NEW LINE: 
# method=1 (Max Coverage) and kmeans=5 forces it to group distinct colors (like red/green) 
# instead of letting the grays steal all 16 palette slots.
img_16 = img.quantize(colors=16, method=1, kmeans=5, dither=1)

# Extract the new custom palette
raw_palette = img_16.getpalette()[:16*3]

print("\n=== COPY THIS INTO YOUR VERILOG MODULE ===")
print("case (pixel_color)")
for i in range(16):
    r = raw_palette[i*3]
    g = raw_palette[i*3 + 1]
    b = raw_palette[i*3 + 2]
    
    # Scale 8-bit RGB to Zybo's 5-bit R, 6-bit G, 5-bit B
    r5 = r >> 3
    g6 = g >> 2
    b5 = b >> 3
    
    print(f"    4'd{i}: begin vga_r <= 5'd{r5}; vga_g <= 6'd{g6}; vga_b <= 5'd{b5}; end")
print("endcase")
print("==========================================\n")

# Pack the pixels into 16-bit words
pixels = list(img_16.getdata())
words = []
for i in range(0, len(pixels), 4):
    word = 0
    for p in range(4):
        c = pixels[i + p] if (i + p) < len(pixels) else 0
        word = (word << 4) | c
    words.append(f"{word:04X}")

# Pad to exactly 76,800 words
target_depth = 76800
while len(words) < target_depth:
    words.append("0000")
if len(words) > target_depth:
    words = words[:target_depth]

# Write COE
with open(output_coe, 'w') as f:
    f.write('memory_initialization_radix=16;\n')
    f.write('memory_initialization_vector=\n')
    f.write(',\n'.join(words) + ';\n')

print(f"Success! {output_coe} generated.")
