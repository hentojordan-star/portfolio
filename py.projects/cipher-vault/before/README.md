# CipherVault – Initial Encryption Tool (Pre-Optimization Report)

### Overview
This folder contains the initial build of the *CipherVault* encryption utility developed for internal business use. The software was intended to provide data encryption and decryption capabilities for sensitive company files while maintaining restricted access for authorized personnel.

---

### Project Background
The tool was designed to rotate encryption algorithms automatically and secure access via biometric authentication. However, early testing revealed multiple operational and logical inconsistencies that prevented the software from functioning as intended.

---

### Identified Technical Issues

1. **Unstable Encryption Logic**
   - The encryption and decryption processes produced inconsistent or invalid outputs.
   - Algorithm rotation failed intermittently due to mismanaged randomization and key reuse.

2. **Key Storage and Retrieval Errors**
   - Keys were not persistently written to storage.
   - The system occasionally overwrote valid keys with null values, causing permanent data loss.

3. **Performance and Memory Inefficiencies**
   - Redundant encryption calls led to unnecessary resource consumption.
   - Memory usage increased exponentially during repeated operations.

4. **Incomplete Authentication Mechanism**
   - The fingerprint access feature was only partially implemented.
   - Security checks could be bypassed under specific conditions.

5. **Poor Code Organization**
   - Function definitions were scattered and lacked modular structure.
   - Inadequate documentation and minimal error handling complicated debugging.

---

### Testing Observations
- Decryption frequently failed to reproduce the original message.  
- Keys were lost upon application restart.  
- File I/O operations sometimes caused the program to terminate unexpectedly.  
- Biometric authentication remained nonfunctional.

---

### Summary
The current version demonstrates the conceptual foundation for the encryption system but lacks the structural and operational reliability required for deployment.  
This iteration has been retained strictly for reference and comparison with the optimized, production-ready version available in the `/after` directory.

---

**Internal Note:**  
This build was archived for evaluation purposes before system rework and optimization.
