import streamlit as st
import base64
import hashlib
import os
from cryptography.fernet import Fernet, InvalidToken

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="File Encryption Tool",
    page_icon="🔐",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* Import a sharp, modern font */
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

  html, body, [class*="css"] {
      font-family: 'IBM Plex Sans', sans-serif;
  }
  h1, h2, h3 {
      font-family: 'IBM Plex Mono', monospace;
      letter-spacing: -0.5px;
  }

  /* Dark card container */
  .card {
      background: #0f1117;
      border: 1px solid #2a2d3a;
      border-radius: 12px;
      padding: 1.5rem 2rem;
      margin-bottom: 1.2rem;
  }

  /* Status badges */
  .badge-success {
      display: inline-block;
      background: #1a3a2a;
      color: #4caf7d;
      border: 1px solid #2d6b4a;
      border-radius: 6px;
      padding: 0.3rem 0.8rem;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 0.82rem;
  }
  .badge-error {
      display: inline-block;
      background: #3a1a1a;
      color: #e05c5c;
      border: 1px solid #6b2d2d;
      border-radius: 6px;
      padding: 0.3rem 0.8rem;
      font-family: 'IBM Plex Mono', monospace;
      font-size: 0.82rem;
  }

  /* Subtle info panel */
  .info-panel {
      background: #161b27;
      border-left: 3px solid #3a7bd5;
      border-radius: 4px;
      padding: 0.6rem 1rem;
      font-size: 0.85rem;
      color: #8a9bbf;
      margin-bottom: 0.8rem;
  }
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def derive_key(password: str) -> bytes:
    """Derive a 32-byte key from a password using SHA-256."""
    return base64.urlsafe_b64encode(
        hashlib.sha256(password.encode("utf-8")).digest()
    )

def human_size(num_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if num_bytes < 1024:
            return f"{num_bytes:.1f} {unit}"
        num_bytes /= 1024
    return f"{num_bytes:.1f} TB"

def get_output_filename(original_name: str, action: str) -> str:
    name, _, ext = original_name.rpartition(".")
    if action == "Encrypt":
        return f"{name or original_name}.enc"
    # Strip .enc suffix for decryption if present
    if original_name.endswith(".enc"):
        return original_name[:-4] or "decrypted_file"
    return f"decrypted_{original_name}"

def password_strength(pw: str) -> tuple[int, str, str]:
    """Returns (score 0-4, label, color)."""
    score = 0
    if len(pw) >= 8:   score += 1
    if len(pw) >= 14:  score += 1
    if any(c.isupper() for c in pw) and any(c.islower() for c in pw): score += 1
    if any(c in "!@#$%^&*()-_=+[]{}|;:',.<>?/`~" for c in pw): score += 1
    labels = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
    colors = ["#e05c5c", "#e08c3a", "#e0c050", "#4caf7d", "#3a9bd5"]
    return score, labels[score], colors[score]


# ── Session state init ────────────────────────────────────────────────────────
for key, default in [
    ("result_data", None),
    ("result_filename", None),
    ("result_action", None),
    ("processed", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("## 🔐 File Encryption Tool")
st.markdown(
    '<div class="info-panel">Encrypt or decrypt any file locally using '
    'AES-128 symmetric encryption (Fernet). Your password never leaves your browser session.</div>',
    unsafe_allow_html=True,
)

st.divider()

# ── File upload ───────────────────────────────────────────────────────────────
uploaded_file = st.file_uploader(
    "Upload a file",
    help="Supports any file type. Max size depends on your Streamlit memory.",
)

if uploaded_file:
    file_bytes = uploaded_file.read()
    col1, col2 = st.columns(2)
    col1.metric("File name", uploaded_file.name)
    col2.metric("File size", human_size(len(file_bytes)))

    st.divider()

    # ── Operation ─────────────────────────────────────────────────────────────
    st.markdown("#### Operation")
    action = st.radio(
        "Select action",
        ["Encrypt", "Decrypt"],
        horizontal=True,
        label_visibility="collapsed",
    )

    st.markdown("#### Password")
    password = st.text_input(
        "Password",
        type="password",
        placeholder="Enter a strong password…",
        label_visibility="collapsed",
    )

    # Password strength meter
    if password:
        score, label, color = password_strength(password)
        bar_pct = int((score + 1) / 5 * 100)
        st.markdown(
            f"""
            <div style="margin-bottom:0.5rem;">
              <div style="height:5px;background:#2a2d3a;border-radius:3px;overflow:hidden;">
                <div style="height:100%;width:{bar_pct}%;background:{color};
                            border-radius:3px;transition:width 0.3s;"></div>
              </div>
              <span style="font-size:0.78rem;color:{color};">{label}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    if action == "Decrypt":
        confirm_pw = None  # No confirmation needed for decryption
    else:
        confirm_pw = st.text_input(
            "Confirm password",
            type="password",
            placeholder="Re-enter your password…",
        )

    # ── Process button ────────────────────────────────────────────────────────
    can_process = bool(password) and (
        action == "Decrypt" or password == confirm_pw
    )

    if action == "Encrypt" and password and confirm_pw and password != confirm_pw:
        st.warning("⚠️ Passwords do not match.", icon=None)

    if st.button(
        f"{'🔒 Encrypt' if action == 'Encrypt' else '🔓 Decrypt'} File",
        disabled=not can_process,
        type="primary",
        use_container_width=True,
    ):
        fernet = Fernet(derive_key(password))
        with st.spinner(f"{'Encrypting' if action == 'Encrypt' else 'Decrypting'}…"):
            if action == "Encrypt":
                st.session_state.result_data = fernet.encrypt(file_bytes)
                st.session_state.result_action = "Encrypt"
                st.session_state.processed = True
            else:
                try:
                    st.session_state.result_data = fernet.decrypt(file_bytes)
                    st.session_state.result_action = "Decrypt"
                    st.session_state.processed = True
                except InvalidToken:
                    st.error("❌ Incorrect password or the file is not a valid encrypted file.")
                    st.session_state.processed = False

        if st.session_state.processed:
            st.session_state.result_filename = get_output_filename(
                uploaded_file.name, action
            )

    # ── Download result ───────────────────────────────────────────────────────
    if st.session_state.processed and st.session_state.result_data:
        action_done = st.session_state.result_action
        st.success(f"✅ File {action_done.lower()}ed successfully!")
        st.download_button(
            label=f"⬇ Download {action_done}ed File",
            data=st.session_state.result_data,
            file_name=st.session_state.result_filename,
            mime="application/octet-stream",
            use_container_width=True,
        )

st.divider()

# ── Reset ─────────────────────────────────────────────────────────────────────
if st.button("↺ Reset Tool", use_container_width=False):
    for key in ["result_data", "result_filename", "result_action"]:
        st.session_state[key] = None
    st.session_state["processed"] = False
    st.rerun()

st.caption("Built by Vrinda Vasudev · Python Encryption Tool")