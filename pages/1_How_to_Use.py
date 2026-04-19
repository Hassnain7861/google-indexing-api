import streamlit as st

st.set_page_config(page_title="How to Use", page_icon="📖", layout="centered")

st.title("📖 How to Use — Step by Step Guide")
st.caption("Follow this guide from scratch. No experience needed. Takes about 10 minutes total.")

st.info("👋 Hey! This guide will walk you through **everything** from zero to submitting your URLs to Google. Just follow the steps in order!")

# ─────────────────────────────────────────────────────────────────────────────
# OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.subheader("🗺️ Quick Overview — What We're Going to Do")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("### 1️⃣\nEnable the API in Google Cloud")
with col2:
    st.markdown("### 2️⃣\nCreate a Service Account & download key")
with col3:
    st.markdown("### 3️⃣\nAdd the account to Google Search Console")
with col4:
    st.markdown("### 4️⃣\nUse this tool to submit your URLs")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 1
# ─────────────────────────────────────────────────────────────────────────────
st.header("🔵 Step 1 — Enable the Google Indexing API")
st.markdown("Think of this like turning on a light switch before you can use it.")

with st.container(border=True):
    st.markdown("#### 1.1 — Go to Google Cloud Console")
    st.markdown("""
Go to 👉 **https://console.cloud.google.com/**

> If you've never used it before, sign in with your **Google account**.
> It's free to use for this purpose.
""")
    st.image("https://i.imgur.com/placeholder.png", caption="Google Cloud Console homepage", use_container_width=True) if False else None

    st.markdown("""
```
What you'll see:
A dark blue header with "Google Cloud" logo on the top left.
```
""")

with st.container(border=True):
    st.markdown("#### 1.2 — Create or Select a Project")
    st.markdown("""
At the **top left**, next to the Google Cloud logo, you'll see a **dropdown** that says something like *"My First Project"* or *"Select a project"*.

1. Click that dropdown
2. Click **"New Project"** (top right of the popup)
3. Give it any name, like `indexing-tool`
4. Click **"Create"**
5. Wait a few seconds, then make sure that project is selected in the dropdown
""")
    st.success("✅ You now have a project — think of it like a folder where everything lives.")

with st.container(border=True):
    st.markdown("#### 1.3 — Enable the Indexing API")
    st.markdown("""
1. In the **search bar at the top**, type:
   ```
   Indexing API
   ```
2. Click the result that says **"Web Search Indexing API"** (by Google)
3. Click the big blue **"Enable"** button

That's it for Step 1! 🎉
""")
    st.success("✅ The Indexing API is now enabled for your project.")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 2
# ─────────────────────────────────────────────────────────────────────────────
st.header("🟣 Step 2 — Create a Service Account & Download Key")
st.markdown("A Service Account is like a robot worker — it talks to Google on your behalf.")

with st.container(border=True):
    st.markdown("#### 2.1 — Open the Service Accounts page")
    st.markdown("""
1. In the **left sidebar**, click **"IAM & Admin"**
2. Then click **"Service Accounts"**

> **Can't find the sidebar?** Click the ☰ (three lines) menu icon at the top left first.
""")

with st.container(border=True):
    st.markdown("#### 2.2 — Create a new Service Account")
    st.markdown("""
1. Click **"+ Create Service Account"** at the top
2. Fill in:
   - **Name:** `indexing-api` (or anything you like)
   - **ID:** auto-fills — leave it
   - **Description:** optional
3. Click **"Create and Continue"**
4. On the next screen (Grant Access) — **skip it**, just click **"Continue"**
5. On the last screen — **skip it too**, just click **"Done"**
""")
    st.info("💡 You don't need to give it any roles — the Indexing API uses a different permission system via Search Console.")

with st.container(border=True):
    st.markdown("#### 2.3 — Download the JSON Key file")
    st.markdown("""
1. You'll now see your new service account in the list — **click on it**
2. Go to the **"Keys"** tab (at the top)
3. Click **"Add Key"** → **"Create new key"**
4. Choose **JSON** format
5. Click **"Create"**

A `.json` file will **automatically download** to your computer.

> **Keep this file safe!** It's like a password. Don't share it publicly.
""")
    st.success("✅ You now have a `service_account.json` file downloaded. Keep it safe!")
    st.warning("⚠️ Never upload this file to GitHub or share it with anyone.")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 3
# ─────────────────────────────────────────────────────────────────────────────
st.header("🟢 Step 3 — Add the Service Account to Google Search Console")
st.markdown("This tells Google: *'Yes, this robot worker is allowed to submit URLs for my website.'*")

with st.container(border=True):
    st.markdown("#### 3.1 — Find your Service Account email")
    st.markdown("""
Open the `.json` file you downloaded (open it in Notepad or any text editor).

Look for the line that says:
```json
"client_email": "something@your-project.iam.gserviceaccount.com"
```

**Copy that email address.** You'll need it in the next step.
""")

with st.container(border=True):
    st.markdown("#### 3.2 — Open Google Search Console")
    st.markdown("""
Go to 👉 **https://search.google.com/search-console/**

Sign in with the Google account that owns your website.
""")

with st.container(border=True):
    st.markdown("#### 3.3 — Add the Service Account as an Owner")
    st.markdown("""
1. Select your **website/property** from the left sidebar
2. Scroll down in the left sidebar and click **"Settings"** (gear icon ⚙️)
3. Click **"Users and permissions"**
4. Click **"Add user"** (top right)
5. Paste the **service account email** you copied
6. Set the permission to **"Owner"** ← this is important!
7. Click **"Add"**
""")
    st.success("✅ Done! The service account can now submit URLs for your site.")
    st.info("⏱️ Wait about 1–2 minutes before using the tool — Google needs a moment to apply the permission.")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# STEP 4
