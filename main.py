
import datetime
import logging
import time
from io import BytesIO

import colorsys
import plotly.graph_objects as go
import streamlit as st
import requests
from fpdf import FPDF

# Session State Initialization
# Helper Functions
def safe_float_conversion(value):
    try:
        return float(value)
    except ValueError:
        return 0.0



st.header("Carbon Conscious: "
          "Track and Reduce Your Footprint")
st.markdown("This project is part of the M602A Computer Programming (WS0124) course, designed to offer a "
            " practical experience in assessing the carbon footprint associated with energy consumption, "
            " waste production, and business travel.")

tabs = st.tabs(["New Report", "Energy Usage", "Waste Usage", "Business Travel", "Analysis", "About"])

################################################################################################
################################## New Report #############################
################################################################################################
with tabs[0]:
    st.markdown("#### New Report UUID")
    st.markdown("Press the button below to create an UUID that you can use for the next report. You can use "
                "UUID to update the previous report as well.")
    if st.button("Generate Report"):
        response = requests.get("http://localhost:8080/register")

        if response.status_code == 201:
            report_data = response.json()
            st.write("Your report UUID:")
            st.write(report_data["report_uuid"])

        else:
            st.error("Report generation failed. Please try again.")

################################################################################################
################################### create ENERGY ############################
################################################################################################
with tabs[1]:
    with st.expander("Create new report for Energy Usage sector"):

        report_uuid = st.text_input("Report UUID for Energy sector")
        average_monthly_bill = st.number_input(
            "Average Monthly Bill (Euro)", value=0.0
        )  # Default to 0.0
        average_natural_gas_bill = st.number_input("Average Natural Gas Bill (Euro)", value=0.0)
        monthly_fuel_bill = st.number_input("Monthly Fuel Bill (Euro)", value=0.0)
        city = st.text_input("City for energy sector")
        company_name = st.text_input("Company Name for energy sector")

        if st.button("Create new Energy report"):
            data = {
                "report_uuid": report_uuid,
                "average_monthly_bill": average_monthly_bill,
                "average_natural_gas_bill": average_natural_gas_bill,
                "monthly_fuel_bill": monthly_fuel_bill,
                "city": city,
                "company_name": company_name,
            }

            response = requests.post("http://localhost:8080/create-energy-usage", json=data)

            if response.status_code == 200:
                st.success("Data submitted successfully!")
            else:
                st.error("An error occurred. Please try again.")

    ############################################  get  ENERGY   ########################################################
    # Get Reports Section
    st.markdown("#### Withdraw all reports for the specific company")
    company_name_for_reports = st.text_input("Company Name for Energy Reports")

    if st.button("Show All Reports energy usage"):
        data = {"company_name": company_name_for_reports}
        response = requests.get("http://localhost:8080/get-energy-usage", params=data)
        if response.status_code == 200:
            reports_data = response.json()["data"]
            if reports_data:
                st.write("Reports:")
                for report in reports_data:
                    st.write(f"Report UUID: {report['report_uuid']}")
                    st.write(f"City: {report['city']}")
                    st.write(f"Carbon Footprint: {report['carbon_footprint']} kg")
                    st.write(f"Created : {report['created_at']}")
                    st.write("-" * 20)  # Separator
            else:
                st.write("No reports found for this company.")
        else:
            st.error("An error occurred fetching reports.")

    ################################################################################################
    #################### create WASTE ###############
    ################################################################################################
