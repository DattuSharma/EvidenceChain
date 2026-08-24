from datetime import datetime
import json
import os


def save_verification_result(record_id, verified, output_path):
    result = {
        "record_id": record_id,
        "verified": verified,
        "timestamp": datetime.now().isoformat()
    }

    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    with open(output_path, "w") as file:
        json.dump(result, file, indent=2)


def create_verification_report(
    record,
    current_hash,
    current_file_size,
    record_integrity_verified,
    verified
):
    return {
        "record_id": record["record_id"],
        "file_name": record["file_name"],
        "original_sha256": record["sha256"],
        "current_sha256": current_hash,
        "original_file_size": record["file_size"],
        "current_file_size": current_file_size,
        "record_integrity": record_integrity_verified,
        "evidence_verified": verified,
        "status": "VERIFIED" if verified else "TAMPERED",
        "timestamp": datetime.now().isoformat()
    }


def save_text_report(report, output_path):
    os.makedirs(
        os.path.dirname(output_path),
        exist_ok=True
    )

    with open(output_path, "w") as file:
        file.write("========================================\n")
        file.write("          EVIDENCECHAIN REPORT\n")
        file.write("========================================\n\n")

        file.write(f"Record ID: {report['record_id']}\n")
        file.write(f"File Name: {report['file_name']}\n\n")

        file.write("HASH VERIFICATION\n")
        file.write("----------------------------------------\n")
        file.write(f"Original SHA-256: {report['original_sha256']}\n")
        file.write(f"Current SHA-256:  {report['current_sha256']}\n\n")

        file.write("FILE SIZE VERIFICATION\n")
        file.write("----------------------------------------\n")
        file.write(f"Original Size: {report['original_file_size']} bytes\n")
        file.write(f"Current Size:  {report['current_file_size']} bytes\n\n")

        file.write("INTEGRITY\n")
        file.write("----------------------------------------\n")
        file.write(
            f"Record Integrity: {report['record_integrity']}\n"
        )
        file.write(
            f"Evidence Verified: {report['evidence_verified']}\n\n"
        )

        file.write("FINAL RESULT\n")
        file.write("----------------------------------------\n")
        file.write(f"STATUS: {report['status']}\n\n")

        file.write(f"Verification Time: {report['timestamp']}\n")
        file.write("========================================\n")