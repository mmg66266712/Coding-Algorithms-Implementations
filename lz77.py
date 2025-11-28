# -----------------------------------------------------
# team7: Assignment 1 - LZ77 Compression and Decompression
# Members:
# - Member 1: Mariam Medhat, ID: 20230399
# - Member 2: Somaya Amr, ID: 20230179
# - Member 3: Fatema Ali, ID: 20230282
# -----------------------------------------------------
import pandas as pd

# -----------------------------------------------------
# Tag Class
# -----------------------------------------------------
class Tag:
    def __init__(self, position=0, length=0, next_char=''):
        self.position = position
        self.length = length
        self.next_char = next_char

    def __repr__(self):
        return f"({self.position}, {self.length}, '{self.next_char}')"


# -----------------------------------------------------
# LZ77 Compression Function
# -----------------------------------------------------
def lz77_compress(text, window_size=20):
    i = 0
    n = len(text)
    tags = []

    while i < n:
        start_index = max(0, i - window_size)
        search_buffer = text[start_index:i]
        lookahead = text[i:]

        best_distance = 0
        best_length = 0

        if search_buffer:
            for s in range(len(search_buffer)):
                pattern = search_buffer[s:]
                pat_len = len(pattern)
                if pat_len == 0:
                    continue

                L = 0
                while L < len(lookahead) and lookahead[L] == pattern[L % pat_len]:
                    L += 1

                if L == 0:
                    continue

                dist = len(search_buffer) - s
                if L > best_length or (L == best_length and dist < best_distance):
                    best_length = L
                    best_distance = dist

        if best_length < len(lookahead):
            next_char = lookahead[best_length]
        else:
            next_char = ''

        tags.append(Tag(best_distance, best_length, next_char))
        i += best_length + 1

    return tags


# -----------------------------------------------------
# Decompression Function
# -----------------------------------------------------
def decompress(tags):
    text = ""
    for tag in tags:
        if tag.position == 0 and tag.length == 0:
            text += tag.next_char
        else:
            start = len(text) - tag.position
            for i in range(tag.length):
                text += text[start + i]
            text += tag.next_char
    return text


# -----------------------------------------------------
# MAIN PROGRAM
# -----------------------------------------------------
def main():
    print("Welcome to LZ77 Compression Tool")

    while True:
        choice = input("\nDo you want to (1) Compress or (2) Decompress? Enter 1 or 2: ").strip()

        if choice not in ['1', '2']:
            print("invalid choice. Please enter 1 or 2.")
            continue

        # ---------------------------------------------
        # Compression Mode
        # ---------------------------------------------
        if choice == '1':
            Data = input("Enter your data to compress it: ").strip()
            if not Data:
                print("Error: Empty input.")
                continue
            if not Data.isalpha():
                print("Error: Input must contain only letters (A–Z or a–z).")
                continue

            tags = lz77_compress(Data)
            df = pd.DataFrame([{'position': t.position, 'length': t.length, 'symbol': t.next_char} for t in tags])

            print("\n--- Compression Result (Tags) ---")
            print(df.to_string(index=False))
            print("\ncompression done successfully.")

        # ---------------------------------------------
        # Decompression Mode
        # ---------------------------------------------
        elif choice == '2':
            print("\nEnter tags as: position,length,symbol  (type 'ok' when done)")
            user_tags = []

            while True:
                raw = input("Tag: ").strip()
                if raw.lower() == 'ok':
                    break
                try:
                    pos, length, sym = raw.split(',')
                    pos = int(pos)
                    length = int(length)
                    sym = sym.strip()

                    if sym not in ['', 'null'] and not (len(sym) == 1 and sym.isalpha()):
                        print("Symbol must be a single letter (A–Z or a–z) or empty.")
                        continue

                    t = Tag(pos, length, sym if sym != 'null' else '')
                    user_tags.append(t)
                except:
                    print("invalid format. Example: 3,2,a")

            if not user_tags:
                print("No tags entered.")
                continue

            result = decompress(user_tags)
            print("\n--- Decompressed Text ---")
            print(result)

        # ---------------------------------------------
        # Ask to Run Again
        # ---------------------------------------------
        again = input("\nDo you want to run again? (yes/no): ").lower().strip()
        if again not in ['y', 'yes']:
            print("Goodbye!")
            break


# -----------------------------------------------------
# Run the program
# -----------------------------------------------------
if __name__ == "__main__":
    main()
