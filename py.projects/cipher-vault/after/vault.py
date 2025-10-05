#!/usr/bin/env python3
"""
CipherVault (after) - secure CLI vault for encrypting/decrypting text.
- Uses modern symmetric encryption (Fernet + ChaCha20Poly1305 options)
- Keystore (user keys) are stored encrypted using a master key derived from a passphrase
- Fingerprint authentication simulated via hashed tokens (consistent storage)
- Atomic disk writes and audit logging
- Algorithm rotation with history preserved (old items remain decryptable)
"""

import os
import json
import base64
import secrets
import hashlib
import time
from datetime import datetime
from getpass import getpass
from pathlib import Path
from typing import Optional, Dict, Any

# Cryptography imports
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.backends import default_backend

# ---------------------------
# Configuration & paths
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent  # project root
DATA_DIR = BASE_DIR / 'data'
KEYSTORE_PATH = DATA_DIR / 'keystore.json'
AUDIT_LOG = DATA_DIR / 'audit.log'
SALT_PATH = DATA_DIR / 'salt.bin'  # salt for KDF (persisted)

# Supported algorithms (internal names)
ALGORITHMS = ['fernet', 'chacha20']

# KDF parameters
KDF_ITERATIONS = 200_000

# Ensure data dir exists
DATA_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------
# Utility helpers
# ---------------------------
def atomic_write(path: Path, data: str) -> None:
    """Write file atomically to avoid partial writes."""
    tmp = path.with_suffix('.tmp')
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(data)
    os.replace(tmp, path)


def now_iso() -> str:
    return datetime.utcnow().isoformat() + 'Z'


def hash_fp(token: str) -> str:
    """Return a stable hash of the fingerprint token."""
    h = hashlib.sha256(token.encode('utf-8')).hexdigest()
    return h


def load_json(path: Path) -> Any:
    if not path.exists():
        return {}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_json_atomic(path: Path, obj: Any) -> None:
    atomic_write(path, json.dumps(obj, indent=2))


def append_audit(entry: str) -> None:
    """Append a timestamped audit line."""
    line = f"{now_iso()} {entry}\n"
    with open(AUDIT_LOG, 'a', encoding='utf-8') as f:
        f.write(line)


# ---------------------------
# Master key derivation
# ---------------------------
def _ensure_salt() -> bytes:
    if SALT_PATH.exists():
        return SALT_PATH.read_bytes()
    # Create a new random salt
    s = secrets.token_bytes(16)
    SALT_PATH.write_bytes(s)
    return s


def derive_master_key(passphrase: str) -> bytes:
    """Derive a 32-byte key from passphrase using PBKDF2."""
    salt = _ensure_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=KDF_ITERATIONS,
        backend=default_backend()
    )
    return kdf.derive(passphrase.encode('utf-8'))


def master_key_to_fernet(master_key: bytes) -> Fernet:
    """Return a Fernet object derived from master key bytes."""
    # Fernet key is base64 of 32 url-safe bytes
    token = base64.urlsafe_b64encode(master_key)
    return Fernet(token)


# ---------------------------
# Keystore format & helpers
# Keystore stores per-user:
#   users: { username: { fp_hash: "...", created: "..."}}
#   keys: { username: { enc_key: "<b64>", algo_history: [..] } }
#   current_algo: "fernet"
# ---------------------------
def load_keystore() -> Dict[str, Any]:
    data = load_json(KEYSTORE_PATH)
    # Ensure structure
    if not data:
        data = {'users': {}, 'keys': {}, 'current_algo': ALGORITHMS[0]}
    if 'current_algo' not in data:
        data['current_algo'] = ALGORITHMS[0]
    return data


def save_keystore_encrypted(keystore: Dict[str, Any], master_fernet: Fernet) -> None:
    """Encrypt entire keystore JSON with master key and write atomic.
    We will store an envelope: {'v': 1, 'payload': <b64 encrypted json>}
    """
    raw = json.dumps(keystore).encode('utf-8')
    token = master_fernet.encrypt(raw)
    envelope = {'v': 1, 'payload': token.decode('utf-8')}
    save_json_atomic(KEYSTORE_PATH, envelope)


def load_keystore_decrypted(master_fernet: Fernet) -> Dict[str, Any]:
    """Load keystore envelope and decrypt payload. If no keystore, return default."""
    if not KEYSTORE_PATH.exists():
        return {'users': {}, 'keys': {}, 'current_algo': ALGORITHMS[0]}
    envelope = load_json(KEYSTORE_PATH)
    if not envelope or 'payload' not in envelope:
        return {'users': {}, 'keys': {}, 'current_algo': ALGORITHMS[0]}
    try:
        raw = master_fernet.decrypt(envelope['payload'].encode('utf-8'))
        return json.loads(raw.decode('utf-8'))
    except InvalidToken:
        raise ValueError("Master passphrase doesn't match stored keystore.")
    except Exception:
        return {'users': {}, 'keys': {}, 'current_algo': ALGORITHMS[0]}


