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