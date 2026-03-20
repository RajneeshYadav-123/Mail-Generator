# import streamlit as st
# from langchain_community.document_loaders import WebBaseLoader

# from chains import Chain
# from portfolio import Portfolio
# from utils import clean_text


# def create_streamlit_app(llm, portfolio, clean_text):
#     st.title("📧 Cold Mail Generator")
#     url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
#     submit_button = st.button("Submit")

#     if submit_button:
#         try:
#             loader = WebBaseLoader([url_input])
#             data = clean_text(loader.load().pop().page_content)
#             portfolio.load_portfolio()
#             jobs = llm.extract_jobs(data)
#             for job in jobs:
#                 skills = job.get('skills', [])
#                 links = portfolio.query_links(skills)
#                 email = llm.write_mail(job, links)
#                 st.code(email, language='markdown')
#         except Exception as e:
#             st.error(f"An Error Occurred: {e}")


# if __name__ == "__main__":
#     chain = Chain()
#     portfolio = Portfolio()
#     st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
#     create_streamlit_app(chain, portfolio, clean_text)

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio):
    st.title("📧 AI Cold Mail Generator (Placement Ready)")

    url_input = st.text_input(
        "Enter Job URL:",
        value="https://www.foundit.in/job/embedded-software-engineering-technical-leader-c-c-python-npu-cisco-bengaluru-bangalore-47696854"
    )

    submit_button = st.button("Generate")

    if submit_button:
        try:
            with st.spinner("Processing..."):

                loader = WebBaseLoader([url_input])
                raw_data = loader.load().pop().page_content
                data = clean_text(raw_data)

                portfolio.load_portfolio()

                jobs = llm.extract_jobs(data)

                for job in jobs:
                    st.subheader(f"🏢 {job.get('company')} - {job.get('role')}")

                    skills = job.get("skills", [])

                    match_data = portfolio.match_skills(skills)
                    matched = match_data["matched"]
                    missing = match_data["missing"]
                    score = match_data["score"]

                    st.write(f"🎯 Skill Match Score: {score}%")
                    st.progress(score / 100)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.write("🟢 Matched Skills")
                        st.write(matched if matched else "None")

                    with col2:
                        st.write("🔴 Missing Skills")
                        st.write(missing if missing else "None")

                    links = portfolio.query_links(matched)

                    email = llm.write_mail(job, matched, missing, links)

                    st.subheader("📧 Generated Email")
                    st.code(email, language="markdown")

        except Exception as e:
            st.error(f"Error: {e}")


if __name__ == "__main__":
    st.set_page_config(
        layout="wide",
        page_title="Cold Email Generator",
        page_icon="📧"
    )

    chain = Chain()
    portfolio = Portfolio()

    create_streamlit_app(chain, portfolio)


