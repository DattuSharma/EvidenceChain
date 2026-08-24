from src.verification import (
    save_verification_result,
    create_verification_report,
    save_text_report
)
import os
import json

from src.hasher import calculate_sha256
from src.evidence_record import (
    verify_evidence_record,
    load_evidence_record,
    verify_record_integrity
)

print("================================")
print("      EvidenceChain")
print("  Digital Evidence Verification")
print("================================")

file_path = input("Enter evidence file path: ")

if not os.path.exists(file_path):
    print("Error: Evidence file not found.")
    exit()

record_id = input("Enter Evidence Record ID: ")

try:
    record = load_evidence_record(record_id)
except FileNotFoundError:
    print("Error: Evidence Record ID not found.")
    exit()

record_integrity_verified = verify_record_integrity(record)

print("Record integrity:", record_integrity_verified)

if not record_integrity_verified:
    print("RESULT: EVIDENCE RECORD TAMPERED")
    exit()

current_hash = calculate_sha256(file_path)
current_file_size = os.path.getsize(file_path)

verified = verify_evidence_record(
    record,
    current_hash,
    current_file_size
)

print("Evidence Record ID:", record["record_id"])
print("File:", record["file_name"])
print("Evidence verification:", verified)

if verified:
    print("RESULT: VERIFIED")
else:
    print("RESULT: TAMPERED")

report = create_verification_report(
    record,
    current_hash,
    current_file_size,
    record_integrity_verified,
    verified
)

report_path = f"evidence/Verification/{record['record_id']}_report.json"

with open(report_path, "w") as file:
    json.dump(report, file, indent=2)

text_report_path = (
    f"evidence/Verification/"
    f"{record['record_id']}_report.txt"
)

save_text_report(
    report,
    text_report_path
)

verification_path = f"evidence/Verification/{record['record_id']}.json"

save_verification_result(
    record["record_id"],
    verified,
    verification_path
)

print("Verification result saved.")
print("JSON report saved.")
print("Text report saved.")