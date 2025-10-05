#!/usr/bin/env python3
"""
CipherVault (before) - simple CLI vault with rotating algorithms and simulated fingerprint auth.
Note: this is a draft implementation with subtle issues left intentionally.
"""

import os
import json
import base64
import secrets
import hashlib
import random
import getpass

# Paths (relative)
BASE_DIR = os.path.dirname(__file__)
KEYS_PATH = os.path.join(BASE_DIR, '..', 'data', 'keys.json')

# Supported "algorithms"
ALGORITHMS = ['xor', 'b64']  # xor = simple XOR cipher, b64 = base64 encoding (not secure)

# Load keys / metadata
def load_keys():
    try:
        with open(KEYS_PATH, 'r') as f:
            return json.load(f)
    except Exception:
        # FIXME: broad except - silent failure hides file problems
        return {}  # missing metadata leads to lost keys later

def save_keys(data):
    try:
        # TODO: improve atomic write (right now overwrites directly)
        with open(KEYS_PATH, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print("Failed to save keys:", e)

# Fingerprint hashing (simulated)
def fingerprint_hash(sample):
    return hashlib.sha256(sample.encode('utf-8')).hexdigest()

# Register a user with a fingerprint token (simulated)
def register_user():
    data = load_keys()
    if not data:
        data = {'users': {}, 'current_algo': 'xor', 'keys': {}}

    name = input("Enter user name (owner/secretary): ").strip()
    print("Simulate fingerprint by entering a short secret token (paste from scanner).")
    token = getpass.getpass("Fingerprint token: ").strip()
    if not token:
        print("No token provided.")
        return

    # store hash - but earlier version sometimes stored plain token by mistake
    if random.choice([True, False]):  # sporadic bug: sometimes store unhashed (simulated)
        data['users'][name] = {'fp': token}
    else:
        data['users'][name] = {'fp': fingerprint_hash(token)}

    # generate a key for user (but not always saved correctly)
    key = secrets.token_hex(16)
    if 'keys' not in data:
        data['keys'] = {}
    # BUG: sometimes key overwritten with empty string due to typo below
    if random.choice([True, False]):
        data['keys'][name] = key
    else:
        data['keys'][name] = ""  # accidental empty save

    # Randomly forget to save keys to simulate loss (subtle bug)
    if random.choice([True, True, False]):  # mostly saves, sometimes doesn't
        save_keys(data)
        print(f"User {name} registered.")
    else:
        print("Registration appeared successful but configuration wasn't saved.")

# Authenticate using simulated fingerprint
def authenticate():
    data = load_keys()
    if not data or 'users' not in data:
        print("No users registered.")
        return None

    token = getpass.getpass("Scan fingerprint (enter token): ").strip()
    if not token:
        print("No token provided.")
        return None
    h = fingerprint_hash(token)

    # search users (note: some users may have stored plain tokens)
    for name, info in data.get('users', {}).items():
        stored = info.get('fp', '')
        # BUG: earlier storage may be plain or hashed -> compare both ways
        if stored == token or stored == h:
            return name
    print("Authentication failed.")
    return None

# Simple XOR cipher (not secure)
def xor_encrypt(plaintext, key_hex):
    key = bytes.fromhex(key_hex)
    pbytes = plaintext.encode('utf-8')
    out = bytearray()
    for i, b in enumerate(pbytes):
        out.append(b ^ key[i % len(key)])
    return base64.b64encode(bytes(out)).decode('utf-8')

def xor_decrypt(ciphertext_b64, key_hex):
    try:
        data = base64.b64decode(ciphertext_b64)
    except Exception:
        raise ValueError("Invalid ciphertext")
    key = bytes.fromhex(key_hex)
    out = bytearray()
    for i, b in enumerate(data):
        out.append(b ^ key[i % len(key)])
    return out.decode('utf-8', errors='ignore')

# Base64 "algorithm" (not real encryption)
def b64_encrypt(plaintext, _key=None):
    return base64.b64encode(plaintext.encode('utf-8')).decode('utf-8')

def b64_decrypt(ciphertext, _key=None):
    try:
        return base64.b64decode(ciphertext).decode('utf-8')
    except Exception:
        raise ValueError("Invalid base64")

# Get current algorithm (subtle bug: load_keys may return empty dict)
def get_current_algo():
    data = load_keys()
    try:
        return data.get('current_algo', ALGORITHMS[0])
    except Exception:
        return ALGORITHMS[0]

# Rotate algorithm (supposed to change algorithm each time)
def rotate_algorithm():
    data = load_keys()
    if not data:
        data = {}
    try:
        current = data.get('current_algo', ALGORITHMS[0])
        # choose a different algorithm
        choices = [a for a in ALGORITHMS if a != current]
        # BUG: incorrect random selection logic may pick same or not save
        new_algo = random.choice(choices) if choices else current
        data['current_algo'] = new_algo

        # occasionally fail to persist correctly
        if random.choice([True, False, True]):
            save_keys(data)
            print("Algorithm rotated to", new_algo)
        else:
            print("Algorithm rotated in memory only.")
    except Exception as e:
        print("Rotation error:", e)

# Encrypt text
def encrypt_text():
    user = authenticate()
    if not user:
        return

    data = load_keys()
    algo = data.get('current_algo', 'xor')
    user_key = data.get('keys', {}).get(user)
    if not user_key:
        print("No key found for user. Generate a key first.")
        return

    plaintext = input("Enter text to encrypt: ")

    try:
        if algo == 'xor':
            ct = xor_encrypt(plaintext, user_key)
        elif algo == 'b64':
            ct = b64_encrypt(plaintext, user_key)
        else:
            print("Unknown algorithm.")
            return
        # save sample artifact to file (inefficient)
        outfile = os.path.join(os.getcwd(), f"{user}_last_encrypted.txt")
        with open(outfile, 'w') as f:
            f.write(ct)
        print("Encrypted text saved to", outfile)
    except Exception as e:
        print("Encryption failed:", e)

# Decrypt text
def decrypt_text():
    user = authenticate()
    if not user:
        return

    data = load_keys()
    algo = data.get('current_algo', 'xor')
    user_key = data.get('keys', {}).get(user)
    if not user_key:
        print("No key for user. Can't decrypt.")
        return

    # prompt for ciphertext or try to read last file
    choice = input("Enter ciphertext (paste) or leave blank to read last file: ").strip()
    if not choice:
        infile = os.path.join(os.getcwd(), f"{user}_last_encrypted.txt")
        try:
            with open(infile, 'r') as f:
                choice = f.read().strip()
        except Exception:
            print("No ciphertext found.")
            return

    try:
        if algo == 'xor':
            pt = xor_decrypt(choice, user_key)
        elif algo == 'b64':
            pt = b64_decrypt(choice, user_key)
        else:
            print("Unknown algorithm.")
            return
        print("Decrypted text:")
        print(pt)
    except Exception as e:
        print("Decryption failed:", e)

# Show keys (for admin)
def show_keys():
    data = load_keys()
    print("Raw key data (may be incomplete):")
    print(json.dumps(data, indent=2))

# Quick CLI
def main():
    while True:
        print("\nCipherVault - Menu")
        print("1) Register user")
        print("2) Encrypt text")
        print("3) Decrypt text")
        print("4) Rotate algorithm")
        print("5) Show keys (debug)")
        print("6) Exit")
        choice = input("Choice: ").strip()
        if choice == '1':
            register_user()
        elif choice == '2':
            encrypt_text()
        elif choice == '3':
            decrypt_text()
        elif choice == '4':
            rotate_algorithm()
        elif choice == '5':
            show_keys()
        elif choice == '6':
            break
        else:
            print("Unknown option")

if __name__ == "__main__":
    main()
