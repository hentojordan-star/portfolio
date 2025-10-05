# CipherVault  
### Secure Text Encryption and Decryption System  

**Developer Summary:**  
This repository contains both the *initial version* (before optimization) and the *revised version* of CipherVault — a secure vault utility designed to help the company protect sensitive text data such as confidential files, notes, or messages.  

The new implementation completely restructures the code for better security, efficiency, and reliability while preserving the original concept and improving usability.

---

## 🔐 Project Overview  

CipherVault is a local encryption and decryption tool that allows only authorized users to encrypt and decrypt sensitive text data.  

Each authorized user (e.g., the owner and secretary) authenticates using a fingerprint-based token (simulated). Once verified, the user can:
- Encrypt text using rotating algorithms, and  
- Decrypt their own stored data.  

All activities are logged, and all sensitive keys are encrypted using a master passphrase.

---

## 🧩 Key Problems in the Previous Version  

The initial draft had multiple structural and functional flaws, which caused instability and made the encryption unreliable.  
Major issues included:

1. **Weak Encryption Logic** – Encryption keys were stored in plaintext and often lost between sessions.  
2. **Faulty Algorithm Handling** – Algorithm rotation and decryption often broke previously encrypted files.  
3. **Authentication Instability** – Fingerprint verification failed inconsistently, sometimes locking out all users.  
4. **No Audit or Error Tracking** – There was no way to confirm what happened during encryption/decryption.  
5. **File Corruption Risks** – Writing operations overwrote or corrupted key files if the program crashed midway.  
6. **Poor Scalability** – No structure for extending new algorithms or user records.  

---

## ⚙️ Improvements in the New Version  

The new CipherVault was rebuilt for **security, maintainability, and clarity**.  
Key improvements include:

### 🔸 Secure Keystore System  
- All encryption keys and user records are now stored **inside an encrypted keystore (`keystore.json`)**.  
- The keystore itself is protected using a **master passphrase**, converted into a strong encryption key via PBKDF2.  
- Losing this passphrase means losing access — ensuring that even local file access doesn’t compromise data.

### 🔸 Fingerprint Authentication (Simulated & Stable)  
- Fingerprint tokens are **hashed** using SHA-256 before storage, ensuring privacy and consistency.  
- Only matching hashes can unlock user profiles.  

### 🔸 Stronger Cryptographic Algorithms  
- Supports two modern, authenticated encryption methods:  
  - `Fernet` (AES under the hood, URL-safe)  
  - `ChaCha20-Poly1305` (high-performance, used in modern systems like TLS 1.3)  
- The system can rotate between these algorithms without breaking previously encrypted data.

### 🔸 Algorithm Rotation & History  
- The vault can **switch algorithms** securely, recording a rotation history.  
- This ensures compatibility for decrypting older content.

### 🔸 Data Integrity & Atomic Writes  
- All writes to disk (keystore, ciphertexts, audit logs) are **atomic**, meaning files are never half-written.  
- This prevents corruption even if the program crashes during an operation.

### 🔸 Comprehensive Audit Logging  
- Every action — user registration, authentication, encryption, decryption, rotation, and key export — is **recorded in an audit log** (`audit.log`) with UTC timestamps.  

### 🔸 Usability Enhancements  
- Clear, text-based menu system.  
- Context-based prompts and automatic file creation.  
- Error handling and human-readable messages.  

---

## 📁 Folder Structure  

```bash
cipher-vault/
│
├── before/
│   ├── vault_before.py          # Original faulty version
│   └──README.md                 # Company's submission
├── after/
│   ├──vault.py                 # Optimized and secured version
│
├── data/
│   ├── keystore.json            # Encrypted keystore (auto-created)
│   ├── audit.log                # Operation logs (auto-created)
│   ├── salt.bin                 # Cryptographic salt (auto-created)
│   ├── *_last_cipher.txt      # Per-user ciphertext files
│
└── README.md                    # Documentation (this file)
```

🧭 How to Set Up and Use CipherVault
1️⃣ Installation

Ensure you have Python 3.8+ installed, then install dependencies:
```bash
pip install cryptography
```
---
2️⃣ Running the Application

Navigate to your CipherVault directory and run:
```bash
python after/vault.py
```
The first time you run it, you’ll be prompted to create a master passphrase.
This passphrase encrypts your keystore — keep it private and safe.

---
3️⃣ Creating Users

After entering the master passphrase, use the main menu to register users.

Steps:
```bash
1) Register user
```
Then:

1. Enter a username (e.g., owner or secretary).

2. When prompted for a fingerprint, enter a unique token (string).

- The token will be hashed — it can be any memorable word or code.

3. The user is now registered with their own encryption key.

---
4️⃣ Encrypting Text

Example flow:
```bash
2) Encrypt text
```
Then:

1. Enter fingerprint token for authentication.
2. Type or paste the text to encrypt.
3. CipherVault encrypts it using the current algorithm and stores it in:

```bash
data/<username>_last_cipher.txt
```
✅ Example output:
```bash
Encryption successful!
Ciphertext saved to data/owner_last_cipher.txt
```
---
5️⃣ Decrypting Text
```bash
Example flow:
```
3) Decrypt text

Then:

1. Enter fingerprint token.

2. Press Enter (to use last ciphertext) or paste ciphertext manually.

✅ Example output:
```bash
Decryption successful!
Decrypted text:
"Confidential data for October payroll."
```
---
6️⃣ Rotating the Encryption Algorithm

Periodically rotate the active algorithm to maintain security:
```bash
4) Rotate algorithm
```
CipherVault switches between:

- fernet
- chacha20

All previous ciphertexts remain decryptable.

✅ Example:
```bash
Algorithm rotated successfully!
Current algorithm: chacha20
```
---
7️⃣ Viewing Logs and Keystore Summary

To check current users:
``bash
5) Show keystore (summary)
```
To view activity history:
```bash
7) View audit log
```
Example log output:
```bash
[2025-10-05 16:21:11 UTC] User 'owner' registered.
[2025-10-05 16:23:09 UTC] Text encrypted using algorithm 'fernet'.
[2025-10-05 16:24:33 UTC] Algorithm rotated to 'chacha20'.
```
---
8️⃣ Exporting a User Key (Admin Only)

If you ever need to back up a user key:
```bash
6) Export user key
```
✅ Example:
```bash
Enter username: owner
Exported key (base64): gAAAAABlI5...
```
⚠️ Only use this on trusted, offline systems.

---
🧮 Security & Data Management

- All keys and user data are stored encrypted using your master passphrase.
- Fingerprint tokens are hashed (SHA-256) and cannot be reversed.
- CipherVault never stores plaintext data — only ciphertexts and encrypted keystore files.
- If the keystore is lost, encrypted data cannot be recovered.
---
🧾 Conclusion

The reworked CipherVault provides a secure, efficient, and maintainable encryption system ready for business use.

It eliminates key loss, ensures proper authentication, and introduces a professional-grade audit and encryption structure.
The system now reflects a production-ready standard suitable for sensitive business operations.

---
✅ Deliverables Summary

- Fully functional, optimized encryption/decryption tool.
- Encrypted keystore with master-passphrase protection.
- Algorithm rotation support and complete audit logging.
- JSON data handling, atomic writes, and consistent file structure.
- Detailed documentation for deployment and maintenance.
