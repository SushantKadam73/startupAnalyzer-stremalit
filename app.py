import streamlit as st
import asyncio
import os
from PESTEL_Analysis import pestel_market
from advance_market_analysis import analyze_market_advanced
from internationalMarketAnalysis import analyze_market
from competitive_product_analysis import analyze_competitor
from advance_competitor_analysis import analyze_competitor_advanced
from technical_report_generator import generate_report
import modules.small_modules
import scrapers.url_to_llm_friend as url_to_llm_friend
from C_D_M import C_D_M_agent
from P_E_E import A_F_C
try:
    from C_D_M.C_D_M_agent import customer_discovery_module_agent
    from P_E_E.A_F_C import collect_feedback_of_the_user
except ModuleNotFoundError:
    st.error("The module 'cdm_pem' is not found. Please ensure it is installed and accessible.")
import markdown
import re

# Async wrappers for all analysis types
async def pestel_analysis(country: str, industry: str, company_name: str,url:str) -> str:
    return await pestel_market(country, industry, company_name)

async def advanced_market_analysis(country: str, industry: str, company_name: str,url:str) -> str:
    return await analyze_market_advanced(country, industry, company_name)

async def international_analysis(country: str, industry: str, company_name: str,url:str) -> str:
    return await analyze_market(country, industry, company_name)

async def competitor_analysis(country: str, industry: str, company_name: str,url:str) -> str:
    return await analyze_competitor(country, industry, company_name)

async def advanced_competitor_analysis(country: str, industry: str, company_name: str,url:str) -> str:
    return await analyze_competitor_advanced(country, industry, company_name)

async def technical_report(country: str, industry: str, company_name: str,url:str) -> str:
    return await generate_report(company_name, st.session_state.analysis_tool)

async def customer_discovery_analysis(country: str, industry: str, company_name: str,url:str) -> str:
    try:
        company_name=modules.small_modules.extract_website_name(url)
        report_path=C_D_M_agent.customer_discovery_module_agent(company_name)
    except:
        give_=url_to_llm_friend.url_to_llm_explainer(url)
        company_name=modules.small_modules.extract_website_name(url)
        report_path=C_D_M_agent.customer_discovery_module_agent(company_name)
    return report_path

async def Product_Evolution_Analysis(country: str, industry: str, company_name: str,url:str) -> str:
    try:
        company_name=modules.small_modules.extract_website_name(url)
        report_path=A_F_C.collect_feedback_of_the_user(company_name)
    except:
        give_=url_to_llm_friend.url_to_llm_explainer(url)
        company_name=modules.small_modules.extract_website_name(url)
        report_path=A_F_C.collect_feedback_of_the_user(company_name)
    return report_path

st.set_page_config(page_title="Startup analysis", layout="wide")

# Initialize session state for results
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = ""

st.title("Startup Analysis Tool")

# Tool Selection
with st.sidebar:
    st.header("Analysis Tools")
    analysis_tool = st.selectbox(
        "Select Analysis Type",
        [
            "PESTEL Analysis",
            "Advanced Market Analysis",
            "International Market Analysis",
            "Competitor Analysis",
            "Advanced Competitor Analysis",
            "Customer Discovery Analysis",
            "Product Evolution Analysis",
            # "Report Generator"
        ]
    )
    
    st.divider()
    
    # Common inputs
    st.header("Analysis Parameters")
    country = st.text_input("Country" )
    industry = st.text_input("Industry")
    company_name = st.text_input("Company Name")
    url = st.text_input("URL")
    
    # Single analyze button
    analyze_button = st.button("Run Analysis")

# Function mapping
analysis_functions = {
    "PESTEL Analysis": pestel_analysis,
    "Advanced Market Analysis": advanced_market_analysis,
    "International Market Analysis": international_analysis,
    "Competitor Analysis": competitor_analysis,
    "Advanced Competitor Analysis": advanced_competitor_analysis,
    "Customer Discovery Analysis": customer_discovery_analysis,
    "Product Evolution Analysis": Product_Evolution_Analysis,
    "Report Generator": technical_report
}

# Handle analysis
if analyze_button:
    # Store current analysis type in session state
    st.session_state.analysis_tool = analysis_tool
    with st.spinner('Running analysis...'):
        try:
            if analysis_tool in analysis_functions:
                # Run selected analysis asynchronously
                result_file = asyncio.run(
                    analysis_functions[analysis_tool](
                        country=country,
                        industry=industry,
                        company_name=company_name,url=url
                    )
                )
                
                # Display results
                if result_file and os.path.exists(result_file):
                    with open(result_file, 'r', encoding='utf-8') as f:
                        st.session_state.analysis_result = f.read()
                else:
                    print(result_file)
                    st.error("Analysis failed to generate results")
            else:
                st.warning("Selected analysis type not yet implemented")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Display results
if st.session_state.analysis_result:
    from markdown_pdf import MarkdownPdf, Section
    pdf = MarkdownPdf()
    pdf.meta["title"] = 'Title'
    pdf.add_section(Section(st.session_state.analysis_result, toc=False))
    pdf.save('output.pdf')
    with open("output.pdf", "rb") as pdf_file:
        st.download_button(
            label="Download Report",
            data=pdf_file,
            file_name="report.pdf",
            mime="application/octet-stream"
        )
    
    st.markdown(f"""
    <div style="background-color:#1f1f1f; padding:10px; border-radius:5px;">
    {st.session_state.analysis_result}
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div style="background-color:#1f1f1f; padding:10px; border-radius:5px;font-size:xx-small">
    <p>works best with public crawlable website</p>
    </div>
    """, unsafe_allow_html=True)

