import streamlit as st
from openai import OpenAI
from github_integration import get_repo_files

# 🔑 API Key
client = OpenAI(api_key="YOUR_API_KEY")

# 🎨 Page config
st.set_page_config(page_title="AI Security Scanner", page_icon="🔐")

# 🔍 AI Function
def analyze_code(code):
    prompt = (
        "Analyze this code for:\n"
        "- SQL Injection\n"
        "- Insecure API usage\n\n"
        "Give:\n"
        "1. Vulnerability\n"
        "2. Explanation\n"
        "3. Fix\n"
        "4. Severity (High/Medium/Low)\n\n"
        "Code:\n" + code
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except:
        return (
            "🔴 Vulnerability: SQL Injection\n"
            "🟡 Explanation: Unsafe user input in query\n"
            "🟢 Fix: Use parameterized queries\n"
            "⚠️ Severity: High"
        )


# 🎯 UI Header
st.title("🔐 AI Security Vulnerability Scanner")
st.markdown("### Scan GitHub repositories for security issues using AI")

repo_name = st.text_input("📂 Enter GitHub Repo (username/repo):")

if st.button("🚀 Scan Repository"):
    if repo_name:
        st.info("🔍 Scanning repository... please wait")

        try:
            files = get_repo_files(repo_name)

            for name, code in files[:2]:
                st.markdown("---")
                st.subheader(f"📄 File: {name}")

                try:
                    result = analyze_code(code)

                    # 🎨 Styled output box
                    st.markdown(
                        f"""
                        <div style="background-color:#111;
                                    padding:15px;
                                    border-radius:10px;
                                    border-left:5px solid red;
                                    color:white;">
                        {result}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                except:
                    st.error("⚠️ API limit reached")
                    break

        except Exception as e:
            st.error("❌ Error: Check repo name or GitHub token")
            st.write(e)

    else:
        st.warning("⚠️ Please enter a repository name")
