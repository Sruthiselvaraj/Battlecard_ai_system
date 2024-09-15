import streamlit as st
import requests

st.title('Battlecard Generator')

# Inputs for competitors, industry, and product info
competitors_input = st.text_input('Competitor Names (comma-separated)')
industry = st.text_input('Industry Keywords')
product_info = st.text_area('Product Information')

# Generate battlecard when the button is clicked
if st.button('Generate Battlecard'):
    if competitors_input and industry and product_info:
        try:
            # Step 1: Collect data from competitors and industry
            competitors = [comp.strip() for comp in competitors_input.split(',')]
            
            # Collect data from API
            collect_data_response = requests.post(
                "http://127.0.0.1:8000/collect_data/",
                json={"competitors": competitors, "industry": industry}
            )
            collect_data_response.raise_for_status()
            raw_data = collect_data_response.json().get('data', {})

            # Step 2: Analyze the collected data
            analyze_data_response = requests.post(
                "http://127.0.0.1:8000/analyze_data/",
                json=raw_data
            )
            analyze_data_response.raise_for_status()
            analyzed_data = analyze_data_response.json().get('analyzed_data', {})

            # Prepare competitors data with strengths and weaknesses from API
            competitors_data = []
            for comp in competitors:
                strength = analyzed_data.get(comp, {}).get('strengths', '')
                weakness = analyzed_data.get(comp, {}).get('weaknesses', '')
                competitors_data.append({
                    "name": comp,
                    "strengths": strength,
                    "weaknesses": weakness
                })

            # Step 3: Generate textual battlecard from analyzed data
            generate_battlecard_response = requests.post(
                "http://127.0.0.1:8000/generate_battlecard/",
                json={
                    "competitors": competitors_data,
                    "product_info": product_info,
                    "industry": industry
                }
            )
            generate_battlecard_response.raise_for_status()
            battlecard_text = generate_battlecard_response.json().get('battlecard', '')

            # Display the textual battlecard
            st.text_area("Generated Battlecard", battlecard_text, height=300)

            # Step 4: Design the battlecard as a PDF
            design_battlecard_response = requests.post(
                "http://127.0.0.1:8000/design_battlecard/",
                json={
                    "competitors": competitors_data,
                    "product_info": product_info,
                    "industry": industry
                }
            )
            design_battlecard_response.raise_for_status()

            # Step 5: Provide the download button for the generated PDF
            st.download_button(
                label="Download Battlecard PDF",
                data=design_battlecard_response.content,
                file_name="battlecard.pdf",
                mime="application/pdf"
            )

        except requests.RequestException as e:
            st.error(f"Error: {e}")
    else:
        st.error("Please provide all required inputs.")
