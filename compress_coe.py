input_coe = '640x480.coe'  # Your original 24-bit source COE
output_coe = 'image_640x480_color.coe'

# Exact 16-color RGB palette matching your Verilog case statement
palette = {
    0: (0, 0, 0),  # Black
    1: (255, 255, 255),  # White
    2: (255, 255, 0),  # Yellow
    3: (0, 255, 255),  # Cyan
    4: (0, 255, 0),  # Green
    5: (255, 0, 255),  # Magenta
    6: (255, 0, 0),  # Red
    7: (0, 0, 255),  # Blue
    8: (255, 128, 0),  # Orange
    9: (128, 255, 0),  # Light green
    10: (0, 255, 128),  # Light greenish blue
    11: (128, 0, 255),  # Purple
    12: (255, 0, 128),  # Pink
    13: (0, 128, 0),  # Dark green
    14: (128, 192, 0),  # Leaf green
    15: (128, 128, 128),  # Gray
}


def get_closest_color(r, g, b):
  min_dist = float('inf')
  best_idx = 0
  for idx, (pr, pg, pb) in palette.items():
    dist = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
    if dist < min_dist:
      min_dist = dist
      best_idx = idx
  return best_idx


pixels_4bit = []
print(f'Parsing {input_coe}...')

with open(input_coe, 'r') as f:
  lines = f.readlines()

vector_started = False
for line in lines:
  line = line.strip()
  if 'memory_initialization_vector=' in line:
    vector_started = True
    continue
  if vector_started and line:
    val_str = line.rstrip(',;')
    if val_str:
      hex_val = int(val_str, 16)
      r = (hex_val >> 16) & 0xFF
      g = (hex_val >> 8) & 0xFF
      b = hex_val & 0xFF
      pixels_4bit.append(get_closest_color(r, g, b))

# Pack 4 pixels per 16-bit word
words = []
for i in range(0, len(pixels_4bit), 4):
  word = 0
  for p in range(4):
    c = pixels_4bit[i + p] if (i + p) < len(pixels_4bit) else 0
    word = (word << 4) | c
  words.append(f'{word:04X}')

# Pad to exactly 76,800 words
while len(words) < 76800:
  words.append('0000')
if len(words) > 76800:
  words = words[:76800]

with open(output_coe, 'w') as f:
  f.write('memory_initialization_radix=16;\n')
  f.write('memory_initialization_vector=\n')
  f.write(',\n'.join(words) + ';\n')

print(f'Done. {output_coe} created with {len(words)} entries.')
