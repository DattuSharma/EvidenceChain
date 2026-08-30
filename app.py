from flask import Flask, request, render_template_string
from pathlib import Path
from datetime import datetime
import hashlib
import json
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = Path("uploads")
RECORD_FOLDER = Path("evidence/records")
HISTORY_FOLDER = Path("evidence/Verification")

UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
RECORD_FOLDER.mkdir(parents=True, exist_ok=True)
HISTORY_FOLDER.mkdir(parents=True, exist_ok=True)


# ============================================================
# SHA-256
# ============================================================

def calculate_sha256(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            chunk = file.read(4096)

            if not chunk:
                break

            sha256.update(chunk)

    return sha256.hexdigest()


# ============================================================
# RECORD INTEGRITY
# ============================================================

def calculate_record_integrity(record):

    data = {
        "record_id": record.get("record_id", ""),
        "file_name": record.get("file_name", ""),
        "file_type": record.get("file_type", ""),
        "sha256": record.get("sha256", ""),
        "file_size": record.get("file_size", 0),
        "timestamp": record.get("timestamp", "")
    }

    encoded = json.dumps(
        data,
        sort_keys=True
    ).encode()

    return hashlib.sha256(encoded).hexdigest()


def verify_record_integrity(record):

    if "integrity_hash" not in record:
        return False

    return (
        record["integrity_hash"]
        == calculate_record_integrity(record)
    )


# ============================================================
# RECORD LOADING
# ============================================================

def load_records():

    records = []

    for path in RECORD_FOLDER.glob("*.json"):

        try:

            with open(path, "r") as file:
                record = json.load(file)

            records.append(record)

        except (json.JSONDecodeError, OSError):
            continue

    records.sort(
        key=lambda x: x.get("timestamp", ""),
        reverse=True
    )

    return records


def load_record(record_id):

    path = RECORD_FOLDER / f"{record_id}.json"

    if not path.exists():
        return None

    try:

        with open(path, "r") as file:
            return json.load(file)

    except (json.JSONDecodeError, OSError):
        return None


# ============================================================
# VERIFICATION HISTORY
# ============================================================

def save_verification_history(result):

    verification_id = str(uuid.uuid4())

    history = {
        "verification_id": verification_id,
        "record_id": result.get("record_id", ""),
        "verified": result.get("verified", False),
        "record_integrity": result.get(
            "record_integrity",
            False
        ),
        "original_sha256": result.get(
            "original_sha256",
            ""
        ),
        "current_sha256": result.get(
            "current_sha256",
            ""
        ),
        "original_file_size": result.get(
            "original_file_size",
            0
        ),
        "current_file_size": result.get(
            "current_file_size",
            0
        ),
        "timestamp": datetime.now().isoformat()
    }

    path = HISTORY_FOLDER / f"{verification_id}.json"

    with open(path, "w") as file:
        json.dump(
            history,
            file,
            indent=2
        )

    return history


def load_history():

    history_items = []

    for path in HISTORY_FOLDER.glob("*.json"):

        try:

            with open(path, "r") as file:
                item = json.load(file)

            # Compatibility with older history files
            item.setdefault(
                "verification_id",
                path.stem
            )

            item.setdefault(
                "record_id",
                "Unknown"
            )

            item.setdefault(
                "verified",
                False
            )

            item.setdefault(
                "record_integrity",
                False
            )

            item.setdefault(
                "original_sha256",
                ""
            )

            item.setdefault(
                "current_sha256",
                ""
            )

            item.setdefault(
                "original_file_size",
                0
            )

            item.setdefault(
                "current_file_size",
                0
            )

            item.setdefault(
                "timestamp",
                ""
            )

            history_items.append(item)

        except (json.JSONDecodeError, OSError):
            continue

    history_items.sort(
        key=lambda x: x.get(
            "timestamp",
            ""
        ),
        reverse=True
    )

    return history_items


# ============================================================
# HTML
# ============================================================

HTML = """

<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>EvidenceChain</title>


<style>

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    background: #f4f6f8;

    color: #1f2937;
}


/* SIDEBAR */

.sidebar {

    position: fixed;

    left: 0;

    top: 0;

    bottom: 0;

    width: 235px;

    background: #111827;

    color: white;

    padding: 25px 15px;
}


.logo {

    font-size: 22px;

    font-weight: bold;

    padding:
        10px
        15px
        25px;
}


.logo-small {

    font-size: 13px;

    color: #9ca3af;

    margin-top: 5px;
}


.sidebar a {

    display: block;

    text-decoration: none;

    color: #d1d5db;

    padding: 12px 15px;

    margin: 5px 0;

    border-radius: 8px;
}


.sidebar a:hover {

    background: #374151;

    color: white;
}


/* MAIN */

.main {

    margin-left: 235px;

    min-height: 100vh;
}


.header {

    background: white;

    padding: 25px 35px;

    border-bottom:
        1px solid #e5e7eb;
}


.header h1 {

    margin: 0;

    font-size: 27px;
}


.header p {

    margin:
        7px
        0
        0;

    color: #6b7280;
}


.container {

    max-width: 1150px;

    margin: auto;

    padding: 30px;
}


/* CARDS */

.card {

    background: white;

    padding: 25px;

    border-radius: 12px;

    margin-bottom: 25px;

    box-shadow:
        0 3px 12px
        rgba(0,0,0,0.06);
}


.card h2 {

    margin-top: 0;
}


/* DASHBOARD */

.stats {

    display: grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap: 18px;

    margin-bottom: 25px;
}


.stat {

    background: white;

    padding: 22px;

    border-radius: 12px;

    box-shadow:
        0 3px 12px
        rgba(0,0,0,0.06);
}


.stat-title {

    color: #6b7280;

    font-size: 14px;
}


.stat-number {

    font-size: 30px;

    font-weight: bold;

    margin-top: 8px;
}


/* FORMS */

label {

    display: block;

    font-weight: bold;

    margin-top: 15px;
}


input[type="text"],
input[type="file"] {

    width: 100%;

    padding: 12px;

    margin-top: 7px;

    border:
        1px solid #d1d5db;

    border-radius: 7px;

    background: white;
}


button {

    border: none;

    background: #111827;

    color: white;

    padding:
        12px
        20px;

    border-radius: 7px;

    margin-top: 18px;

    cursor: pointer;

    font-size: 14px;
}


button:hover {

    background: #374151;
}


/* UPLOAD */

.upload-area {

    border:
        2px dashed #9ca3af;

    padding: 35px;

    text-align: center;

    border-radius: 12px;
}


/* TABLE */

.table-wrapper {

    overflow-x: auto;
}


table {

    width: 100%;

    border-collapse: collapse;
}


th,
td {

    padding: 13px;

    border-bottom:
        1px solid #e5e7eb;

    text-align: left;
}


th {

    background: #f9fafb;
}


td {

    font-size: 14px;
}


/* HASH */

.hash {

    font-family: monospace;

    word-break: break-all;

    background: #f3f4f6;

    padding: 12px;

    border-radius: 7px;
}


/* STATUS */

.status {

    display: inline-block;

    padding:
        6px
        10px;

    border-radius: 20px;

    font-weight: bold;

    font-size: 12px;
}


.verified {

    background: #dcfce7;

    color: #166534;
}


.tampered {

    background: #fee2e2;

    color: #991b1b;
}


/* RESULTS */

.success {

    background: #ecfdf5;

    border-left:
        6px solid #16a34a;

    padding: 22px;

    border-radius: 8px;
}


.danger {

    background: #fef2f2;

    border-left:
        6px solid #dc2626;

    padding: 22px;

    border-radius: 8px;
}


.big-status {

    font-size: 30px;

    font-weight: bold;
}


/* LINKS */

.action-link {

    color: #2563eb;

    text-decoration: none;

    font-weight: bold;
}


.action-link:hover {

    text-decoration: underline;
}


/* MOBILE */

@media (max-width: 800px) {

    .sidebar {

        position: relative;

        width: 100%;

        height: auto;
    }


    .main {

        margin-left: 0;
    }


    .stats {

        grid-template-columns:
            repeat(2, 1fr);
    }

}

</style>

</head>


<body>


<!-- SIDEBAR -->

<div class="sidebar">

    <div class="logo">

        🔐 EvidenceChain

        <div class="logo-small">

            Digital Evidence Trust System

        </div>

    </div>


    <a href="/">
        📊 Dashboard
    </a>


    <a href="/create">
        📁 Create Record
    </a>


    <a href="/verify">
        🛡️ Verify Evidence
    </a>


    <a href="/records">
        📋 Evidence Records
    </a>


    <a href="/history">
        🕒 Verification History
    </a>

</div>


<!-- MAIN -->

<div class="main">


<div class="header">

    <h1>
        {{ title }}
    </h1>

    <p>
        EvidenceChain Digital Media Evidence Trust
        & Verification System
    </p>

</div>


<div class="container">


{% if page == "dashboard" %}


<div class="stats">


<div class="stat">

    <div class="stat-title">
        Total Evidence Records
    </div>

    <div class="stat-number">
        {{ total_records }}
    </div>

</div>


<div class="stat">

    <div class="stat-title">
        Verifications
    </div>

    <div class="stat-number">
        {{ total_verifications }}
    </div>

</div>


<div class="stat">

    <div class="stat-title">
        Verified
    </div>

    <div class="stat-number">
        {{ verified_count }}
    </div>

</div>


<div class="stat">

    <div class="stat-title">
        Tampered
    </div>

    <div class="stat-number">
        {{ tampered_count }}
    </div>

</div>


</div>


<div class="card">

<h2>
    🛡️ EvidenceChain
</h2>

<p>

EvidenceChain is a digital evidence
integrity platform that uses SHA-256
cryptographic hashing to detect changes
in evidence files.

</p>

<p>

Create trusted evidence records,
verify files, detect tampering and
maintain verification history.

</p>

</div>


<div class="card">

<h2>
    Recent Evidence Records
</h2>


{% if records %}


<div class="table-wrapper">


<table>


<tr>

<th>Record ID</th>

<th>File</th>

<th>Size</th>

<th>Created</th>

<th>Action</th>

</tr>


{% for record in records[:5] %}


<tr>

<td>
    {{ record.get("record_id", "")[:12] }}...
</td>

<td>
    {{ record.get("file_name", "") }}
</td>

<td>
    {{ record.get("file_size", 0) }} bytes
</td>

<td>
    {{ record.get("timestamp", "") }}
</td>

<td>

<a
class="action-link"
href="/record/{{ record.get('record_id', '') }}">

View

</a>

</td>

</tr>


{% endfor %}


</table>


</div>


{% else %}

<p>
No evidence records yet.
</p>

{% endif %}


</div>


{% elif page == "create" %}


<div class="card">

<h2>
📁 Create Evidence Record
</h2>

<p>

Upload an original evidence file
to generate a trusted EvidenceChain record.

</p>


<form
action="/upload"
method="POST"
enctype="multipart/form-data">


<div class="upload-area">

<div style="font-size:50px;">
📁
</div>


<p>

<strong>
Select Evidence File
</strong>

</p>


<input
type="file"
name="evidence_file"
required>


<button type="submit">

Create Evidence Record

</button>


</div>


</form>

</div>


{% if record %}


<div class="card">

<h2>
✅ Evidence Record Created
</h2>


<div class="success">


<p>

<strong>
Record ID:
</strong>

<br>

{{ record.record_id }}

</p>


<p>

<strong>
File:
</strong>

<br>

{{ record.file_name }}

</p>


<p>

<strong>
File Size:
</strong>

{{ record.file_size }} bytes

</p>


<p>

<strong>
Timestamp:
</strong>

<br>

{{ record.timestamp }}

</p>


<p>

<strong>
SHA-256:
</strong>

</p>


<div class="hash">

{{ record.sha256 }}

</div>


</div>

</div>


{% endif %}


{% elif page == "verify" %}


<div class="card">

<h2>
🛡️ Verify Evidence
</h2>


<p>

Compare an evidence file against
its trusted EvidenceChain record.

</p>


<form
action="/verify"
method="POST"
enctype="multipart/form-data">


<label>
Evidence Record ID
</label>


<input
type="text"
name="record_id"
placeholder="Enter Record ID"
required>


<label>
Evidence File
</label>


<input
type="file"
name="evidence_file"
required>


<button type="submit">

Verify Evidence

</button>


</form>

</div>


{% if verification %}


<div class="card">

<h2>
Verification Result
</h2>


{% if verification.verified %}


<div class="success">

<div
class="big-status"
style="color:#15803d;">

🟢 VERIFIED

</div>


<p>

The evidence matches the
original trusted record.

</p>

</div>


{% else %}


<div class="danger">

<div
class="big-status"
style="color:#dc2626;">

🔴 TAMPERED

</div>


<p>

The evidence does not match
the original trusted record.

</p>

</div>


{% endif %}


<p>

<strong>
Record ID:
</strong>

<br>

{{ verification.record_id }}

</p>


<p>

<strong>
Record Integrity:
</strong>

{{ verification.record_integrity }}

</p>


<p>

<strong>
Original SHA-256:
</strong>

</p>


<div class="hash">

{{ verification.original_sha256 }}

</div>


<p>

<strong>
Current SHA-256:
</strong>

</p>


<div class="hash">

{{ verification.current_sha256 }}

</div>


<p>

<strong>
Original File Size:
</strong>

{{ verification.original_file_size }}
bytes

</p>


<p>

<strong>
Current File Size:
</strong>

{{ verification.current_file_size }}
bytes

</p>


</div>


{% endif %}


{% elif page == "records" %}


<div class="card">

<h2>
📋 Evidence Records
</h2>


<form
method="GET"
action="/records">


<input
type="text"
name="search"
value="{{ search }}"
placeholder="Search by Record ID or file name">


<button type="submit">

🔎 Search

</button>


</form>

</div>


<div class="card">


<div class="table-wrapper">


<table>


<tr>

<th>Record ID</th>

<th>File</th>

<th>Size</th>

<th>SHA-256</th>

<th>Details</th>

</tr>


{% for record in records %}


<tr>

<td>

{{ record.get("record_id", "")[:12] }}...

</td>


<td>

{{ record.get("file_name", "") }}

</td>


<td>

{{ record.get("file_size", 0) }}
bytes

</td>


<td>

{{ record.get("sha256", "")[:16] }}...

</td>


<td>

<a
class="action-link"
href="/record/{{ record.get('record_id', '') }}">

View

</a>

</td>

</tr>


{% endfor %}


</table>


</div>


{% if not records %}

<p>
No matching records found.
</p>

{% endif %}


</div>


{% elif page == "details" %}


<div class="card">


<h2>
📄 Evidence Record Details
</h2>


{% if record %}


<p>

<strong>
Record ID:
</strong>

<br>

{{ record.get("record_id", "") }}

</p>


<p>

<strong>
File:
</strong>

<br>

{{ record.get("file_name", "") }}

</p>


<p>

<strong>
File Type:
</strong>

{{ record.get("file_type", "") }}

</p>


<p>

<strong>
File Size:
</strong>

{{ record.get("file_size", 0) }}
bytes

</p>


<p>

<strong>
Timestamp:
</strong>

<br>

{{ record.get("timestamp", "") }}

</p>


<p>

<strong>
SHA-256:
</strong>

</p>


<div class="hash">

{{ record.get("sha256", "") }}

</div>


<p>

<strong>
Record Integrity:
</strong>

{{ integrity }}

</p>


{% else %}


<p>
Evidence record not found.
</p>


{% endif %}


</div>


{% elif page == "history" %}


<div class="card">


<h2>
🕒 Verification History
</h2>


{% if history %}


<div class="table-wrapper">


<table>


<tr>

<th>Status</th>

<th>Record ID</th>

<th>Original Hash</th>

<th>Current Hash</th>

<th>Original Size</th>

<th>Current Size</th>

<th>Timestamp</th>

</tr>


{% for item in history %}


<tr>


<td>


{% if item.get("verified", False) %}


<span class="status verified">

VERIFIED

</span>


{% else %}


<span class="status tampered">

TAMPERED

</span>


{% endif %}


</td>


<td>

{{ item.get("record_id", "Unknown")[:12] }}...

</td>


<td>

{% if item.get("original_sha256") %}

{{ item.get("original_sha256")[:16] }}...

{% else %}

N/A

{% endif %}

</td>


<td>

{% if item.get("current_sha256") %}

{{ item.get("current_sha256")[:16] }}...

{% else %}

N/A

{% endif %}

</td>


<td>

{{ item.get("original_file_size", "N/A") }}

</td>


<td>

{{ item.get("current_file_size", "N/A") }}

</td>


<td>

{{ item.get("timestamp", "N/A") }}

</td>


</tr>


{% endfor %}


</table>


</div>


{% else %}


<p>

No verification history yet.

</p>


{% endif %}


</div>


{% endif %}


</div>

</div>


</body>

</html>

"""


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
def dashboard():

    records = load_records()

    history = load_history()


    total_records = len(records)

    total_verifications = len(history)


    verified_count = sum(
        1
        for item in history
        if item.get("verified") is True
    )


    tampered_count = sum(
        1
        for item in history
        if item.get("verified") is False
    )


    return render_template_string(

        HTML,

        page="dashboard",

        title="Dashboard",

        records=records,

        total_records=total_records,

        total_verifications=total_verifications,

        verified_count=verified_count,

        tampered_count=tampered_count

    )


# ============================================================
# CREATE PAGE
# ============================================================

@app.route("/create")
def create():

    return render_template_string(

        HTML,

        page="create",

        title="Create Evidence Record"

    )


# ============================================================
# UPLOAD
# ============================================================

@app.route(
    "/upload",
    methods=["POST"]
)
def upload():

    uploaded_file = request.files.get(
        "evidence_file"
    )


    if uploaded_file is None:

        return "No file selected.", 400


    if uploaded_file.filename == "":

        return "No file selected.", 400


    safe_name = Path(
        uploaded_file.filename
    ).name


    file_path = (
        UPLOAD_FOLDER /
        safe_name
    )


    uploaded_file.save(file_path)


    file_hash = calculate_sha256(
        file_path
    )


    file_size = file_path.stat().st_size


    record = {

        "record_id":
            str(uuid.uuid4()),

        "file_name":
            str(file_path),

        "file_type":
            file_path.suffix,

        "sha256":
            file_hash,

        "file_size":
            file_size,

        "timestamp":
            datetime.now().isoformat()

    }


    record["integrity_hash"] = (
        calculate_record_integrity(
            record
        )
    )


    record_path = (

        RECORD_FOLDER /

        f"{record['record_id']}.json"

    )


    with open(
        record_path,
        "w"
    ) as file:

        json.dump(
            record,
            file,
            indent=2
        )


    return render_template_string(

        HTML,

        page="create",

        title="Create Evidence Record",

        record=record

    )


# ============================================================
# VERIFY
# ============================================================

@app.route(
    "/verify",
    methods=["GET", "POST"]
)
def verify():

    if request.method == "GET":

        return render_template_string(

            HTML,

            page="verify",

            title="Verify Evidence"

        )


    record_id = request.form.get(
        "record_id",
        ""
    ).strip()


    uploaded_file = request.files.get(
        "evidence_file"
    )


    if not record_id:

        return "Record ID is required.", 400


    if uploaded_file is None:

        return "Evidence file is required.", 400


    record = load_record(
        record_id
    )


    if record is None:

        return "Evidence record not found.", 404


    record_integrity = (
        verify_record_integrity(
            record
        )
    )


    temporary_name = (

        f"verification_"
        f"{uuid.uuid4()}"
        f"{Path(uploaded_file.filename).suffix}"

    )


    temporary_path = (
        UPLOAD_FOLDER /
        temporary_name
    )


    uploaded_file.save(
        temporary_path
    )


    current_hash = calculate_sha256(
        temporary_path
    )


    current_size = (
        temporary_path.stat().st_size
    )


    verified = (

        record_integrity

        and

        record.get("sha256", "")
        == current_hash

        and

        record.get("file_size", 0)
        == current_size

    )


    try:

        temporary_path.unlink()

    except OSError:

        pass


    verification = {

        "record_id":
            record_id,

        "record_integrity":
            record_integrity,

        "original_sha256":
            record.get("sha256", ""),

        "current_sha256":
            current_hash,

        "original_file_size":
            record.get("file_size", 0),

        "current_file_size":
            current_size,

        "verified":
            verified

    }


    save_verification_history(
        verification
    )


    return render_template_string(

        HTML,

        page="verify",

        title="Verify Evidence",

        verification=verification

    )


# ============================================================
# RECORDS + SEARCH
# ============================================================

@app.route("/records")
def records():

    search = request.args.get(
        "search",
        ""
    ).strip().lower()


    records = load_records()


    if search:

        records = [

            record

            for record in records

            if

            search in record.get(
                "record_id",
                ""
            ).lower()

            or

            search in record.get(
                "file_name",
                ""
            ).lower()

        ]


    return render_template_string(

        HTML,

        page="records",

        title="Evidence Records",

        records=records,

        search=search

    )


# ============================================================
# RECORD DETAILS
# ============================================================

@app.route(
    "/record/<record_id>"
)
def record_details(record_id):

    record = load_record(
        record_id
    )


    integrity = False


    if record:

        integrity = (
            verify_record_integrity(
                record
            )
        )


    return render_template_string(

        HTML,

        page="details",

        title="Evidence Record Details",

        record=record,

        integrity=integrity

    )


# ============================================================
# HISTORY
# ============================================================

@app.route("/history")
def history():

    history_items = load_history()


    return render_template_string(

        HTML,

        page="history",

        title="Verification History",

        history=history_items

    )


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    app.run(

        host="127.0.0.1",

        port=8000,

        debug=False

    )