# ─────────────────────────────────────────────────────────────────────────────
st.header("🟡 Step 4 — Use This Tool to Submit URLs")
st.markdown("The fun part! Let's tell Google to index your pages.")

with st.container(border=True):
    st.markdown("#### 4.1 — Upload your Service Account Key")
    st.markdown("""
1. Look at the **left sidebar** of this app
2. Under **"1. Service Account"**, click **"Browse files"**
3. Find and upload the `.json` file you downloaded in Step 2
4. You'll see a green message: ✅ *Service account loaded successfully*
""")

with st.container(border=True):
    st.markdown("#### 4.2 — Choose your action")
    st.markdown("""
Still in the **left sidebar**, under **"2. Options"**:

| Option | What it does |
|---|---|
| **URL_UPDATED (index)** | Tells Google: *"Please crawl and index this page"* ✅ |
| **URL_DELETED (remove)** | Tells Google: *"Remove this page from search results"* ❌ |

👉 **Choose "URL_UPDATED"** if you just want Google to index your pages (most common case).
""")

with st.container(border=True):
    st.markdown("#### 4.3 — Add your URLs (3 ways)")

    tab1, tab2, tab3 = st.tabs(["Option A: Sitemap", "Option B: Paste", "Option C: Upload File"])

    with tab1:
        st.markdown("""
**Best for:** Submitting your whole website at once.

1. Click the **"Fetch from Sitemap"** tab in the main area
2. Type your sitemap URL, like:
   ```
   https://yourwebsite.com/sitemap.xml
   ```
3. Click **"Fetch URLs from Sitemap"**
4. The tool will find all your pages automatically!
5. (Optional) Type a keyword in the filter box to only submit certain pages

> **Don't know your sitemap URL?** Try `yourwebsite.com/sitemap.xml` or `yourwebsite.com/sitemap_index.xml`
""")

    with tab2:
        st.markdown("""
**Best for:** Submitting a few specific URLs quickly.

1. Click the **"Paste URLs"** tab
2. Type or paste your URLs, one per line:
   ```
   https://yourwebsite.com/
   https://yourwebsite.com/about
   https://yourwebsite.com/contact
   ```
""")

    with tab3:
        st.markdown("""
**Best for:** Submitting a big list you already have saved.

1. Create a `.txt` file on your computer
2. Put one URL per line
3. Click the **"Upload File"** tab
4. Upload your `.txt` file
""")

with st.container(border=True):
    st.markdown("#### 4.4 — Submit!")
    st.markdown("""
1. Once you see the green preview showing your URLs are loaded...
2. Click the big **"Submit to Google"** button
3. Watch the progress bar — it submits one URL at a time
4. When done, you'll see a results table:
   - 🟢 **Green rows** = submitted successfully
   - 🔴 **Red rows** = something went wrong (see the detail column)
""")

with st.container(border=True):
    st.markdown("#### 4.5 — Download your report")
    st.markdown("""
After submission, two download buttons appear:

- **"Download Full Report (.json)"** — complete log of everything
- **"Download Failed URLs (.txt)"** — only the ones that failed (re-upload to retry)
""")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# QUOTA
# ─────────────────────────────────────────────────────────────────────────────
st.header("📊 Important: Daily Quota Limits")

col1, col2 = st.columns(2)
with col1:
    st.metric("Default daily limit", "200 URLs/day")
with col2:
    st.metric("Per-minute limit", "~60 requests/min")

st.info("""
**Need more than 200/day?**
Go to Google Cloud Console → Your Project → "APIs & Services" → "Indexing API" → "Quotas"
→ Click the pencil icon to request an increase.
""")

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# FAQ
# ─────────────────────────────────────────────────────────────────────────────
st.header("❓ Common Problems & Fixes")

with st.expander("❌ Error: 403 — Permission denied / Failed to verify URL ownership"):
    st.markdown("""
**This means:** The service account email hasn't been added to Search Console yet, or Google hasn't applied it yet.

**Fix:**
1. Double-check you added the service account email in Search Console as an **Owner** (not just Viewer)
2. Wait 2–3 minutes and try again
3. Make sure you're submitting URLs that belong to the property in Search Console
""")

with st.expander("❌ Error: 400 — Invalid URL"):
    st.markdown("""
**This means:** One of your URLs is formatted incorrectly.

**Fix:**
- Make sure every URL starts with `https://` or `http://`
- Remove any blank lines or spaces
- Example of correct URL: `https://yourwebsite.com/page`
""")

with st.expander("❌ The JSON file upload shows an error"):
    st.markdown("""
**This means:** The file might be corrupted or it's the wrong file.

**Fix:**
- Make sure you're uploading the file downloaded from Google Cloud → Service Accounts → Keys
- It should be a `.json` file containing fields like `"type": "service_account"`
- Try downloading a fresh key from Google Cloud Console
""")

with st.expander("❌ Sitemap fetch returns 0 URLs"):
    st.markdown("""
**This means:** The tool couldn't read your sitemap.

**Fix:**
- Check the URL is correct — visit it in your browser first
- Make sure it's a valid XML sitemap (not an HTML page)
- Some sites block bots — check your `robots.txt` isn't blocking the sitemap
""")

with st.expander("✅ Submitted successfully — but pages still not indexed?"):
    st.markdown("""
**This is normal!** The Indexing API tells Google to *look at* the page, but Google still decides whether to index it.

- It can take **hours to a few days** to see results
- Check **Google Search Console → URL Inspection** to see the status
- Make sure your pages aren't blocked by `noindex` tags or `robots.txt`
""")

st.markdown("---")
st.success("🎉 That's everything! If you get stuck, re-read the relevant step above. You've got this!")
st.caption("Built with Streamlit · Google Indexing API v3")
