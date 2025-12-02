# app.py
import streamlit as st
import sqlite3
import os
import uuid
from datetime import datetime
import json

# ---------- CONFIG ----------
DB_PATH = "vendors.db"
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ---------- DB HELPERS ----------
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    # vendors table
    c.execute('''
    CREATE TABLE IF NOT EXISTS vendors (
        id TEXT PRIMARY KEY,
        name TEXT,
        business_type TEXT,
        contact TEXT,
        address TEXT,
        docs TEXT,
        status TEXT,
        admin_comment TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    ''')
    # audit log table
    c.execute('''
    CREATE TABLE IF NOT EXISTS audit_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vendor_id TEXT,
        action_by TEXT,
        action TEXT,
        comment TEXT,
        timestamp TEXT
    )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------- CRUD ----------
def create_vendor(name, business_type, contact, address, doc_paths):
    conn = get_conn()
    c = conn.cursor()
    vid = str(uuid.uuid4())[:8]
    now = datetime.utcnow().isoformat()
    docs_json = json.dumps(doc_paths)
    c.execute('''
    INSERT INTO vendors (id,name,business_type,contact,address,docs,status,created_at,updated_at)
    VALUES (?,?,?,?,?,?,?,?,?)
    ''', (vid, name, business_type, contact, address, docs_json, "Pending", now, now))
    conn.commit()
    conn.close()
    return vid

def list_vendors(filter_status=None):
    conn = get_conn()
    c = conn.cursor()
    if filter_status:
        c.execute("SELECT * FROM vendors WHERE status=? ORDER BY created_at DESC", (filter_status,))
    else:
        c.execute("SELECT * FROM vendors ORDER BY created_at DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_vendor(vid):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM vendors WHERE id=?", (vid,))
    r = c.fetchone()
    conn.close()
    return r

def update_status(vid, status, admin_comment, action_by="admin"):
    conn = get_conn()
    c = conn.cursor()
    now = datetime.utcnow().isoformat()
    c.execute("UPDATE vendors SET status=?, admin_comment=?, updated_at=? WHERE id=?", (status, admin_comment, now, vid))
    c.execute("INSERT INTO audit_log (vendor_id, action_by, action, comment, timestamp) VALUES (?,?,?,?,?)",
              (vid, action_by, status, admin_comment, now))
    conn.commit()
    conn.close()

def get_audit(vid):
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM audit_log WHERE vendor_id=? ORDER BY timestamp DESC", (vid,))
    rows = c.fetchall()
    conn.close()
    return rows

# ---------- UI ----------
st.set_page_config(page_title="Vendor Onboarding & KYC", layout="wide")
st.title("Mini Vendor Onboarding & KYC Platform")

# Simulated login switch
role = st.sidebar.selectbox("Simulate role", ["Vendor", "Admin"])
st.sidebar.markdown("**Quick actions**")
if role == "Vendor":
    st.sidebar.info("You are viewing as a vendor. Use the form to register and upload KYC.")
else:
    st.sidebar.info("You are viewing as admin. Review/approve vendors here.")

# --- VENDOR VIEW ---
if role == "Vendor":
    st.header("Vendor Registration")
    with st.form("reg"):
        name = st.text_input("Vendor / Business Name", placeholder="ABC Traders")
        business_type = st.selectbox("Business Type", ["Proprietorship", "Partnership", "LLP", "Pvt Ltd", "Other"])
        contact = st.text_input("Contact (phone / email)")
        address = st.text_area("Address")
        st.write("Upload KYC documents (GST/PAN/Reg certificates) — files saved locally")
        uploaded = st.file_uploader("Choose files", accept_multiple_files=True)
        submitted = st.form_submit_button("Submit Registration")
    if submitted:
        if not (name and contact):
            st.error("Please provide at minimum name and contact.")
        else:
            saved_paths = []
            for f in uploaded:
                filename = f"{uuid.uuid4().hex}_{f.name}"
                path = os.path.join(UPLOAD_DIR, filename)
                with open(path, "wb") as wf:
                    wf.write(f.getbuffer())
                saved_paths.append(path)
            vid = create_vendor(name, business_type, contact, address, saved_paths)
            st.success(f"Registration submitted! Your Vendor ID: **{vid}**")
            st.info("Admin will review and update the status. Use the Vendor Status tracker (below) to check updates.")

    st.markdown("---")
    st.header("Vendor Status Tracker")
    st.info("Enter your Vendor ID (shown after registration) to view status.")
    vid_q = st.text_input("Vendor ID")
    if st.button("Check Status"):
        if not vid_q:
            st.error("Enter vendor id")
        else:
            v = get_vendor(vid_q.strip())
            if not v:
                st.error("Vendor ID not found")
            else:
                st.write("**Vendor Name:**", v["name"])
                st.write("**Status:**", v["status"])
                if v["admin_comment"]:
                    st.write("**Admin Comment:**", v["admin_comment"])
                st.write("**Submitted on:**", v["created_at"])
                # show docs
                docs = json.loads(v["docs"]) if v["docs"] else []
                if docs:
                    st.write("Documents:")
                    for p in docs:
                        if os.path.exists(p):
                            st.write(f"- {os.path.basename(p)} (saved: `{p}`)")
                        else:
                            st.write(f"- {os.path.basename(p)} (missing)")

# --- ADMIN VIEW ---
else:
    st.header("Admin Dashboard")
    st.markdown("Filter vendors by status:")
    status_filter = st.selectbox("Status", ["All", "Pending", "Approved", "Rejected"])
    rows = list_vendors(None if status_filter == "All" else status_filter)
    st.write(f"Total results: {len(rows)}")
    for r in rows:
        cols = st.columns([1,3,2,1,1])
        cols[0].write(f"**{r['id']}**")
        cols[1].write(f"**{r['name']}**\n\n{r['business_type']}\n\n{r['contact']}")
        cols[2].write(f"{r['address'][:100]}...")
        cols[3].write(f"Status: **{r['status']}**")
        view_btn = cols[4].button("View / Review", key=f"view_{r['id']}")
        if view_btn:
            st.markdown("---")
            st.subheader(f"Reviewing: {r['name']} (ID: {r['id']})")
            st.write("Business Type:", r["business_type"])
            st.write("Contact:", r["contact"])
            st.write("Address:", r["address"])
            docs = json.loads(r["docs"]) if r["docs"] else []
            st.write("Documents:")
            for p in docs:
                if os.path.exists(p):
                    st.write(f"- {os.path.basename(p)} — saved at `{p}`")
                else:
                    st.write(f"- {os.path.basename(p)} (missing)")
            st.write("----")
            st.subheader("Admin Action")
            col1, col2 = st.columns([2,3])
            with col1:
                new_status = st.selectbox("Set status", ["Pending", "Approved", "Rejected"], index=0)
            with col2:
                admin_comment = st.text_area("Comment for vendor (optional)")
            if st.button("Save Decision", key=f"decide_{r['id']}"):
                update_status(r["id"], new_status, admin_comment or "")
                st.success(f"Vendor {r['id']} set to {new_status}")

            st.subheader("Audit Log")
            logs = get_audit(r["id"])
            if logs:
                for log in logs:
                    st.write(f"- [{log['timestamp']}] {log['action_by']} → {log['action']} — {log['comment']}")
            else:
                st.write("No actions yet.")
            st.markdown("---")

# ---------- Sidebar notes ----------
st.sidebar.markdown("---")
st.sidebar.markdown("**Notes for demo**")
st.sidebar.markdown("""
- This app uses **SQLite** (file `vendors.db`) and stores uploaded docs in `./uploads/`.
- Vendor ID shown after registration — use it to track status.
- Admin actions are saved to an audit log.
- For a quick demo: Register as Vendor, upload 1-2 small files, switch to Admin role, find the vendor and Approve, then switch back Vendor and check status.
""")

if st.sidebar.checkbox("Show raw DB (for testing)"):
    conn = get_conn()
    df = conn.execute("SELECT id,name,status,created_at FROM vendors ORDER BY created_at DESC").fetchall()
    st.write(df)
    conn.close()
