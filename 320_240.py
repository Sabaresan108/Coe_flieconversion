from PIL import Image
import os

# Define filenames
input_image = 'image.png' # <-- Change this to your actual image file
output_coe = 'image_320x240_bw.coe'

def generate_bw_coe():
    print(f"Loading {input_image}...")
    
    # 1. Load, convert to Grayscale ('L'), and resize to 320x240
    img = Image.open(input_image).convert('L').resize((320, 240))
    pixels = list(img.getdata())

    words = []
    
    # 2. Process and pack 4 pixels per 16-bit word
    for i in range(0, len(pixels), 4):
        word = 0
        for p in range(4):
            # Take the 8-bit pixel (0-255) and shift it to 4-bit (0-15)
            val = pixels[i + p] >> 4 
            
            # Shift the existing word left by 4 and append the new pixel
            word = (word << 4) | val
            
        # Format the word as a 4-digit uppercase Hex string
        words.append(f"{word:04X}")

    # 3. Ensure the word count is exactly 19,200
    if len(words) > 19200:
        words = words[:19200]
    while len(words) < 19200:
        words.append("0000")

    # 4. Write the Vivado COE format
    with open(output_coe, 'w') as f:
        f.write('memory_initialization_radix=16;\n')
        f.write('memory_initialization_vector=\n')
        
        # Join all words with a comma and newline, ending with a semicolon
        f.write(',\n'.join(words) + ';\n')

    print(f"Success! {output_coe} generated with {len(words)} words.")
    print("This will consume roughly 10 BRAM blocks.")

if __name__ == "__main__":
    if os.path.exists(input_image):
        generate_bw_coe()
    else:
        print(f"Error: Could not find '{input_image}'. Please check the filename.")
