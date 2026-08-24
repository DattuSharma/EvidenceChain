from src.evidence_record import (
    create_evidence_record,
    verify_evidence_record,
    calculate_record_integrity,
    verify_record_integrity
)


def test_create_evidence_record():
    record = create_evidence_record("test.txt", "abc123", 100)

    assert record["file_name"] == "test.txt"
    assert record["sha256"] == "abc123"
    assert record["file_size"] == 100
    assert record["file_type"] == ".txt"

    assert "timestamp" in record
    assert "integrity_hash" in record
    assert len(record["integrity_hash"]) == 64


def test_verify_evidence_record():
    record = {
        "sha256": "abc123"
    }

    assert verify_evidence_record(record, "abc123") is True
    assert verify_evidence_record(record, "wrong_hash") is False


def test_verify_evidence_record_file_size():
    record = {
        "sha256": "abc123",
        "file_size": 100
    }

    assert verify_evidence_record(record, "abc123", 100) is True
    assert verify_evidence_record(record, "abc123", 200) is False


def test_verify_evidence_record_tampered_file():
    record = {
        "sha256": "original_hash",
        "file_size": 18
    }

    assert verify_evidence_record(
        record,
        "tampered_hash",
        25
    ) is False


def test_evidence_record_integrity():
    record = create_evidence_record(
        "test.txt",
        "abc123",
        18
    )

    hash1 = calculate_record_integrity(record)
    hash2 = calculate_record_integrity(record)

    assert hash1 == hash2
    assert len(hash1) == 64


def test_evidence_record_integrity_detects_change():
    record = create_evidence_record(
        "test.txt",
        "abc123",
        18
    )

    original_hash = calculate_record_integrity(record)

    record["sha256"] = "changed_hash"

    changed_hash = calculate_record_integrity(record)

    assert original_hash != changed_hash


def test_stored_integrity_hash_is_correct():
    record = create_evidence_record(
        "test.txt",
        "abc123",
        18
    )

    calculated_hash = calculate_record_integrity(record)

    assert record["integrity_hash"] == calculated_hash


def test_verify_record_integrity():
    record = create_evidence_record(
        "test.txt",
        "abc123",
        18
    )

    assert verify_record_integrity(record) is True


def test_verify_record_integrity_detects_tampering():
    record = create_evidence_record(
        "test.txt",
        "abc123",
        18
    )

    record["file_name"] = "tampered.txt"

    assert verify_record_integrity(record) is False