with tabs[2]:
    with st.expander("Create new report for Waste Usage sector"):

        report_uuid = st.text_input("Report UUID for waste sector")
        waste_kg = st.number_input(
            "Waste (kg)", value=0.0
        )  # Default to 0.0
        recycled_or_composted_kg = st.number_input("Recycled or Composted %", value=0.0)
        waste_category_enum = st.text_input("Waste Category (only recyclable)", value="recyclable")
        city = st.text_input("City for waste sector")
        company_name = st.text_input("Company Name waste sector")

        if st.button("Create new Waste report"):
            data = {
                "report_uuid": report_uuid,
                "waste_kg": waste_kg,
                "recycled_or_composted_kg": recycled_or_composted_kg,
                "waste_category_enum": waste_category_enum,
                "city": city,
                "company_name": company_name,
            }

            response = requests.post("http://localhost:8080/create-waste-sector", json=data)

            if response.status_code == 200:
                st.success("Data submitted successfully!")
            else:
                st.error("An error occurred. Please try again.")

    ##########################################  GET WASTE   ######################################################
    st.markdown("#### Withdraw all reports for the specific company")
    company_name_for_reports = st.text_input("Company Name for Reports waste sector")

    if st.button("Show All Reports for waste sector"):
        data = {"company_name": company_name_for_reports}
        response = requests.get("http://localhost:8080/get-waste-sector", params=data)
        if response.status_code == 200:
            reports_data = response.json()["data"]
            if reports_data:
                st.write("Reports:")
                for report in reports_data:
                    st.write(f"Report UUID: {report['report_uuid']}")
                    st.write(f"City : {report['city']}")
                    st.write(f"Carbon Footprint: {report['carbon_footprint']} kg")
                    st.write(f"Created : {report['created_at']}")
                    st.write("-" * 20)  # Separator
            else:
                st.write("No reports found for this company.")
        else:
            st.error("An error occurred fetching reports.")
    ############################################################################################
    ############################################################################################

with tabs[3]:
    ############################################################################################
    ##### create BUSINESS
    ############################################################################################
    with st.expander("Create new report for Business sector"):

        report_uuid = st.text_input("Report UUID for Business sector")
        kilometers_per_year = st.number_input(
            "Kilometers per year (km)", value=0.0
        )  # Default to 0.0
        average_efficiency_per_100km = st.number_input("Average efficiency per 100km (L)", value=0.0)
        city = st.text_input("City for business sector")
        company_name = st.text_input("Company Name for business sector")

        if st.button("Create new report for Business sector"):
            data = {
                "report_uuid": report_uuid,
                "kilometers_per_year": kilometers_per_year,
                "average_efficiency_per_100km": average_efficiency_per_100km,
                "city": city,
                "company_name": company_name,
            }

            response = requests.post("http://localhost:8080/create-business-travel", json=data)

            if response.status_code == 200:
                st.success("Data submitted successfully!")
            else:
                st.error("An error occurred. Please try again.")

    ############################################################################################
    ##### Get BUSINESS
    ############################################################################################
    st.markdown("#### Withdraw all reports for the specific company")
    company_name_for_reports = st.text_input("Company Name for Reports business sector")

    if st.button("Show All Reports for business sector"):
        data = {"company_name": company_name_for_reports}
        response = requests.get("http://localhost:8080/get-business-travel", params=data)
        if response.status_code == 200:
            reports_data = response.json()["data"]
            if reports_data:
                st.write("Reports:")
                for report in reports_data:
                    st.write(f"Report UUID: {report['report_uuid']}")
                    st.write(f"City : {report['city']}")
                    st.write(f"Carbon Footprint: {report['carbon_footprint']} kg")
                    st.write(f"Created : {report['created_at']}")
                    st.write("-" * 20)
            else:
                st.write("No reports found for this company.")
        else:
            st.error("An error occurred fetching reports.")

