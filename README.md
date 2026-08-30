# 🔐 EvidenceChain

## Digital Media Evidence Trust & Verification System

EvidenceChain is a digital evidence integrity and verification system designed to detect whether a digital evidence file has been modified after a trusted record was created.

The system uses **SHA-256 cryptographic hashing** to create a unique fingerprint for evidence files and compares the fingerprint during verification.

---

## 🎯 Project Objective

Digital files can be modified without obvious visual changes.

EvidenceChain provides a simple way to:

- Create a trusted evidence record
- Generate a SHA-256 hash
- Verify evidence against its original record
- Detect tampering
- Verify record integrity
- Maintain verification history
- Display evidence statistics through a web dashboard

---

## ⚙️ Key Features

### 📁 Evidence Record Creation

Upload an evidence file to create a trusted record containing:

- Record ID
- File name
- File type
- File size
- Timestamp
- SHA-256 hash
- Record integrity hash

### 🔐 SHA-256 Verification

EvidenceChain calculates the SHA-256 hash of the uploaded file.

During verification, the current hash is compared with the original trusted hash.

### 🛡️ Tamper Detection

If the evidence file changes, the SHA-256 hash changes.

EvidenceChain reports:

**🟢 VERIFIED**

when the evidence matches the trusted record.

**🔴 TAMPERED**

when the evidence does not match.

### 📊 Web Dashboard

The web interface provides:

- Total evidence records
- Total verifications
- Verified results
- Tampered results
- Recent evidence records

### 🔎 Evidence Search

Search evidence records by:

- Record ID
- File name

### 📄 Record Details

Each evidence record can be viewed with its cryptographic information.

### 🕒 Verification History

The system maintains a history of verification results including:

- Verification status
- Record ID
- Original SHA-256
- Current SHA-256
- Original file size
- Current file size
- Timestamp

---

## 🧰 Technologies Used

- Python
- Flask
- SHA-256
- JSON
- HTML
- CSS
- Pytest
- Git & GitHub

---

## 🏗️ Project Structure

```text
EvidenceChain/
│
├── src/
│   ├── hasher.py
│   ├── evidence_record.py
│   └── verification.py
│
├── tests/
│
├── uploads/
│
├── evidence/
│
├── app.py
├── README.md
├── .gitignore
└── requirements.txt