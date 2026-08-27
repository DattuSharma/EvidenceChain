# EvidenceChain

## Digital Media Evidence Trust & Verification System

EvidenceChain is a Python-based digital evidence verification system designed to help determine whether a digital evidence file has been modified after its original evidence record was created.

The system creates a trusted evidence record containing the file's SHA-256 hash, file size, timestamp, and metadata. During verification, the current file is compared against the stored record to detect modifications or tampering.

---

## Key Features

- Create digital evidence records
- Generate SHA-256 file hashes
- Store evidence metadata
- Record file size and timestamp
- Protect evidence records using integrity hashes
- Verify evidence against its original record
- Detect modified or tampered evidence
- Detect file-size changes
- Search evidence records
- View detailed evidence records
- Maintain verification history
- Generate JSON verification reports
- Generate text verification reports
- Interactive command-line interface
- Automated testing with pytest

---

## How It Works

```text
                    Evidence File
                         |
                         v
                  Calculate SHA-256
                         |
                         v
                Create Evidence Record
                         |
             +-----------+-----------+
             |                       |
             v                       v
       File Metadata          Record Integrity
             |                       |
             +-----------+-----------+
                         |
                         v
                    Verification
                         |
                 +-------+-------+
                 |               |
                 v               v
             VERIFIED         TAMPERED
```

EvidenceChain performs two important integrity checks.

### 1. Evidence Integrity

The current SHA-256 hash and file size are compared with the values stored in the evidence record.

If they match:

```text
Record integrity: True
Evidence verification: True
RESULT: VERIFIED
```

If they do not match:

```text
Record integrity: True
Evidence verification: False
RESULT: TAMPERED
```

### 2. Record Integrity

Each evidence record contains an integrity hash calculated from its important metadata.

This helps detect unauthorized modification of the evidence record itself.

---

## Interactive Menu

EvidenceChain provides the following command-line options:

```text
1. Create Evidence Record
2. Verify Evidence
3. List Evidence Records
4. Search Evidence Record
5. Record Details
6. Verification History
7. Exit
```

---

## Example

### Genuine Evidence

When the evidence file has not changed:

```text
Record integrity: True
Evidence verification: True
RESULT: VERIFIED
```

### Tampered Evidence

When the evidence file has been modified:

```text
Record integrity: True
Evidence verification: False
RESULT: TAMPERED
```

EvidenceChain also stores verification events in its history.

---

## Requirements

- Python 3.x
- pytest

No external database is required.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/DattuSharma/EvidenceChain.git
cd EvidenceChain
```

Install pytest:

```bash
python -m pip install pytest
```

---

## Running EvidenceChain

Start the application:

```bash
python main.py
```

The interactive menu will appear.

---

## Running Tests

Run the complete automated test suite:

```bash
python -m pytest -q
```

Current test result:

```text
13 passed
```

The tests cover evidence record creation, hashing, verification, tamper detection, integrity checking, and verification functionality.

---

## Project Structure

```text
EvidenceChain/
|
|-- main.py
|-- create_test_record.py
|-- README.md
|-- .gitignore
|
|-- src/
|   |-- evidence_record.py
|   |-- hasher.py
|   |-- verification.py
|
|-- tests/
|   |-- test_evidence_record.py
|   |-- test_hasher.py
|   |-- test_verification.py
|
|-- uploads/
|
`-- evidence/
    |-- records/
    `-- Verification/
        `-- History/
```

---

## Technology Stack

- Python
- SHA-256 cryptographic hashing
- JSON
- Pytest
- Git / GitHub
- Command-line interface

---

## Security Design

EvidenceChain uses SHA-256 to create a cryptographic fingerprint of an evidence file.

The system stores important evidence metadata including:

- Record ID
- File name
- File type
- SHA-256 hash
- File size
- Timestamp
- Record integrity hash

During verification, the current evidence is compared against the original record.

A changed file produces a different SHA-256 hash and/or file size, allowing EvidenceChain to identify the evidence as potentially tampered.

---

## Testing Demonstration

The project was manually tested using the following workflow:

1. Create an evidence record.
2. Verify the original evidence.
3. Modify the evidence file.
4. Verify the modified evidence.
5. Confirm the result changes from `VERIFIED` to `TAMPERED`.
6. Restore the original evidence.
7. Run the complete automated test suite.

Final automated test result:

```text
13 passed
```

---

## Limitations

EvidenceChain is currently a local prototype intended for educational and demonstration purposes.

It does not currently provide:

- Digital signatures
- Public-key infrastructure
- Secure remote evidence storage
- Role-based access control
- Blockchain-based storage
- Full forensic chain-of-custody compliance
- Protection against deletion of local evidence records

---

## Future Enhancements

Potential future improvements include:

- Digital signatures for evidence records
- Public/private key verification
- Secure cloud storage
- Web-based dashboard
- User authentication and authorization
- Advanced chain-of-custody tracking
- Database-backed evidence storage
- Evidence metadata extraction
- Image and video forensic analysis
- Cryptographically linked verification history
- Exportable professional forensic reports

---

## Project Status

**Functional prototype completed**

The current implementation successfully demonstrates:

- Evidence record creation
- Cryptographic hashing
- Evidence verification
- Tamper detection
- Record integrity verification
- Verification history
- Report generation
- Automated testing

Automated tests:

```text
13 passed
```

---

## Author

**Dattu Sharma**

EvidenceChain — Digital Media Evidence Trust & Verification System