import os
import json
from typing import Dict, Any
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from app.config import settings

def generate_json_report(result_data: Dict[str, Any], output_path: str) -> str:
    with open(output_path, "w") as f:
        json.dump(result_data, f, indent=2)
    return output_path

def generate_pdf_report(result_data: Dict[str, Any], output_path: str) -> str:
    """
    Generates a PDF analysis report for SatQuery AI execution.
    """
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )
    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=22,
        leading=26,
        textColor=colors.HexColor('#0F172A'),
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#64748B'),
        fontName='Helvetica'
    )

    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=14,
        leading=18,
        textColor=colors.HexColor('#1E293B'),
        fontName='Helvetica-Bold',
        spaceBefore=12,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#334155'),
        fontName='Helvetica'
    )

    # Header
    story.append(Paragraph("SATQUERY AI — ANALYSIS REPORT", title_style))
    story.append(Paragraph("Interactive Agentic Vision-Language Remote-Sensing Intelligence Platform", subtitle_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#3B82F6'), spaceAfter=15))

    # Query & Summary Table
    conf_val = result_data.get("confidence", {}).get("value", 0.9) * 100
    conf_type = result_data.get("confidence", {}).get("type", "estimated")

    summary_table_data = [
        [Paragraph("<b>Execution ID:</b>", body_style), Paragraph(str(result_data.get("execution_id")), body_style)],
        [Paragraph("<b>Timestamp:</b>", body_style), Paragraph(str(result_data.get("timestamp")), body_style)],
        [Paragraph("<b>Analysis Mode:</b>", body_style), Paragraph(str(result_data.get("input_type")).upper(), body_style)],
        [Paragraph("<b>Identified Task:</b>", body_style), Paragraph(str(result_data.get("task")).upper(), body_style)],
        [Paragraph("<b>User Query:</b>", body_style), Paragraph(f"<i>\"{result_data.get('query')}\"</i>", body_style)],
        [Paragraph("<b>Overall Confidence:</b>", body_style), Paragraph(f"<b>{conf_val:.1f}%</b> ({conf_type})", body_style)]
    ]

    t_summary = Table(summary_table_data, colWidths=[140, 380])
    t_summary.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_summary)
    story.append(Spacer(1, 15))

    # AI Answer Section
    story.append(Paragraph("AI Intelligence Analysis Result", heading_style))
    answer_text = result_data.get("answer", "No response generated.")
    story.append(Paragraph(answer_text.replace("\n", "<br/>"), body_style))
    story.append(Spacer(1, 15))

    # Observable Agent Execution Trace Table
    story.append(Paragraph("Observable Agent Execution Trace", heading_style))
    trace_data = [[Paragraph("<b>Step Name</b>", body_style), Paragraph("<b>Status</b>", body_style), Paragraph("<b>Detail</b>", body_style)]]
    for step in result_data.get("execution_steps", []):
        trace_data.append([
            Paragraph(step.get("name"), body_style),
            Paragraph(f"<font color='green'><b>{step.get('status').upper()}</b></font>", body_style),
            Paragraph(step.get("detail", ""), body_style)
        ])

    t_trace = Table(trace_data, colWidths=[160, 80, 280])
    t_trace.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_trace)
    story.append(Spacer(1, 15))

    # Visual Evidence References
    story.append(Paragraph("Generated Visual Evidence", heading_style))
    evidence_data = [[Paragraph("<b>Title</b>", body_style), Paragraph("<b>Type</b>", body_style), Paragraph("<b>Reference</b>", body_style)]]
    for item in result_data.get("evidence", []):
        evidence_data.append([
            Paragraph(item.get("title"), body_style),
            Paragraph(item.get("type"), body_style),
            Paragraph(item.get("url"), body_style)
        ])

    t_evidence = Table(evidence_data, colWidths=[180, 100, 240])
    t_evidence.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F1F5F9')),
        ('PADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    story.append(t_evidence)
    story.append(Spacer(1, 20))

    # Footer
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceAfter=10))
    story.append(Paragraph("Generated automatically by SatQuery AI Platform — Grounded Geospatial Intelligence", subtitle_style))

    doc.build(story)
    return output_path
