import streamlit as st
import time
import scrapers.url_to_llm_friend as url_to_llm_friend
from C_D_M import C_D_M_agent
import C_I_S
import market_anylysis
import report_builder
import internation_market
from P_E_E import A_F_C
st.title("Report Agent")
company_name = st.text_input("Company Name")
company_url = st.text_input("Company URL")

options = ["customer discovery", "competitor intelligence", "market analysis", "international market", "user collection"]
selected_options = st.multiselect("Select report type(s):", options)

if st.button("Generate Report"):
    if not selected_options:
        st.warning("Please select at least one report type.")
    else:

        # Simulate report generation (replace with your actual report generation logic)
        with st.spinner("Generating report..."):
            if company_name!=None and company_url!=None and selected_options!=None:
                st.text(company_name)
                st.text(company_url)
                st.text(selected_options)
                if "customer discovery"in selected_options:
                    st.success("Report generated!")
                    with st.spinner("Generating report..."):
                        st.success("Report generated!")
                        with open('output.pdf',"r",encoding="utf-8") as data_f:
                            st.download_button(
                                label="Download Report",
                                data=f"{str(data_f)}",
                                file_name="large_df.pdf",
                                mime="text/x-pdf"
                            )
                    # Replace "hellow_my_lady" with actual report data
            else: 
                st.warning("Please enter a company name and URL. and sellect the module")


