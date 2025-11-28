import json
import os
# ----------------------------------------------------------
# Node class for building the Huffman Tree
# ----------------------------------------------------------
class Node:
    def __init__(self, char=None, freq=0):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
# ----------------------------------------------------------
# Step 1: Calculate frequency of each character in text
# ----------------------------------------------------------
def calculate_frequencies(text):
    frequencies = {}
    for char in text:
        frequencies[char] = frequencies.get(char, 0) + 1
    return frequencies
# ----------------------------------------------------------
# Step 2: Build Huffman Tree from frequencies
# ----------------------------------------------------------
def build_huffman_tree(frequencies):
    nodes = [Node(char, freq) for char, freq in frequencies.items()]

    if not nodes:
        return None  # Handle empty input

    while len(nodes) > 1:
        # Sort nodes by frequency (ascending order)
        nodes.sort(key=lambda x: x.freq)
        left = nodes.pop(0)
        right = nodes.pop(0)

        # Merge the two smallest nodes
        merged = Node(freq=left.freq + right.freq)
        merged.left = left
        merged.right = right
        nodes.append(merged)

    return nodes[0]  # Root of the tree
# ----------------------------------------------------------
# Step 3: Generate Huffman codes for each character
# ----------------------------------------------------------
def generate_huffman_codes(node, current_code="", codes=None):
    if codes is None:
        codes = {}

    if node is None:
        return codes
    # Leaf node → has a character
    if node.char is not None:
        codes[node.char] = current_code or "0"  # handle single-char case

    generate_huffman_codes(node.left, current_code + "0", codes)
    generate_huffman_codes(node.right, current_code + "1", codes)
    return codes
# ----------------------------------------------------------
# Step 4: Encode text using Huffman codes
# ----------------------------------------------------------
def huffman_encoding(text):
    frequencies = calculate_frequencies(text)
    root = build_huffman_tree(frequencies)

    if root is None:
        return "", {}

    codes = generate_huffman_codes(root)
    encoded_text = ''.join(codes[char] for char in text)
    return encoded_text, codes
# ----------------------------------------------------------
# Step 5: Decode Huffman encoded binary string
# ----------------------------------------------------------
def huffman_decoding(encoded_text, codes):
    code_to_char = {v: k for k, v in codes.items()}
    current_code = ""
    decoded_text = ""
    for bit in encoded_text:
        current_code += bit
        if current_code in code_to_char:
            decoded_text += code_to_char[current_code]
            current_code = ""
    return decoded_text
# ----------------------------------------------------------
# Step 6: Save compressed data as binary file
# ----------------------------------------------------------
def save_binary_file(encoded_text, filename):
   
    extra_bits = (8 - len(encoded_text) % 8) % 8

   
    encoded_text += "0" * extra_bits

   
    b = bytearray()
    b.append(extra_bits)

  
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i + 8]
        b.append(int(byte, 2))

    with open(filename, "wb") as f:
        f.write(b)
# ----------------------------------------------------------
# Step 7: Read binary file and convert to bit string
# ----------------------------------------------------------
def read_binary_file(filename):
    with open(filename, "rb") as f:
        
        extra_bits = ord(f.read(1))
        bits = ""

       
        byte = f.read(1)
        while byte:
            bits += f"{ord(byte):08b}"
            byte = f.read(1)

        
        if extra_bits:
            bits = bits[:-extra_bits]

    return bits
# checking path
def get_file_path(prompt, valid_exts):
    """Ask user for file path and validate its extension."""
    while True:
        path = input(prompt).strip('" ')
        ext = os.path.splitext(path)[1].lower()
        if ext in valid_exts:
            if os.path.exists(path):
                return path
            else:
                print(" File not found. Try again.")
        else:
            print(f" Invalid extension. Expected one of {valid_exts}")
# ----------------------------------------------------------
# Step 8: Main program (read → compress → save → decompress)
def main():
  
  while True:
    print(" Huffman Compression / Decompression ")
    choice = input("Do you want to (C)ompress or (D)ecompress? ").strip().lower()

    # Compression Mode
    if choice in ("c", "compress"):
        input_path = get_file_path("Enter input text file path: ", [".txt"])
        output_bin = input("Enter output binary file name (e.g., compressed.bin): ").strip()
        output_json = input("Enter codes file name (e.g., codes.json): ").strip()

        # --- Read original text ---
        with open(input_path, "r", encoding="utf-8") as file:
            text = file.read()

        print("\n Original text loaded.")
        original_size = len(text.encode("utf-8"))  
        print("Original size:", original_size, "bytes")

        # --- Compression ---
        encoded_text, codes = huffman_encoding(text)
        save_binary_file(encoded_text, output_bin)

        with open(output_json, "w") as f:
            json.dump(codes, f)

        compressed_size = os.path.getsize(output_bin)

        # --- Decompress immediately to verify ---
        encoded_bits = read_binary_file(output_bin)
        decoded_text = huffman_decoding(encoded_bits, codes)

        # Write decompressed result temporarily
        decompressed_path = "decompressed_check.txt"
        with open(decompressed_path, "w", encoding="utf-8") as f:
            f.write(decoded_text)

        # --- Comparison ---
        match = (text == decoded_text)

        # --- Display summary ---
        print("\n Compression done successfully!")
        print(f"Compressed data ,bin, saved at: {os.path.abspath(output_bin)}")
        print(f" Huffman codes saved at: {os.path.abspath(output_json)}")
        print(f"{'Files match perfectly!' if match else ' Mismatch detected between original and decompressed text.'}")
    # ----------------------------------------------------------
    # Decompression Mode
    # ----------------------------------------------------------
    elif choice in ("d", "decompress"):
        input_bin = get_file_path("Enter compressed binary file path: ", [".bin"])
        input_json = get_file_path("Enter codes JSON file path: ", [".json"])
        output_txt = input("Enter output decompressed text file name (e.g., decompressed.txt): ").strip()

        # --- Load compressed data ---
        encoded_bits = read_binary_file(input_bin)

        # --- Load Huffman codes ---
        with open(input_json, "r") as f:
            codes = json.load(f)

        # --- Decompression ---
        decoded_text = huffman_decoding(encoded_bits, codes)

        with open(output_txt, "w", encoding="utf-8") as f:
            f.write(decoded_text)

        print("\n Decompression done successfully!")
        print(f"Decompressed text saved at: {os.path.abspath(output_txt)}")

    else:
        print("Invalid choice! Please enter 'C' for compress or 'D' for decompress.")

    again = input("\nDo you want to perform another operation? (y/n): ").strip().lower()
    if again != "y":
        print("\n Program closed.")
        break
# ----------------------------------------------------------
if __name__ == "__main__":
    main()