from src.verification import (
    save_verification_result,
    create_verification_report,
    save_text_report
)

import os
import json

from src.hasher import calculate_sha256

from src.evidence_record import (
    create_evidence_record,
    save_evidence_record,
    verify_evidence_record,
    load_evidence_record,
    verify_record_integrity
)


def create_record():
    print()

    file_path = input("Enter evidence file path: ")

    if not os.path.exists(file_path):
        print("Error: Evidence file not found.")
        return

    current_hash = calculate_sha256(file_path)
    current_file_size = os.path.getsize(file_path)

    record = create_evidence_record(
        file_path,
        current_hash,
        current_file_size
    )

    record_path = (
        f"evidence/records/"
        f"{record['record_id']}.json"
    )

    save_evidence_record(record, record_path)

    print()
    print("Evidence Record Created")
    print("-----------------------")
    print("Record ID:", record["record_id"])
    print("File:", record["file_name"])
    print("SHA-256:", record["sha256"])
    print("File size:", record["file_size"])
    print("Record integrity:", verify_record_integrity(record))
    print("Record saved:", record_path)


def verify_evidence():
    print()

    file_path = input("Enter evidence file path: ")

    if not os.path.exists(file_path):
        print("Error: Evidence file not found.")
        return

    record_id = input("Enter Evidence Record ID: ")

    try:
        record = load_evidence_record(record_id)
    except FileNotFoundError:
        print("Error: Evidence Record ID not found.")
        return

    record_integrity_verified = verify_record_integrity(record)

    print()
    print("Record integrity:", record_integrity_verified)

    if not record_integrity_verified:
        print("RESULT: EVIDENCE RECORD TAMPERED")
        return

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

    report_path = (
        f"evidence/Verification/"
        f"{record['record_id']}_report.json"
    )

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

    verification_path = (
        f"evidence/Verification/"
        f"{record['record_id']}.json"
    )

    save_verification_result(
        record["record_id"],
        verified,
        verification_path
    )

    print("Verification result saved.")
    print("JSON report saved.")
    print("Text report saved.")


def list_evidence_records():
    records_path = "evidence/records"

    if not os.path.exists(records_path):
        print("No evidence records found.")
        return

    files = [
        file for file in os.listdir(records_path)
        if file.endswith(".json")
    ]

    if not files:
        print("No evidence records found.")
        return

    print()
    print("Evidence Records")
    print("================")

    for file_name in sorted(files):
        path = os.path.join(records_path, file_name)

        try:
            with open(path, "r") as file:
                record = json.load(file)

            print()
            print("ID:", record.get("record_id"))
            print("File:", record.get("file_name"))
            print("SHA-256:", record.get("sha256"))
            print("Size:", record.get("file_size"))
            print("Date:", record.get("timestamp"))

        except (json.JSONDecodeError, OSError):
            print()
            print("Unable to read:", file_name)


def search_evidence_record():
    print()

    record_id = input("Enter Evidence Record ID to search: ")

    record_path = os.path.join(
        "evidence",
        "records",
        f"{record_id}.json"
    )

    if not os.path.exists(record_path):
        print("Error: Evidence Record ID not found.")
        return

    try:
        with open(record_path, "r") as file:
            record = json.load(file)

    except (json.JSONDecodeError, OSError):
        print("Error: Unable to read evidence record.")
        return

    print()
    print("Evidence Record Found")
    print("=====================")
    print("ID:", record.get("record_id"))
    print("File:", record.get("file_name"))
    print("SHA-256:", record.get("sha256"))
    print("Size:", record.get("file_size"))
    print("Date:", record.get("timestamp"))
    print(
        "Record integrity:",
        verify_record_integrity(record)
    )


print("================================")
print("        EvidenceChain")
print("   Digital Evidence Verification")
print("================================")


while True:

    print()
    print("1. Create Evidence Record")
    print("2. Verify Evidence")
    print("3. List Evidence Records")
    print("4. Search Evidence Record")
    print("5. Exit")
    print()

    choice = input("Enter your choice: ")

    if choice == "1":
        create_record()

    elif choice == "2":
        verify_evidence()

    elif choice == "3":
        list_evidence_records()

    elif choice == "4":
        search_evidence_record()

    elif choice == "5":
        print("Exiting EvidenceChain.")
        break

    else:
        print("Invalid choice.")