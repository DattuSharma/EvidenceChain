# EvidenceChain

## Digital Media Evidence Trust & Verification System

EvidenceChain is a Python-based digital evidence verification system designed to detect whether a digital evidence file has been modified after its original evidence record was created.

The system uses SHA-256 hashing, file-size verification, record integrity hashing, automated testing, and verification reports.

---

## Key Features

- Create digital evidence records
- Generate SHA-256 hashes
- Store evidence metadata
- Protect evidence records with integrity hashes
- Verify evidence against its original record
- Detect modified or tampered files
- Verify file size changes
- Generate JSON verification reports
- Generate text verification reports
- Automated test suite using pytest
- Interactive command-line interface

---

## How It Works

```text
Evidence File
     |
     v
SHA-256 Hash
     |
     v
Evidence Record
     |
     v
Record Integrity Hash
     |
     v
Verification
     |
     +---------> VERIFIED
     |
     +---------> TAMPERED