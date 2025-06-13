import random
import string
import math

def ask_yes_no(prompt):
    while True:
        ans = input(prompt + " (y/n): ").strip().lower()
        if ans in ['y', 'yes']:
            return True
        elif ans in ['n', 'no']:
            return False
        else:
            print("Just type 'y' or 'n'.")

def get_entropy(password):
    size = 0
    if any(c in string.ascii_lowercase for c in password): size += 26
    if any(c in string.ascii_uppercase for c in password): size += 26
    if any(c in string.digits for c in password): size += 10
    if any(c in string.punctuation for c in password): size += 32
    return len(password) * math.log2(size) if size else 0

def rate_password(password):
    entropy = get_entropy(password)
    if entropy < 40: return "Weak"
    elif entropy < 70: return "Moderate"
    elif entropy < 100: return "Strong"
    else: return "Vault-level"

def suggest_password(length, use_upper, use_lower, use_digits, use_symbols):
    pools = []
    if use_upper: pools.append(string.ascii_uppercase)
    if use_lower: pools.append(string.ascii_lowercase)
    if use_digits: pools.append(string.digits)
    if use_symbols: pools.append(string.punctuation)

    if not pools:
        raise ValueError("You need to select at least one type of character.")

    password = [random.choice(pool) for pool in pools]
    all_chars = ''.join(pools)
    password += random.choices(all_chars, k=length - len(password))
    random.shuffle(password)
    return ''.join(password)

def main():
    print("🔐 Welcome to Your Password Assistant\n")
    
    while True:
        try:
            length = input("How long should the password be? (default: 16): ").strip()
            length = int(length) if length.isdigit() else 16

            print("\nLet's decide what's in your password:")

            use_upper = ask_yes_no("Include UPPERCASE letters?")
            use_lower = ask_yes_no("Include lowercase letters?")
            use_digits = ask_yes_no("Include numbers?")
            use_symbols = ask_yes_no("Include symbols? (!@# etc.)")

            pwd = suggest_password(length, use_upper, use_lower, use_digits, use_symbols)
            strength = rate_password(pwd)

            print("\n✨ Here's a suggestion:")
            print(f"🔑 {pwd}")
            print(f"🔎 Strength: {strength}\n")

            happy = ask_yes_no("Would you like to use this one?")
            if happy:
                print("🎉 Great! Make sure to save it somewhere safe.")
                break
            else:
                if not ask_yes_no("Try again with same settings?"):
                    continue
        except ValueError as ve:
            print(f"\nError: {ve}")
            print("Let's start over.\n")

if __name__ == "__main__":
    main()
