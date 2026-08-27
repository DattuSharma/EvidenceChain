from datetime import datetime
import json
import uuid
import os
import hashlib


def calculate_record_integrity(record):
    """
    Calculate a SHA-256 integrity hash for the evidence record.
    """

    data = {
        "record_id": record["record_id"],
        "file_name": record["file_name"],
        "file_type": record["file_type"],
        "sha256": record["sha256"],
        "file_size": record["file_size"],
        "timestamp": record["timestamp"]
    }

    record_data = json.dumps(
        data,
        sort_keys=True
    ).encode("utf-8")

    return hashlib.sha256(record_data).hexdigest()


def create_evidence_record(file_name, file_hash, file_size):
    """
    Create a new evidence record.
    """

    record = {
        "record_id": str(uuid.uuid4()),
        "file_name": file_name,
        "file_type": os.path.splitext(file_name)[1],
        "sha256": file_hash,
        "file_size": file_size,
        "timestamp": datetime.now().isoformat()
    }

    record["integrity_hash"] = calculate_record_integrity(record)

    return record


def save_evidence_record(record, output_path):
    """
    Save an evidence record as JSON.
    """

    with open(output_path, "w") as file:
        json.dump(record, file, indent=2)


def load_evidence_record(record_id):
    """
    Load an evidence record using its record ID.
    """

    path = f"evidence/records/{record_id}.json"

    with open(path, "r") as file:
        return json.load(file)


def verify_evidence_record(record, current_hash, current_file_size=None):
    """
    Verify the evidence file against the stored record.

    Checks:
    1. SHA-256 hash
    2. File size, when provided
    """

    if record["sha256"] != current_hash:
        return False

    if current_file_size is not None:
        if record["file_size"] != current_file_size:
            return False

    return True


def verify_record_integrity(record):
    """
    Verify that the evidence record itself has not been modified.
    """

    if "integrity_hash" not in record:
        return False

    stored_hash = record["integrity_hash"]

    calculated_hash = calculate_record_integrity(record)

    return stored_hash == calculated_hash