################################################################################################
############# ANALYSE ###########
################################################################################################
def create_pdf_report(company_name, recommendations_data, chart_figure):
        logger = logging.getLogger(__name__)  # Create a logger
        logger.setLevel(logging.DEBUG)  # Set to DEBUG mode for detailed output

        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('ArialUnicode', fname='./ArialUnicode.ttf')
        pdf.set_font("ArialUnicode", size=12)  # Normal text

        # Title
        pdf.cell(200, 10, text=f"{company_name} Carbon Footprint Report", new_x="LMARGIN", new_y="NEXT", align="C")
        pdf.cell(200, 10, text=f"Date: {datetime.date.today()}", new_x="LEFT", new_y="NEXT", align="C")

        # Recommendations
        pdf.ln(10)

        pdf.set_font("Helvetica", size=12)  # Instead of 'Arial'
        pdf.cell(200, 10, text="...", align="C", new_x="LMARGIN", new_y="NEXT")  # Instead of ln=...

        pdf.set_font("ArialUnicode", size=12)  # Normal text

        logger.debug("Starting recommendations text section")
        try:
            recommendation_text = recommendations_data['data']['recommendation']  # Extract the text
            recommendations_encoded = recommendation_text.encode('utf-8')  # Encode the extracted text
            pdf.multi_cell(0, 5, recommendations_encoded.decode('utf-8'))
        except Exception as e:
            logger.error(f"Error encoding recommendations: {e}")

        # Diagram
        pdf.ln(10)
        pdf.set_font("ArialUnicode", size=12)  # Removed 'B' for bold

        pdf.cell(200, 10, text="Carbon Footprint Distribution", new_x="LMARGIN", new_y="NEXT", align="L")

        buffer = BytesIO()
        chart_figure.write_image(buffer, format='png')  # Potentially add 'engine' parameter
        pdf.image(buffer, x=40, y=pdf.get_y() + 10, w=120)
        pdf.output(f"carbon_report_for_{company_name}.pdf")

with (tabs[4]):
    st.markdown("#### Carbon Footprint Analysis")

    company_name_for_recommendation = st.text_input("Enter Company Name:")

    if st.button("Fetch Records and Generate Recommendations"):
        with st.spinner("Processing data..."):
            data = {"company_name": company_name_for_recommendation}
            response = requests.get("http://localhost:8080/give-recommendation", params=data)

            if response.status_code == 200:
                recommendations_data = response.json()

                st.subheader("Carbon Footprint Breakdown")

                col1, col2 = st.columns(2)

                with col1:
                    if "recommendation" in recommendations_data["data"]:
                        st.write(recommendations_data["data"]["recommendation"])
                        st.write("\n")
                    else:
                        st.write("Recommendations not yet available.")

                with col2:

                    def safe_float_conversion(value):
                        try:
                            return float(value)
                        except ValueError:
                            return 0.0

                    total_carbon_footprint = sum(
                        safe_float_conversion(value)
                        for value in recommendations_data["data"].values()
                        if isinstance(value, (int, float))
                    )

                    if total_carbon_footprint != 0:
                        percentages = [(value / total_carbon_footprint) * 100 for value in
                                       recommendations_data["data"].values() if isinstance(value, (int, float))]
                    else:
                        percentages = [0, 0, 0]

                    labels = ["business_travel", "energy_usage", "waste_sector"]


                    num_segments = 3  # Number of segments per slice
                    colors = ['#E94C3C', '#3D9970', '#0074D9']
                    all_labels = []
                    all_values = []

                    for label, value, color in zip(labels, percentages, colors):
                        all_labels.extend([label] * num_segments)
                        all_values.extend([value / num_segments] * num_segments)

                    fig = go.Figure(data=[go.Pie(labels=labels, values=percentages, hole=0.5, marker_colors=colors)])
                    fig.update_layout(
                        title_text=f"Carbon Footprint Distribution (Percentage) for {company_name_for_recommendation}"

                    )

                    st.plotly_chart(fig)

                    st.write("Download DPF and close the report")  # Debugging

                    create_pdf_report(company_name_for_recommendation, recommendations_data, fig)
                    with open(f"carbon_report_for_{company_name_for_recommendation}.pdf", "rb") as pdf_file:
                        st.download_button(
                            label="Download PDF Report",
                            data=pdf_file,
                            file_name=f"carbon_report_for_{company_name_for_recommendation}.pdf",
                            mime="application/octet-stream"
                        )


            else:
                st.error("An error occurred while fetching the records.")


with tabs[5]:
    markdown_text = """
### Resources
* **Project Repository** [https://github.com/Pakhomovskii/gisma_computer_programming_project](https://github.com/Pakhomovskii/gisma_computer_programming_project)
* **API Documentation:** http://64.226.89.177/api/doc 
#### For any questions please contact me
* **LinkedIn:** [www.linkedin.com/in/aleksandr-pakhomovskii-31874a217](www.linkedin.com/in/aleksandr-pakhomovskii-31874a217)
* **Email:** pakhomovskii@gmail.com

"""
    st.markdown(markdown_text, unsafe_allow_html=True)
