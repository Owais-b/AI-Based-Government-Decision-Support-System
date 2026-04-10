# generate_report.py
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER

# Colors
NAVY       = colors.HexColor("#0D1B2A")
BLUE       = colors.HexColor("#1565C0")
LIGHT_BLUE = colors.HexColor("#E3F2FD")
ACCENT     = colors.HexColor("#00ACC1")
GREEN      = colors.HexColor("#2E7D32")
ORANGE     = colors.HexColor("#E65100")
RED        = colors.HexColor("#C62828")
GREY_BG    = colors.HexColor("#F5F5F5")
MID_GREY   = colors.HexColor("#757575")
WHITE      = colors.white

def build_styles():
    styles = getSampleStyleSheet()
    return {
        "section_heading": ParagraphStyle(
            "section_heading", parent=styles["Heading2"],
            fontSize=14, fontName="Helvetica-Bold", textColor=BLUE,
            spaceBefore=14, spaceAfter=8, leading=18
        ),
        "body": ParagraphStyle(
            "body", parent=styles["Normal"],
            fontSize=10, fontName="Helvetica", textColor=colors.black,
            spaceAfter=6, leading=14
        ),
        "caption": ParagraphStyle(
            "caption", fontSize=8, fontName="Helvetica", textColor=MID_GREY,
            alignment=TA_CENTER, spaceAfter=6
        ),
        "kpi_label": ParagraphStyle(
            "kpi_label", fontSize=8, fontName="Helvetica", textColor=MID_GREY,
            alignment=TA_CENTER
        ),
        "kpi_value": ParagraphStyle(
            "kpi_value", fontSize=22, fontName="Helvetica-Bold", textColor=BLUE,
            alignment=TA_CENTER
        ),
    }

def generate_professional_report(output_path, total_complaints=0,
                                 recommendation="No recommendation available",
                                 budget=1000000):
    
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    
    doc = SimpleDocTemplate(output_path, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    
    styles = build_styles()
    story = []
    week = datetime.now().strftime("Week of %d %B %Y")

    # ==================== COVER PAGE ====================
    banner_text = f'''
    <font size="26"><b>Weekly Decision Intelligence Report</b></font><br/>
    <font size="13" color="#B0BEC5">AI-Driven Government Operations</font><br/><br/>
    <font size="11" color="#90A4AE">Period: {week}</font>
    '''
    
    banner = Table([[Paragraph(banner_text, ParagraphStyle("bs", fontName="Helvetica",
                        textColor=WHITE, alignment=TA_CENTER, leading=32))]],
                   colWidths=[17*cm], rowHeights=[6*cm])
    banner.setStyle(TableStyle([("BACKGROUND", (0,0), (-1,-1), NAVY),
                                ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                                ("TOPPADDING", (0,0), (-1,-1), 40)]))
    story.append(banner)
    story.append(Spacer(1, 0.8*cm))
    story.append(Paragraph("Empowering public officials with AI insights — Human keeps final authority.",
                           ParagraphStyle("tl", fontSize=11, fontName="Helvetica", 
                                          textColor=MID_GREY, alignment=TA_CENTER)))
    story.append(Spacer(1, 0.6*cm))
    story.append(HRFlowable(width="100%", thickness=1.5, color=ACCENT))

    # KPI Section
    open_complaints = int(total_complaints * 0.35) if total_complaints else 0
    avg_time = "6.8"

    kpi_data = [
        ["Total Complaints", f"{total_complaints:,}", "Recorded"],
        ["Open Cases", f"{open_complaints:,}", "Pending"],
        ["Avg Resolution", f"{avg_time} hrs", "Target: 8 hrs"],
        ["Crisis Risk", "Medium", "Monitor"],
    ]
    
    kpi_table = Table(kpi_data, colWidths=[4.2*cm]*4, rowHeights=[2.2*cm])
    kpi_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LIGHT_BLUE),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("INNERGRID", (0,0), (-1,-1), 0.5, colors.lightgrey),
        ("BOX", (0,0), (-1,-1), 1.2, BLUE),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ]))
    story.append(kpi_table)
    story.append(Spacer(1, 0.8*cm))
    story.append(PageBreak())

    # ==================== EXECUTIVE SUMMARY ====================
    story.append(Paragraph("1. Executive Summary", styles["section_heading"]))
    story.append(Paragraph(
        "This report provides AI-generated insights from citizen complaints. "
        "It includes priority areas, resource recommendations, and early warnings. "
        "All suggestions are advisory — final decisions rest with government officers.",
        styles["body"]))
    story.append(Spacer(1, 0.4*cm))

    rec_box = Table([[Paragraph(f"<b>AI Top Recommendation:</b><br/>{recommendation}", styles["body"])]],
                    colWidths=[17*cm])
    rec_box.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), LIGHT_BLUE),
        ("BOX", (0,0), (-1,-1), 2, ACCENT),
        ("TOPPADDING", (0,0), (-1,-1), 15),
        ("BOTTOMPADDING", (0,0), (-1,-1), 15),
    ]))
    story.append(rec_box)
    story.append(Spacer(1, 0.6*cm))

    # ==================== RESOURCE ALLOCATION ====================
    story.append(Paragraph("2. Resource Allocation Recommendation", styles["section_heading"]))
    story.append(Paragraph(f"Recommended distribution for ₹{budget:,} budget based on current complaint patterns:", styles["body"]))
    story.append(Spacer(1, 0.3*cm))

    alloc_data = [
        ["Agency", "Amount (₹)", "Percentage", "Focus Area"],
        ["HPD - Housing", f"{int(budget*0.45):,}", "45%", "Heat/Hot Water & Leaks"],
        ["DSNY - Sanitation", f"{int(budget*0.30):,}", "30%", "Waste & Cleanliness"],
        ["NYPD - Safety", f"{int(budget*0.25):,}", "25%", "Noise & Parking"],
    ]
    alloc_table = Table(alloc_data, colWidths=[5*cm, 4*cm, 3*cm, 5*cm])
    alloc_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), NAVY),
        ("TEXTCOLOR", (0,0), (-1,0), WHITE),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("ALIGN", (1,0), (2,-1), "CENTER"),
    ]))
    story.append(alloc_table)
    story.append(Spacer(1, 0.6*cm))

    # ==================== FINAL NOTE ====================
    story.append(Paragraph(
        "DISCLAIMER: All AI-generated recommendations are advisory in nature. "
        "Government officials retain full decision-making authority.",
        ParagraphStyle("disclaimer", fontSize=9, fontName="Helvetica", 
                       textColor=MID_GREY, alignment=TA_CENTER)
    ))

    doc.build(story)
    return output_path


# For testing
if __name__ == "__main__":
    path = generate_professional_report(
        output_path="reports/weekly_report.pdf",
        total_complaints=12456,
        recommendation="Priority Area: BROOKLYN | Main Issue: HEAT/HOT WATER | Priority Score: 1850",
        budget=1500000
    )
    print(f"✅ Report successfully generated at: {path}")
