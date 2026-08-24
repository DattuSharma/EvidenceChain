from src.hasher import calculate_sha256
from src.evidence_record import create_evidence_record, save_evidence_record
import os

p = "uploads/test.txt"
h = calculate_sha256(p)

r = create_evidence_record(p, h, os.path.getsize(p))

save_evidence_record(
    r,
    f"evidence/records/{r['record_id']}.json"
)

print("NEW RECORD ID:", r["record_id"])
print("SHA:", r["sha256"])
print("SIZE:", r["file_size"])
print("INTEGRITY:", r["integrity_hash"])