# ---------------------------
# User management
# ---------------------------
def register_user(master_fernet: Fernet) -> None:
    """Register a user with fingerprint token and generate a per-user key."""
    ks = load_keystore_decrypted(master_fernet)
    name = input("Enter user name (owner/secretary): ").strip()
    if not name:
        print("Name required.")
        return
    token = getpass("Scan fingerprint (enter token): ").strip()
    if not token:
        print("Fingerprint required.")
        return
    fp_h = hash_fp(token)
    ks['users'][name] = {'fp_hash': fp_h, 'created': now_iso()}

    # Generate a 32-byte key for algorithms (raw key)
    raw_key = secrets.token_bytes(32)
    enc_key = base64.b64encode(raw_key).decode('utf-8')

    ks['keys'][name] = {
        'enc_key': enc_key,
        'algo_history': ks.get('keys', {}).get(name, {}).get('algo_history', []),
        'created': now_iso()
    }
    append_audit(f"REGISTER user={name}")
    save_keystore_encrypted(ks, master_fernet)
    print(f"User {name} registered.")


def authenticate_user(master_fernet: Fernet) -> Optional[str]:
    """Authenticate the user using fingerprint token."""
    try:
        ks = load_keystore_decrypted(master_fernet)
    except ValueError as e:
        print("Keystore unlock failed:", e)
        return None

    token = getpass("Scan fingerprint (enter token): ").strip()
    if not token:
        print("No token provided.")
        return None
    fp_h = hash_fp(token)
    for name, info in ks.get('users', {}).items():
        if info.get('fp_hash') == fp_h:
            append_audit(f"AUTH success user={name}")
            return name
    append_audit("AUTH failed")
    print("Authentication failed.")
    return None


# ---------------------------
# Key extraction and rotation
# ---------------------------
def _get_raw_key_for_user(ks: Dict[str, Any], username: str) -> Optional[bytes]:
    entry = ks.get('keys', {}).get(username)
    if not entry:
        return None
    enc_key_b64 = entry.get('enc_key')
    if not enc_key_b64:
        return None
    try:
        return base64.b64decode(enc_key_b64)
    except Exception:
        return None


def rotate_algorithm(master_fernet: Fernet) -> None:
    """Rotate algorithm and record history. Keep existing keys usable."""
    ks = load_keystore_decrypted(master_fernet)
    current = ks.get('current_algo', ALGORITHMS[0])
    choices = [a for a in ALGORITHMS if a != current]
    if not choices:
        print("No alternative algorithm available.")
        return
    new_algo = secrets.choice(choices)
    ks['current_algo'] = new_algo
    ks.setdefault('rotation_history', []).append({'when': now_iso(), 'from': current, 'to': new_algo})
    append_audit(f"ROTATE from={current} to={new_algo}")
    save_keystore_encrypted(ks, master_fernet)
    print("Algorithm rotated to", new_algo)


# ---------------------------
# Encryption primitives
# ---------------------------
def fernet_encrypt(raw_key: bytes, plaintext: str) -> str:
    # Derive a Fernet object from raw_key
    token = base64.urlsafe_b64encode(raw_key)
    f = Fernet(token)
    ct = f.encrypt(plaintext.encode('utf-8'))
    return ct.decode('utf-8')


def fernet_decrypt(raw_key: bytes, ciphertext: str) -> str:
    token = base64.urlsafe_b64encode(raw_key)
    f = Fernet(token)
    pt = f.decrypt(ciphertext.encode('utf-8'))
    return pt.decode('utf-8')


def chacha_encrypt(raw_key: bytes, plaintext: str) -> str:
    aead = ChaCha20Poly1305(raw_key)
    nonce = secrets.token_bytes(12)
    ct = aead.encrypt(nonce, plaintext.encode('utf-8'), associated_data=None)
    return base64.b64encode(nonce + ct).decode('utf-8')


def chacha_decrypt(raw_key: bytes, ciphertext_b64: str) -> str:
    data = base64.b64decode(ciphertext_b64)
    nonce = data[:12]
    ct = data[12:]
    aead = ChaCha20Poly1305(raw_key)
    pt = aead.decrypt(nonce, ct, associated_data=None)
    return pt.decode('utf-8')


# ---------------------------
# High level encryption/decryption
# ---------------------------
def encrypt_for_user(master_fernet: Fernet) -> None:
    user = authenticate_user(master_fernet)
    if not user:
        return
    ks = load_keystore_decrypted(master_fernet)
    current_algo = ks.get('current_algo', ALGORITHMS[0])
    raw_key = _get_raw_key_for_user(ks, user)
    if not raw_key:
        print("No key for this user.")
        return

    plaintext = input("Enter text to encrypt: ")
    try:
        if current_algo == 'fernet':
            ct = fernet_encrypt(raw_key, plaintext)
        elif current_algo == 'chacha20':
            ct = chacha_encrypt(raw_key, plaintext)
        else:
            print("Unsupported algorithm.")
            return
    except Exception as e:
        print("Encryption failed:", e)
        append_audit(f"ENCRYPT error user={user} err={e}")
        return

    # store ciphertext to user-specific file (no plaintext)
    out_path = DATA_DIR / f"{user}_last_cipher.txt"
    atomic_write(out_path, ct)
    append_audit(f"ENCRYPT success user={user} algo={current_algo}")
    print("Encrypted text saved.")


