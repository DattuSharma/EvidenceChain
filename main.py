from src.verification import (
    save_verification_result,
    create_verification_report,
    save_text_report
)

import os
import json
from datetime import datetime

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

    record_path = os.path.join(
        "evidence",
        "records",
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
    print(
        "Record integrity:",
        verify_record_integrity(record)
    )
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

    os.makedirs(
        os.path.join("evidence", "Verification"),
        exist_ok=True
    )

    report_path = os.path.join(
        "evidence",
        "Verification",
        f"{record['record_id']}_report.json"
    )

    with open(report_path, "w") as file:
        json.dump(report, file, indent=2)

    text_report_path = os.path.join(
        "evidence",
        "Verification",
        f"{record['record_id']}_report.txt"
    )

    save_text_report(
        report,
        text_report_path
    )

    verification_path = os.path.join(
        "evidence",
        "Verification",
        f"{record['record_id']}.json"
    )

    save_verification_result(
        record["record_id"],
        verified,
        verification_path
    )

    # ----------------------------------------
    # MULTI-VERIFICATION HISTORY
    # ----------------------------------------

    history_path = os.path.join(
        "evidence",
        "Verification",
        "History"
    )

    os.makedirs(
        history_path,
        exist_ok=True
    )

    history_timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    history_file = os.path.join(
        history_path,
        f"{record['record_id']}_{history_timestamp}.json"
    )

    history_record = {
        "record_id": record["record_id"],
        "file_name": record["file_name"],
        "original_sha256": record["sha256"],
        "current_sha256": current_hash,
        "original_file_size": record["file_size"],
        "current_file_size": current_file_size,
        "record_integrity": record_integrity_verified,
        "verified": verified,
        "result": "VERIFIED" if verified else "TAMPERED",
        "timestamp": datetime.now().isoformat()
    }

    with open(history_file, "w") as file:
        json.dump(history_record, file, indent=2)

    print("Verification result saved.")
    print("JSON report saved.")
    print("Text report saved.")
    print("Verification history saved.")


def list_evidence_records():
    records_path = "evidence/records"

    if not os.path.exists(records_path):
        print("No evidence records found.")
        return

    files = [
        file
        for file in os.listdir(records_path)
        if file.endswith(".json")
    ]

    if not files:
        print("No evidence records found.")
        return

    print()
    print("Evidence Records")
    print("================")

    for file_name in sorted(files):
        path = os.path.join(
            records_path,
            file_name
        )

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

    record_id = input(
        "Enter Evidence Record ID to search: "
    )

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


def record_details():
    print()

    record_id = input(
        "Enter Evidence Record ID: "
    )

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
    print("Evidence Record Details")
    print("=======================")

    print(
        "Record ID:",
        record.get("record_id")
    )

    print(
        "File Name:",
        record.get("file_name")
    )

    print(
        "File Type:",
        record.get("file_type")
    )

    print(
        "SHA-256:",
        record.get("sha256")
    )

    print(
        "File Size:",
        record.get("file_size")
    )

    print(
        "Timestamp:",
        record.get("timestamp")
    )

    print(
        "Integrity Hash:",
        record.get("integrity_hash")
    )

    print()

    print(
        "Record Integrity:",
        verify_record_integrity(record)
    )


def verification_history():
    print()

    record_id = input(
        "Enter Evidence Record ID: "
    )

    history_path = os.path.join(
        "evidence",
        "Verification",
        "History"
    )

    history_files = []

    if os.path.exists(history_path):

        history_files = [
            file
            for file in os.listdir(history_path)
            if file.startswith(record_id + "_")
            and file.endswith(".json")
        ]

    print()
    print("Verification History")
    print("====================")

    if history_files:

        history_files.sort()

        for file_name in history_files:

            path = os.path.join(
                history_path,
                file_name
            )

            try:

                with open(path, "r") as file:
                    result = json.load(file)

                print()
                print("Verification Event")
                print("------------------")

                print(
                    "Record ID:",
                    result.get("record_id")
                )

                print(
                    "File:",
                    result.get("file_name")
                )

                print(
                    "Original SHA-256:",
                    result.get("original_sha256")
                )

                print(
                    "Current SHA-256:",
                    result.get("current_sha256")
                )

                print(
                    "Original Size:",
                    result.get("original_file_size")
                )

                print(
                    "Current Size:",
                    result.get("current_file_size")
                )

                print(
                    "Record Integrity:",
                    result.get("record_integrity")
                )

                print(
                    "Verified:",
                    result.get("verified")
                )

                print(
                    "Result:",
                    result.get("result")
                )

                print(
                    "Timestamp:",
                    result.get("timestamp")
                )

            except (json.JSONDecodeError, OSError):

                print()
                print(
                    "Unable to read:",
                    file_name
                )

        return

    # Compatibility with old verification result files
    verification_path = os.path.join(
        "evidence",
        "Verification",
        f"{record_id}.json"
    )

    if not os.path.exists(verification_path):
        print("No verification history found.")
        return

    try:

        with open(
            verification_path,
            "r"
        ) as file:

            result = json.load(file)

    except (json.JSONDecodeError, OSError):

        print(
            "Error: Unable to read verification history."
        )
        return

    print(
        "Record ID:",
        result.get("record_id")
    )

    print(
        "Verified:",
        result.get("verified")
    )

    print(
        "Timestamp:",
        result.get("timestamp")
    )

    if result.get("verified") is True:
        print("Result: VERIFIED")
    else:
        print("Result: TAMPERED")


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
    print("5. Record Details")
    print("6. Verification History")
    print("7. Exit")
    print()

    choice = input(
        "Enter your choice: "
    )

    if choice == "1":

        create_record()

    elif choice == "2":

        verify_evidence()

    elif choice == "3":

        list_evidence_records()

    elif choice == "4":

        search_evidence_record()

    elif choice == "5":

        record_details()

    elif choice == "6":

        verification_history()

    elif choice == "7":

        print(
            "Exiting EvidenceChain."
        )

        break

    else:

        print(
            "Invalid choice."
        )