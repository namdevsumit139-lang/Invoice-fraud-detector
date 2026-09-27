import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import io

# Page Configuration
st.set_page_config(
    page_title="Enterprise ESG & Carbon Auditor", 
    page_icon="🌱", 
    layout="wide"
)

# Custom CSS for Modern Styling & Attractive Look
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1b4332;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-text {
        color: #52796f;
        font-size: 1.1rem;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# Language Dictionary (Translations)
# ==========================================
translations = {
    "English": {
        "title": "🌱 Enterprise ESG & Carbon Footprint Auditor",
        "subtitle": "Next-gen corporate sustainability analytics & environmental compliance platform",
        "sidebar_header": "🏢 Corporate Data Input",
        "sidebar_desc": "Configure metrics for audit evaluation:",
        "preset_label": "⚡ Load Real-Time Industry Preset",
        "company_name": "Company Name",
        "electricity": "Monthly Electricity (kWh)",
        "fuel": "Fuel Consumption (Liters)",
        "travel": "Business Travel (KM)",
        "run_btn": "🚀 Run ESG Audit",
        "audit_report_for": "📋 Executive Audit Dashboard:",
        "dashboard_desc": "Real-time tracking of scope emissions, compliance readiness, and reduction pathways.",
        "elec_metric": "⚡ Electricity Emission",
        "fuel_metric": "⛽ Fuel Emission",
        "travel_metric": "✈️ Travel Emission",
        "summary_title": "📊 Carbon Footprint Intelligence Summary",
        "high_risk": "⚠️ **High Carbon Risk Alert:** **{company}** total monthly emission is **{emission:.2f} Tons CO2**. Immediate mitigation required for ESG compliance.",
        "optimized": "✅ **Optimized Standing:** **{company}** total monthly emission is **{emission:.2f} Tons CO2**. Within acceptable green thresholds.",
        "recs": """**💡 AI-Driven Corporate Sustainability Recommendations:**
1. **Renewable Energy Transition:** Shift 40% of grid electricity to on-site solar installations to drastically drop scope-2 electricity emissions.
2. **Fleet Electrification:** Convert corporate logistics and transport fleets to Electric Vehicles (EVs) to mitigate diesel/petrol penalties.
3. **Green Travel Framework:** Enforce virtual-first meetings for regional branches to minimize high-emission business air and road travel.""",
        "pdf_btn": "📥 Download Official ESG Audit PDF Report"
    },
    "हिन्दी": {
        "title": "🌱 एंटरप्राइज़ ESG और कार्बन फ़ुटप्रिंट ऑडिटर",
        "subtitle": "अगली पीढ़ी का कॉर्पोरेट स्थिरता एनालिटिक्स और पर्यावरण अनुपालन मंच",
        "sidebar_header": "🏢 कॉर्पोरेट डेटा इनपुट",
        "sidebar_desc": "ऑडिट मूल्यांकन के लिए मेट्रिक्स कॉन्फ़िगर करें:",
        "preset_label": "⚡ रीयल-टाइम इंडस्ट्री प्रीसेट लोड करें",
        "company_name": "कंपनी का नाम",
        "electricity": "मासिक बिजली की खपत (kWh)",
        "fuel": "ईंधन की खपत (लीटर)",
        "travel": "व्यापारिक यात्रा (KM)",
        "run_btn": "🚀 ESG ऑडिट चलाएं",
        "audit_report_for": "📋 कार्यकारी ऑडिट डैशबोर्ड:",
        "dashboard_desc": "स्कोप एमिशन, अनुपालन तत्परता और कमी के रास्तों की रीयल-टाइम ट्रैकिंग।",
        "elec_metric": "⚡ बिजली से उत्सर्जन",
        "fuel_metric": "⛽ ईंधन से उत्सर्जन",
        "travel_metric": "✈️ यात्रा से उत्सर्जन",
        "summary_title": "📊 कार्बन फुटप्रिंट इंटेलिजेंस सारांश",
        "high_risk": "⚠️ **उच्च कार्बन जोखिम चेतावनी:** **{company}** का कुल मासिक उत्सर्जन **{emission:.2f} टन CO2** है। ESG अनुपालन के लिए तत्काल सुधार आवश्यक है।",
        "optimized": "✅ **अनुकूलित स्थिति:** **{company}** का कुल मासिक उत्सर्जन **{emission:.2f} टन CO2** है। स्वीकार्य ग्रीन सीमाओं के भीतर।",
        "recs": """**💡 AI-संचालित कॉर्पोरेट स्थिरता सिफ़ारिशें:**
1. **अक्षय ऊर्जा संक्रमण:** स्कोप-2 बिजली उत्सर्जन को भारी रूप से कम करने के लिए ग्रिड बिजली का 40% ऑन-साइट सौर प्रतिष्ठानों में स्थानांतरित करें।
2. **फ्लीट विद्युतीकरण:** डीजल/पेट्रोल पेनल्टी को कम करने के लिए कॉर्पोरेट लॉजिस्टिक्स और ट्रांसपोर्ट फ्लीट को इलेक्ट्रिक वाहनों (EVs) में बदलें।
3. **ग्रीन ट्रैवल फ्रेमवर्क:** उच्च-उत्सर्जन व्यावसायिक हवाई और सड़क यात्रा को कम करने के लिए क्षेत्रीय शाखाओं के लिए वर्चुअल-फर्स्ट बैठकों को लागू करें.""",
        "pdf_btn": "📥 आधिकारिक ESG ऑडिट PDF रिपोर्ट डाउनलोड करें"
    }
}

# ==========================================
# Sidebar Language Selector
# ==========================================
st.sidebar.markdown("### 🌐 Language / भाषा")
selected_lang = st.sidebar.selectbox("Choose Language", ["English", "हिन्दी"], label_visibility="collapsed")
lang = translations[selected_lang]

# Top Header & Branding
st.markdown(f'<p class="main-header">{lang["title"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-text">{lang["subtitle"]}</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar - Real-Time Industry Presets
st.sidebar.markdown(f"### {lang['sidebar_header']}")
industry_preset = st.sidebar.selectbox(
    lang['preset_label'],
    ["Custom Input", "Global Tech Giant (Low Impact)", "Heavy Manufacturing Corp (High Impact)", "Logistics & Supply Chain Fleet"]
)

# Set default values based on Real-Time Industry Presets
if industry_preset == "Global Tech Giant (Low Impact)":
    default_name = "Apex Tech Solutions"
    default_elec = 8000.0
    default_fuel = 500.0
    default_travel = 2000.0
elif industry_preset == "Heavy Manufacturing Corp (High Impact)":
    default_name = "Titan Industrial Ltd"
    default_elec = 45000.0
    default_fuel = 12000.0
    default_travel = 15000.0
elif industry_preset == "Logistics & Supply Chain Fleet":
    default_name = "SwiftGlobal Logistics"
    default_elec = 15000.0
    default_fuel = 25000.0
    default_travel = 30000.0
else:
    default_name = "ABC Global Corp"
    default_elec = 15000.0
    default_fuel = 2000.0
    default_travel = 5000.0

company_name = st.sidebar.text_input(lang['company_name'], default_name)
electricity_kwh = st.sidebar.number_input(lang['electricity'], min_value=0.0, value=default_elec, step=500.0)
fuel_liters = st.sidebar.number_input(lang['fuel'], min_value=0.0, value=default_fuel, step=100.0)
travel_km = st.sidebar.number_input(lang['travel'], min_value=0.0, value=default_travel, step=200.0)

# Execution Button in Sidebar
st.sidebar.markdown("---")
run_audit = st.sidebar.button(lang['run_btn'], type="primary", use_container_width=True)

# Main Screen Header with Company Focus
st.markdown(f"### {lang['audit_report_for']} **{company_name}**")
st.write(lang['dashboard_desc'])

# Calculation Logic (Standard Emission Factors)
elec_emission = (electricity_kwh * 0.82) / 1000  # Tons CO2
fuel_emission = (fuel_liters * 2.68) / 1000      # Tons CO2
travel_emission = (travel_km * 0.15) / 1000      # Tons CO2

total_carbon_emission = elec_emission + fuel_emission + travel_emission

# Dashboard Metrics Layout
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label=lang['elec_metric'], value=f"{elec_emission:.2f} Tons", delta="-1.2%")
with col2:
    st.metric(label=lang['fuel_metric'], value=f"{fuel_emission:.2f} Tons", delta="+0.8%")
with col3:
    st.metric(label=lang['travel_metric'], value=f"{travel_emission:.2f} Tons", delta="0.0%")

st.divider()

# Total Impact Summary & Recommendations
st.subheader(lang['summary_title'])

if total_carbon_emission > 25:
    st.error(lang['high_risk'].format(company=company_name, emission=total_carbon_emission))
else:
    st.success(lang['optimized'].format(company=company_name, emission=total_carbon_emission))

st.info(lang['recs'])

st.divider()

# ==========================================
# PDF Report Generation Function using ReportLab
# ==========================================
def generate_pdf(comp_name, elec, fuel, travel, total):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'ReportTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=colors.HexColor('#1b4332'),
        spaceAfter=10
    )
    normal_style = styles['Normal']
    
    # PDF Header Content
    story.append(Paragraph("Enterprise ESG & Carbon Audit Report", title_style))
    story.append(Paragraph(f"<b>Company Name:</b> {comp_name}", normal_style))
    story.append(Paragraph("<b>Status:</b> Official Corporate Compliance Evaluation", normal_style))
    story.append(Spacer(1, 15))
    
    # Data Table for PDF
    data = [
        ["Emission Category", "Metric Data", "Carbon Output (Tons CO2)"],
        ["Electricity Consumption", f"{elec:,.2f} kWh", f"{elec_emission:.2f}"],
        ["Fuel Consumption", f"{fuel:,.2f} Liters", f"{fuel_emission:.2f}"],
        ["Business Travel", f"{travel:,.2f} KM", f"{travel_emission:.2f}"],
        ["Total Carbon Footprint", "-", f"{total:.2f} Tons"]
    ]
    
    table = Table(data, colWidths=[180, 150, 150])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2d6a4f')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#d8f3dc')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
    ]))
    
    story.append(table)
    story.append(Spacer(1, 15))
    story.append(Paragraph("<b>AI-Driven Recommendations & Mitigation Strategy:</b>", styles['Heading3']))
    story.append(Paragraph("1. Transition grid power to renewable solar/wind installations.", normal_style))
    story.append(Paragraph("2. Optimize supply chain logistics and shift transport fleets to EVs.", normal_style))
    story.append(Paragraph("3. Implement a strict green travel and virtual-first meeting framework.", normal_style))
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# PDF Download Button in Streamlit
pdf_data = generate_pdf(company_name, electricity_kwh, fuel_liters, travel_km, total_carbon_emission)

st.download_button(
    label=lang['pdf_btn'],
    data=pdf_data,
    file_name=f"{company_name}_ESG_Audit_Report.pdf",
    mime="application/pdf",
    type="primary"
)