def decrypt_for_user(master_fernet: Fernet) -> None:
    user = authenticate_user(master_fernet)
    if not user:
        return
    ks = load_keystore_decrypted(master_fernet)
    current_algo = ks.get('current_algo', ALGORITHMS[0])
    raw_key = _get_raw_key_for_user(ks, user)
    if not raw_key:
        print("No key for this user.")
        return

    choice = input("Paste ciphertext or leave blank to read last file: ").strip()
    if not choice:
        in_path = DATA_DIR / f"{user}_last_cipher.txt"
        if not in_path.exists():
            print("No ciphertext available.")
            return
        choice = in_path.read_text(encoding='utf-8').strip()

    try:
        if current_algo == 'fernet':
            pt = fernet_decrypt(raw_key, choice)
        elif current_algo == 'chacha20':
            pt = chacha_decrypt(raw_key, choice)
        else:
            print("Unsupported algorithm.")
            return
        append_audit(f"DECRYPT success user={user} algo={current_algo}")
        print("Decrypted text:\n")
        print(pt)
    except InvalidToken:
        print("Decryption failed: invalid token or wrong key.")
        append_audit(f"DECRYPT failure user={user} reason=InvalidToken")
    except Exception as e:
        print("Decryption error:", e)
        append_audit(f"DECRYPT error user={user} err={e}")


# ---------------------------
# Admin utilities
# ---------------------------
def show_keystore(master_fernet: Fernet) -> None:
    try:
        ks = load_keystore_decrypted(master_fernet)
    except ValueError:
        print("Cannot unlock keystore with provided passphrase.")
        return
    # print minimal information (no raw keys)
    simple = {
        'users': {u: {'created': info.get('created')} for u, info in ks.get('users', {}).items()},
        'current_algo': ks.get('current_algo'),
        'rotation_history': ks.get('rotation_history', [])
    }
    print(json.dumps(simple, indent=2))


def export_user_key(master_fernet: Fernet, username: str) -> None:
    """Export raw key material for user (admin operation)."""
    try:
        ks = load_keystore_decrypted(master_fernet)
    except ValueError:
        print("Cannot unlock keystore with provided passphrase.")
        return
    raw = _get_raw_key_for_user(ks, username)
    if not raw:
        print("No key for user.")
        return
    print(f"Key for {username} (base64): {base64.b64encode(raw).decode('utf-8')}")
    append_audit(f"EXPORT_KEY user={username}")


# ---------------------------
# CLI / Driver
# ---------------------------
def unlock_master() -> Optional[Fernet]:
    """Prompt user for master passphrase and return Fernet for keystore operations."""
    passphrase = getpass("Enter master passphrase to unlock keystore: ").strip()
    if not passphrase:
        print("Passphrase required.")
        return None
    try:
        mk = derive_master_key(passphrase)
        return master_key_to_fernet(mk)
    except Exception as e:
        print("Failed to derive master key:", e)
        return None


def init_first_time(master_fernet: Fernet) -> None:
    """Ensure keystore exists; if not, create an empty keystore encrypted."""
    if KEYSTORE_PATH.exists():
        return
    ks = {'users': {}, 'keys': {}, 'current_algo': ALGORITHMS[0], 'rotation_history': []}
    save_keystore_encrypted(ks, master_fernet)
    append_audit("INIT keystore")


def main():
    print("CipherVault — secure vault")
    master = unlock_master()
    if master is None:
        return
    # initialize if missing
    init_first_time(master)

    while True:
        print("\nMenu:")
        print("1) Register user")
        print("2) Encrypt text")
        print("3) Decrypt text")
        print("4) Rotate algorithm")
        print("5) Show keystore (summary)")
        print("6) Export user key (admin)")
        print("7) View audit log")
        print("8) Exit")
        choice = input("Choice: ").strip()
        if choice == '1':
            register_user(master)
        elif choice == '2':
            encrypt_for_user(master)
        elif choice == '3':
            decrypt_for_user(master)
        elif choice == '4':
            rotate_algorithm(master)
        elif choice == '5':
            show_keystore(master)
        elif choice == '6':
            user = input("Enter username to export key: ").strip()
            export_user_key(master, user)
        elif choice == '7':
            # show last 200 lines of audit log
            if not AUDIT_LOG.exists():
                print("No audit log yet.")
            else:
                with open(AUDIT_LOG, 'r', encoding='utf-8') as f:
                    lines = f.readlines()[-200:]
                    print(''.join(lines))
        elif choice == '8':
            print("Exiting.")
            break
        else:
            print("Unknown option.")


if __name__ == '__main__':
    main()
