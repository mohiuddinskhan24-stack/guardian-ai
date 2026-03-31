import streamlit as st
import os
from openai import OpenAI
from github_integration import get_repo_files

# 🔐 Load API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 🎨 Page setup
st.set_page_config(page_title="AI Security Scanner", page_icon="🔐")

# 🌈 Styling
st.markdown("""
<style>
h1 {
    text-align: center;
    color: #00ADB5;
}
.stButton>button {
    background-color: #00ADB5;
    color: white;
    border-radius: 10px;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# 🔍 AI Function
def analyze_code(code):
    try:
        prompt = f"""
Analyze this code for security vulnerabilities including:

- SQL Injection
- Cross-Site Scripting (XSS)
- Command Injection
- Insecure API usage
- Hardcoded credentials
- Broken authentication
- Security misconfiguration

Give output in this format:

🔴 Vulnerability:
🟡 Explanation:
🟢 Fix:
⚠️ Severity:

If no vulnerability found, say: "No major vulnerability detected"

Code:
{code}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        return response.choices[0].message.content

    except Exception:
        return "⚠️ Error analyzing code (API limit or issue)"

# 🖥️ UI
st.title("🔐 AI Security Vulnerability Scanner")
st.markdown("### 🚀 Scan GitHub repositories for security issues")

repo_name = st.text_input("🔗 Enter GitHub Repo (username/repo):")

if st.button("🔍 Scan Repository"):
    if repo_name:
        with st.spinner("Scanning repository... ⏳"):
            try:
                files = get_repo_files(repo_name)

                found = False

                # 🔥 Scan only code files
                for name, code in files[:10]:

                    if not name.endswith((".py", ".js", ".java", ".cpp", ".html")):
                        continue

                    found = True

                    st.markdown(f"### 📄 {name}")
                    result = analyze_code(code)

                    st.success("✅ Scan Complete")
                    st.code(result, language="markdown")

                if not found:
                    st.warning("⚠️ No code files found to scan")

            except Exception as e:
                st.error("❌ Error: Check repo name or GitHub token")
                st.write(e)

    else:
        st.warning("⚠️ Please enter a repository name")

# 📌 Footer
st.markdown("---")
st.markdown("👨‍💻 Developed using Streamlit + OpenAI + GitHub API")
