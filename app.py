import json
import time
import xml.etree.ElementTree as ET
import requests
import pandas as pd
import streamlit as st

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Google Indexing API",
    page_icon="🔍",
    layout="centered",
)

st.title("🔍 Google Indexing API — Bulk Submitter")
st.caption("Submit URLs for indexing/deindexing via Google's Indexing API · 200 req/day default quota")

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_service(key_dict: dict):
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    creds = service_account.Credentials.from_service_account_info(
        key_dict, scopes=["https://www.googleapis.com/auth/indexing"]
    )
    return build("indexing", "v3", credentials=creds, cache_discovery=False)


def submit_url(service, url: str, notification_type: str) -> dict:
    from googleapiclient.errors import HttpError
    body = {"url": url, "type": notification_type}
    try:
        resp = service.urlNotifications().publish(body=body).execute()
        notify_time = (
            resp.get("urlNotificationMetadata", {})
                .get("latestUpdate", {})
                .get("notifyTime", "")
        )
        return {"url": url, "status": "Success", "detail": notify_time}
    except HttpError as e:
        msg = json.loads(e.content).get("error", {}).get("message", str(e))
        return {"url": url, "status": "Failed", "detail": msg}
    except Exception as e:
        return {"url": url, "status": "Failed", "detail": str(e)}


