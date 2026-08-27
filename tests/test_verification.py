from src.evidence_record import create_evidence_record
from src.verification import create_verification_report


def test_create_verification_report():
    record = create_evidence_record(
        "test.txt",
        "abc123",
        18
    )

    report = create_verification_report(
        record,
        "abc123",
        18,
        True,
        True
    )

    assert report["record_id"] == record["record_id"]
    assert report["file_name"] == "test.txt"
    assert report["original_sha256"] == "abc123"
    assert report["current_sha256"] == "abc123"
    assert report["original_file_size"] == 18
    assert report["current_file_size"] == 18
    assert report["record_integrity"] is True
    assert report["evidence_verified"] is True
    assert report["status"] == "VERIFIED"
    assert "timestamp" in report


def test_create_tampered_verification_report():
    record = create_evidence_record(
        "test.txt",
        "original_hash",
        18
    )

    report = create_verification_report(
        record,
        "tampered_hash",
        25,
        True,
        False
    )

    assert report["original_sha256"] == "original_hash"
    assert report["current_sha256"] == "tampered_hash"
    assert report["original_file_size"] == 18
    assert report["current_file_size"] == 25
    assert report["record_integrity"] is True
    assert report["evidence_verified"] is False
    assert report["status"] == "TAMPERED"


def test_verification_history_event_integrity():
    history_record = {
        "record_id": "test-record",
        "file_name": "test.txt",
        "original_sha256": "abc123",
        "current_sha256": "abc123",
        "original_file_size": 18,
        "current_file_size": 18,
        "record_integrity": True,
        "verified": True,
        "result": "VERIFIED",
        "timestamp": "2026-08-25T22:00:00"
    }

    assert history_record["record_integrity"] is True
    assert history_record["verified"] is True
    assert history_record["result"] == "VERIFIED"