def fetch_sitemap_urls(sitemap_url: str, visited: set = None) -> list[str]:
    """Recursively fetch URLs from a sitemap or sitemap index."""
    if visited is None:
        visited = set()
    if sitemap_url in visited:
        return []
    visited.add(sitemap_url)

    try:
        resp = requests.get(sitemap_url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()
    except Exception as e:
        st.error(f"Failed to fetch sitemap: {e}")
        return []

    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError as e:
        st.error(f"Failed to parse XML: {e}")
        return []

    # Strip XML namespace for tag matching
    tag = lambda el: el.tag.split("}")[-1] if "}" in el.tag else el.tag

    urls = []
    for child in root:
        child_tag = tag(child)

        if child_tag == "sitemap":          # sitemap index → recurse
            for sub in child:
                if tag(sub) == "loc":
                    urls.extend(fetch_sitemap_urls(sub.text.strip(), visited))

        elif child_tag == "url":            # regular sitemap
            for sub in child:
                if tag(sub) == "loc":
                    urls.append(sub.text.strip())

    return urls


# ── Sidebar — Service Account ─────────────────────────────────────────────────
with st.sidebar:
    st.header("1. Service Account")
    key_file = st.file_uploader("Upload service_account.json", type="json")

    if key_file:
        try:
            key_dict = json.load(key_file)
            st.success("Service account loaded successfully.")
        except Exception as e:
            st.error(f"Invalid JSON: {e}")
            key_dict = None
    else:
        key_dict = None
        st.info("Get your key from Google Cloud Console → Service Accounts → Keys")

    st.divider()
    st.header("2. Options")
    action = st.radio("Action", ["URL_UPDATED (index)", "URL_DELETED (remove)"])
    notification_type = "URL_UPDATED" if "UPDATED" in action else "URL_DELETED"
    delay = st.slider("Delay between requests (s)", 0.5, 5.0, 1.0, 0.5)

# ── Main — URL Input ──────────────────────────────────────────────────────────
st.header("3. URLs to Submit")

tab_sitemap, tab_paste, tab_upload = st.tabs([
    "Fetch from Sitemap", "Paste URLs", "Upload File (.txt / .json)"
])

# ── Tab: Sitemap ──────────────────────────────────────────────────────────────
with tab_sitemap:
    sitemap_url = st.text_input(
        "Sitemap URL",
        placeholder="https://example.com/sitemap.xml",
    )
    fetch_btn = st.button("Fetch URLs from Sitemap", disabled=not sitemap_url)

    urls_sitemap: list[str] = st.session_state.get("urls_sitemap", [])

    if fetch_btn and sitemap_url:
        with st.spinner("Fetching sitemap..."):
            fetched = fetch_sitemap_urls(sitemap_url)
        if fetched:
            st.session_state["urls_sitemap"] = fetched
            urls_sitemap = fetched
            st.success(f"Found {len(fetched)} URLs")
        else:
            st.warning("No URLs found in sitemap.")

    if urls_sitemap:
        filter_text = st.text_input("Filter URLs (optional keyword)", key="sitemap_filter")
        displayed = (
            [u for u in urls_sitemap if filter_text.lower() in u.lower()]
            if filter_text else urls_sitemap
        )
        st.caption(f"Showing {len(displayed)} of {len(urls_sitemap)} URLs")
        st.dataframe(
            pd.DataFrame(displayed, columns=["URL"]),
            use_container_width=True,
            height=250,
        )
        if filter_text:
            st.info(f"{len(displayed)} URLs match the filter and will be submitted.")

        # store filtered selection for submit
        st.session_state["urls_sitemap_selected"] = displayed

# ── Tab: Paste ────────────────────────────────────────────────────────────────
with tab_paste:
    raw = st.text_area(
        "One URL per line",
        height=200,
        placeholder="https://example.com/\nhttps://example.com/about",
    )
    urls_paste = [u.strip() for u in raw.splitlines() if u.strip().startswith("http")]

# ── Tab: Upload ───────────────────────────────────────────────────────────────
with tab_upload:
    uploaded = st.file_uploader("Upload .txt or .json", type=["txt", "json"])
    urls_file: list[str] = []
    if uploaded:
        content = uploaded.read().decode("utf-8")
        if uploaded.name.endswith(".json"):
            data = json.loads(content)
            urls_file = data["urls"] if isinstance(data, dict) else data
        else:
            urls_file = [u.strip() for u in content.splitlines() if u.strip().startswith("http")]
        st.info(f"{len(urls_file)} URLs loaded from file")

# ── Resolve active URL list (priority: sitemap > paste > upload) ──────────────
urls_sitemap_selected = st.session_state.get("urls_sitemap_selected", [])
urls = urls_sitemap_selected or urls_paste or urls_file

# ── Preview ───────────────────────────────────────────────────────────────────
if urls:
    with st.expander(f"Preview — {len(urls)} URLs queued for submission", expanded=False):
        st.dataframe(pd.DataFrame(urls, columns=["URL"]), use_container_width=True, height=200)

# ── Submit ────────────────────────────────────────────────────────────────────
st.divider()
ready = key_dict and urls
submit_btn = st.button("Submit to Google", type="primary", disabled=not ready)

if not key_dict:
    st.warning("Upload your service account JSON in the sidebar to continue.")
elif not urls:
    st.warning("Add at least one URL using any tab above.")

if submit_btn and ready:
    try:
        service = get_service(key_dict)
    except Exception as e:
        st.error(f"Failed to authenticate: {e}")
        st.stop()

    results = []
    progress = st.progress(0, text="Starting...")
    status_box = st.empty()

    for i, url in enumerate(urls):
        status_box.markdown(f"**[{i+1}/{len(urls)}]** Submitting `{url}`...")
        result = submit_url(service, url, notification_type)
        results.append(result)
        progress.progress((i + 1) / len(urls), text=f"{i+1} / {len(urls)}")
        if i < len(urls) - 1:
            time.sleep(delay)

    status_box.empty()
    progress.empty()

    # ── Results ───────────────────────────────────────────────────────────────
    df = pd.DataFrame(results)
    success = df[df["status"] == "Success"]
    failed  = df[df["status"] == "Failed"]

    col1, col2 = st.columns(2)
    col1.metric("Submitted", len(success))
    col2.metric("Failed",    len(failed))

    st.subheader("Results")
    st.dataframe(
        df.style.apply(
            lambda row: ["background-color: #d4edda" if row["status"] == "Success"
                         else "background-color: #f8d7da"] * len(row),
            axis=1,
        ),
        use_container_width=True,
    )

    # ── Downloads ─────────────────────────────────────────────────────────────
    st.divider()
    col_a, col_b = st.columns(2)

    with col_a:
        st.download_button(
            "Download Full Report (.json)",
            data=json.dumps(results, indent=2),
            file_name="indexing_report.json",
            mime="application/json",
        )

    with col_b:
        if not failed.empty:
            st.download_button(
                "Download Failed URLs (.txt)",
                data="\n".join(failed["url"].tolist()),
                file_name="failed_urls.txt",
                mime="text/plain",
            )
        else:
            st.success("No failed URLs!")
