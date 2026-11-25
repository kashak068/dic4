import os, sys
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont('Helvetica', 8)
        self.setFillColor(colors.HexColor('#666666'))
        doc_type = getattr(self, '_doc_title_tag', 'IEEE Draft')
        self.drawString(54, 750, f'ICEIB 2027 / IEEE Conference Submission Draft — [{doc_type}]')
        self.drawRightString(612 - 54, 36, f'Page {self._pageNumber} of {page_count}')
        self.restoreState()

def build_bad_pdf(filename="paper_draft_flawed_bad.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'BadTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        alignment=1,
        textColor=colors.HexColor('#990000')
    )
    sub_style = ParagraphStyle(
        'BadSub',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=14,
        alignment=1,
        textColor=colors.HexColor('#555555')
    )
    h1_style = ParagraphStyle(
        'BadH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#111111'),
        spaceBefore=12,
        spaceAfter=6
    )
    h2_style = ParagraphStyle(
        'BadH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor('#222222'),
        spaceBefore=8,
        spaceAfter=4
    )
    body_style = ParagraphStyle(
        'BadBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#222222'),
        spaceAfter=6
    )
    flaw_box = ParagraphStyle(
        'FlawBox',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#990000')
    )

    def make_flaw_callout(title, text):
        content = [
            Paragraph(f"<b>[CRITICAL PEER-REVIEW DEFECT / FLAW] {title}</b>", flaw_box),
            Spacer(1, 2),
            Paragraph(text, flaw_box)
        ]
        t = Table([[content]], colWidths=[504])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFF0F0')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#D32F2F')),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return t

    story = []
    
    # Header Banner
    banner_text = Paragraph(
        "<b>FLAWED / UNREFACTORED DRAFT (BEFORE REFACTORING)</b><br/>"
        "<font size=8>This version illustrates the common academic pitfalls, superficial literature review ('paper dump'), "
        "and lack of rigorous problem formulation that lead to IEEE conference paper rejection.</font>",
        ParagraphStyle('Banner', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=14, alignment=1, textColor=colors.HexColor('#B71C1C'))
    )
    b_table = Table([[banner_text]], colWidths=[504])
    b_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFCDD2')),
        ('BOX', (0,0), (-1,-1), 1.5, colors.HexColor('#B71C1C')),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(b_table)
    story.append(Spacer(1, 14))

    # Title & Authors
    story.append(Paragraph("AirSleuth: Using IoT Sensors and AI to Answer Air Quality Questions", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Student Authors: Yen-Kai Chen, Hong-Yu Chen, Ting-Chang Wang, Chia-Feng Li, Sheng-Ru Chou", sub_style))
    story.append(Spacer(1, 10))

    # Flawed Abstract
    story.append(Paragraph("<b>Abstract</b>", h2_style))
    story.append(Paragraph(
        "Air quality is bad in many places and PM2.5 causes a lot of deaths. Taiwan has over 10,000 sensors, but people only get colors and numbers. "
        "They don't know why it is bad or what to do. In this project we build an AI agent called AirSleuth that uses LLM and tools to analyze PM2.5 data. "
        "We collected data from Taichung and Kaohsiung and tested our system. It works well and can answer user questions nicely.",
        body_style
    ))
    story.append(make_flaw_callout(
        "Unstructured Abstract Lacking A~F Rigor & Quantitative Proof",
        "The abstract violates IEEE conventions: it fails to follow the structured A~F progression (Attention, Bottleneck, Cure, Development, Experiments, Findings). "
        "Crucially, it contains ZERO quantitative metrics (no error reduction %, no F1-score, no traceability guarantee). Claims like 'works well' and 'nicely' are subjective and rejected by peer reviewers."
    ))
    story.append(Spacer(1, 10))

    # Flawed Introduction
    story.append(Paragraph("1. Introduction", h1_style))
    story.append(Paragraph(
        "Air pollution is a major problem worldwide and in Taiwan. WHO has strict guidelines for PM2.5. Taiwan has many low-cost sensors deployed under Civil IoT. "
        "However, people usually just look at the AQI color on apps. If it is yellow or red, they don't know if the pollution is from nearby or from far away. "
        "If you want to exercise outside, you don't know if you should cancel or just go to another park.",
        body_style
    ))
    story.append(Paragraph(
        "There are some problems with sensors. Low cost sensors are cheap so they have errors, especially when it is humid. Also LLMs can hallucinate numbers. "
        "Therefore, we propose AirSleuth, an agent that connects to sensor data and answers questions. We have four contributions: 1. an architecture with LLM and tools; "
        "2. an attribution method; 3. real data experiments; 4. open source code.",
        body_style
    ))
    story.append(make_flaw_callout(
        "Superficial Introduction Missing Technical Bottlenecks & MCP Formulation",
        "1. Missing rigorous epidemiological baseline: No mention of the 7.9M global mortality burden or the paradoxical 31% public behavioral compliance barrier.<br/>"
        "2. Fails to formulate the three core technical bottlenecks: sensor hygroscopic swelling non-linearity, spatial attribution ambiguity across scales, and LLM hallucination in numeric domains.<br/>"
        "3. Lacks the Model Context Protocol (MCP) and deterministic tool-grounded execution boundary."
    ))
    story.append(Spacer(1, 10))

    # Flawed Related Work
    story.append(Paragraph("2. Related Work", h1_style))
    story.append(Paragraph(
        "ReAct was proposed by Yao et al. for LLM reasoning and acting. Neuro-Air used multi-agents for air quality analysis. "
        "Other papers also used MCP or generated code. But they only serve analysts and trust clean data.",
        body_style
    ))
    story.append(Paragraph(
        "PurpleAir sensors in the US overestimate PM2.5 by 40% and humidity is important. In Taiwan, AirBox sensors need spatial corrections. "
        "Methods to separate local sources include spatial networks and filters. Exercise is good, but pollution is bad when PM2.5 is high.",
        body_style
    ))
    story.append(make_flaw_callout(
        "Severe 'Laundry List' Paper Dumping with No Comparative Synthesis",
        "1. <b>Zero Taxonomy:</b> Studies are randomly listed without grouping into functional paradigms or methodologies.<br/>"
        "2. <b>No Comparative Analysis:</b> Does not explain WHY Neuro-Air fails on noisy citizen IoT meshes (assumes sparse reference stations; lacks uncertainty calibration).<br/>"
        "3. <b>Disconnection from Innovation:</b> Does not derive the research gap that AirSleuth fills.<br/>"
        "4. <b>Missing Summary Table:</b> Readers cannot compare state-of-the-art approaches across key dimensions at a glance."
    ))
    story.append(Spacer(1, 10))

    # Flawed System Design
    story.append(Paragraph("3. System Design & Experiments", h1_style))
    story.append(Paragraph(
        "We built 8 modules. LLM does planning, and Python functions do math. We use a formula to check local excess and coherence. "
        "We tested forecasting with regression and tested 40 questions. Our method achieves high accuracy and the agent answers without making up numbers.",
        body_style
    ))
    story.append(make_flaw_callout(
        "Vague Methodology Lacking Algorithmic Thresholds & Traceability Mechanics",
        "Fails to specify mathematical formulations: local radius (2/8/15 km), absolute rise guards (+5 ug/m3), number-traceability regex verification, "
        "and empirical failure modes (e.g., station lag, clean-air noise amplification)."
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated bad PDF: {filename} ({os.path.getsize(filename)} bytes)")

def build_good_pdf(filename="paper_draft_refactored_good.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    styles = getSampleStyleSheet()

    # Refactored IEEE-like styles
    title_style = ParagraphStyle(
        'GoodTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        alignment=1,
        textColor=colors.HexColor('#002B49')
    )
    author_style = ParagraphStyle(
        'GoodAuthor',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=colors.HexColor('#333333')
    )
    affil_style = ParagraphStyle(
        'GoodAffil',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11,
        alignment=1,
        textColor=colors.HexColor('#555555')
    )
    abstract_heading = ParagraphStyle(
        'AbsHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        alignment=1,
        textColor=colors.HexColor('#111111')
    )
    abstract_body = ParagraphStyle(
        'AbsBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        alignment=4,
        textColor=colors.HexColor('#111111')
    )
    h1_style = ParagraphStyle(
        'GoodH1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#002B49'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'GoodH2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#111111'),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'GoodBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        alignment=4,
        textColor=colors.HexColor('#222222'),
        spaceAfter=5
    )
    bullet_style = ParagraphStyle(
        'GoodBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        leftIndent=12,
        spaceAfter=3
    )
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9
    )
    table_head = ParagraphStyle(
        'TableHead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9,
        textColor=colors.white
    )

    story = []

    # Title & Authors
    story.append(Paragraph("AirSleuth: A Tool-Grounded Domain AI Agent for Explainable PM<sub>2.5</sub> Source Attribution and Personalized Activity Decision Support from Public IoT Sensor Networks", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Yen-Kai Chen<sup>1,*</sup>, Hong-Yu Chen<sup>1</sup>, Ting-Chang Wang<sup>1</sup>, Chia-Feng Li<sup>1</sup>, Sheng-Ru Chou<sup>1</sup>", author_style))
    story.append(Paragraph("<sup>1</sup>Department of Computer Science and Information Engineering / IoT Smart City Research Lab, Taiwan<br/><sup>*</sup>Corresponding author: air.sleuth.project@gmail.com | Repository: https://github.com/A0966411725-png/AirSleuth", affil_style))
    story.append(Spacer(1, 8))

    # Structured Abstract (A to F)
    abs_text = (
        "<b>(A) Attention Getter / Area:</b> Ambient fine particulate matter (PM<sub>2.5</sub>) caused an estimated 7.9 million deaths globally in 2023. While Taiwan deployed over 10,200 public IoT micro-sensors, existing services report only broad color-coded AQI tiers, creating an information paradox where dense measurements fail to yield actionable guidance.<br/>"
        "<b>(B) Bottleneck / Problem:</b> Citizens need answers to three critical questions: <i>Why</i> is PM<sub>2.5</sub> elevated (local plume vs. regional episode)? <i>How</i> should individuals adapt? And <i>is</i> the reading credible? Dense low-cost sensors exhibit severe hygroscopic swelling (>40% bias at RH>70%), and standalone LLMs notoriously hallucinate environmental metrics.<br/>"
        "<b>(C) Cure / Core Solution:</b> We propose <b>AirSleuth</b>, a tool-grounded domain AI agent combining generative language reasoning with deterministic execution. The LLM is strictly confined to user intention comprehension, task orchestration, and empathetic explanation, while all computations (quality control, localized calibration, multi-scale spatial attribution, and action optimization) are executed by deterministic tools.<br/>"
        "<b>(D) Development / Methodology:</b> AirSleuth incorporates: (i) an automated 5-flag QC pipeline; (ii) city-specific dynamic humidity calibration anchored to reference stations; (iii) a multi-scale spatial decomposition algorithm analyzing local excess (<i>E</i>) and neighborhood coherence (<i>C</i>) across 2, 8, and 15 km radiuses; (iv) explainable MLR trend forecasting; and (v) an automated number-traceability guardrail that rejects responses containing unverified figures.<br/>"
        "<b>(E) Experiments / Evaluation:</b> Evaluated on 15.5 million 5-min records from 2,560 sensors, 18 reference stations, and 124 weather stations in Taichung and Kaohsiung, 880 semi-synthetic injection scenarios, and a 40-question benchmark, AirSleuth achieves 84.0% attribution accuracy (macro-F1 0.80) and rejects 99.0% of single-sensor faults.<br/>"
        "<b>(F) Findings / Impact:</b> AirSleuth achieves 100% numeric traceability (0.00 hallucination rate) and 96.0% action alignment (vs. 25% for standalone LLMs). All specifications and workflows are structured via OpenSpec for full reproducibility."
    )
    
    abs_table = Table([[
        Paragraph("<b>ABSTRACT</b>", abstract_heading),
    ], [
        Paragraph(abs_text, abstract_body)
    ]], colWidths=[532])
    abs_table.setStyle(TableStyle([
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#002B49')),
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#EBF3F9')),
        ('BACKGROUND', (0,1), (-1,1), colors.HexColor('#FAFCFD')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(abs_table)
    story.append(Spacer(1, 8))

    # Keywords
    story.append(Paragraph("<b>Keywords:</b> Air Quality, PM2.5, Low-Cost IoT Sensors, LLM Agent, Tool Use, Model Context Protocol, Spatial Attribution, Spec-Driven Development.", ParagraphStyle('KW', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7.5, leading=10)))
    story.append(Spacer(1, 8))

    # Section 1: Refactored Introduction
    story.append(Paragraph("1. Introduction", h1_style))
    story.append(Paragraph(
        "Ambient fine particulate matter (PM<sub>2.5</sub>) represents the paramount environmental threat to global health, causing an estimated 7.9 million premature deaths worldwide in 2023 [S-060]. Due to conclusive epidemiological findings proving that cardiovascular and pulmonary damage persists at low concentrations with no identifiable threshold [S-020, S-021], Taiwan revised its air quality standards in 2024 to 12 ug/m3 (annual) and 30 ug/m3 (daily) alongside a tightened Air Quality Index (AQI) [S-016]. However, public risk communication remains trapped in an information paradox: standard dashboards condense intricate atmospheric dynamics into static color badges and coarse demographic warnings [S-032]. Consequently, a systematic review revealed that a median of only 31% of citizens modify outdoor routines in response to warnings, largely due to confusing index metrics and lack of personalized action alternatives [S-028].",
        body_style
    ))
    story.append(Paragraph(
        "Taiwan's dense public Internet of Things (IoT) network—comprising over 10,200 micro-sensors streaming 5-minute data via open SensorThings APIs [S-001, S-013]—offers the spatial resolution needed to resolve this paradox. Unlike sparse government reference stations (spaced 10–20 km apart), dense sensor arrays reveal whether a PM<sub>2.5</sub> spike is a hyper-local event (within 2 km) or a 15 km regional stagnant episode. This distinction fundamentally changes actionable behavior: in local events, relocating a few kilometers eliminates exposure; in regional episodes, moving across town is useless, requiring schedule postponement or indoor air filtration.",
        body_style
    ))
    story.append(Paragraph(
        "Three fundamental bottlenecks currently obstruct the utilization of public IoT streams: (1) <i>Sensor Bias and Hygroscopic Distortion:</i> low-cost sensors systematically overestimate mass by ~40% due to humidity swelling (RH>70%), and calibration formulas fail when transferred across climatic regions [S-008, S-058]; (2) <i>Spatial Attribution Ambiguity:</i> disentangling local plumes from regional background remains difficult, and naive nearest-sensor heuristics trigger rampant false alarms on hardware glitches [S-057]; and (3) <i>LLM Hallucination and Traceability Void:</i> while generative language models excel at dialogue, unconstrained LLMs fabricate environmental numbers and fail to execute physical spatial logic [S-035, S-055].",
        body_style
    ))
    story.append(Paragraph(
        "We propose <b>AirSleuth</b>, a tool-grounded domain AI agent combining generative language reasoning with deterministic execution. By strictly confining the LLM to user intention comprehension and dialogue explanation, all computations are delegated to deterministic, logged tools. Our primary contributions include: (i) an MCP-inspired agent architecture with automated number-traceability regex guardrails; (ii) a multi-scale spatial decomposition algorithm (2/8/15 km) distinguishing local, subregional, regional, and faulty sensors; (iii) validation across 15.5M records in Taichung and Kaohsiung, 880 semi-synthetic injection scenarios, and a 40-scenario agent benchmark; and (iv) an open-source implementation governed by OpenSpec spec-driven development.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Section 2: Refactored Related Work
    story.append(Paragraph("2. Related Work and Comparative Synthesis", h1_style))
    story.append(Paragraph(
        "<b>2.1 LLM Agents and Tool-Grounded Execution:</b> ReAct pioneered interleaving reasoning traces with tool execution [S-035]. In environmental analytics, systems like Neuro-Air [S-053] orchestrate multi-agent pipelines over certified reference stations (88.4% accuracy), while other systems automate analysis scripts [S-037] or wrap APIs via the Model Context Protocol [S-036]. However, a survey of 45 data science agents revealed that >90% lack explicit trust or verification guardrails [S-055]. Critically, existing systems assume pristine reference data; when exposed to thousands of noisy, uncalibrated consumer IoT nodes, standard agents unreservedly accept corrupted readings and hallucinate plausible yet fabricated exposure figures [S-035]. AirSleuth resolves this by enforcing a deterministic perimeter where every reported figure is validated against execution logs.",
        body_style
    ))
    story.append(Paragraph(
        "<b>2.2 Low-Cost Sensors & Hygroscopic Distortions:</b> Optical particle counters suffer from particle hygroscopic swelling, leading to 40%–50% overestimation at high humidity [S-008, S-009]. While machine learning calibrations exist [S-011, S-041], models fail when generalized across distinct regions; Taiwan AirBox evaluations confirmed that a single nationwide equation is unviable, necessitating spatially varying coefficients [S-058]. Prior works treat calibration as an offline task; AirSleuth dynamically embeds localized calibration within the live agent reasoning loop.",
        body_style
    ))
    story.append(Paragraph(
        "<b>2.3 Spatial Source Attribution:</b> Background normalization, spatial moving medians, and spectral filtering separate local emissions from regional background [S-045, S-047], yet comparative benchmarks show no single method dominates across topographies [S-057]. Crucially, nearest-sensor heuristics collapse when individual sensors glitch. AirSleuth resolves this via multi-scale median pooling (2/8/15 km) and neighborhood coherence metrics.",
        body_style
    ))
    story.append(Paragraph(
        "<b>2.4 Exposure Assessment & Health Decision Trade-offs:</b> Ambient concentration does not equal inhaled dose [S-034]. NHAPS proved urban residents spend >87% of time indoors. While physical activity is protective, high pollution degrades mortality benefits from ~30% down to 12%–15% at PM<sub>2.5</sub> >= 25 ug/m3 [S-061]. AirSleuth reformulates binary 'stay home' warnings into personalized multi-attribute action ranking (time shift, route change, indoor filtration).",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Table 1: Comparative Matrix
    t1_data = [
        [Paragraph("<b>Evaluation Dimension</b>", table_head), Paragraph("<b>Traditional AQI Portals</b>", table_head), Paragraph("<b>Standalone LLMs</b>", table_head), Paragraph("<b>Expert Agents (e.g. Neuro-Air)</b>", table_head), Paragraph("<b>AirSleuth (This Work)</b>", table_head)],
        [Paragraph("Target Audience", table_cell), Paragraph("General public (passive)", table_cell), Paragraph("General dialogue users", table_cell), Paragraph("Environmental scientists", table_cell), Paragraph("Citizens, sensitive groups", table_cell)],
        [Paragraph("Data Input", table_cell), Paragraph("Sparse reference stations", table_cell), Paragraph("Pre-training corpora", table_cell), Paragraph("Certified station records", table_cell), Paragraph("10,000+ IoT nodes + Stations", table_cell)],
        [Paragraph("QC & Calibration", table_cell), Paragraph("Manual EPA screening", table_cell), Paragraph("None (data unaware)", table_cell), Paragraph("Assumes clean data", table_cell), Paragraph("5-flag QC + dynamic RH anchor", table_cell)],
        [Paragraph("Spatial Attribution", table_cell), Paragraph("Coarse zone color", table_cell), Paragraph("Qualitative guessing", table_cell), Paragraph("Python script generation", table_cell), Paragraph("Multi-scale (2/8/15 km) coherence", table_cell)],
        [Paragraph("Numeric Traceability", table_cell), Paragraph("Static webpage table", table_cell), Paragraph("Fails (hallucinates values)", table_cell), Paragraph("Unconstrained execution", table_cell), Paragraph("Strict regex guardrail & replay log", table_cell)],
        [Paragraph("Action Guidance", table_cell), Paragraph("Coarse group warnings", table_cell), Paragraph("Generic health advice", table_cell), Paragraph("None (reporting only)", table_cell), Paragraph("Personalized tradeoff ranking", table_cell)],
    ]
    t1 = Table(t1_data, colWidths=[80, 105, 110, 115, 122])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#002B49')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#B0BEC5')),
        ('PADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F5F7F8')]),
    ]))
    story.append(t1)
    story.append(Spacer(1, 6))

    # Section 3: Architecture & Algorithms
    story.append(Paragraph("3. System Architecture and Algorithms", h1_style))
    story.append(Paragraph(
        "AirSleuth divides operations across 8 modules (Figure 1 in Overleaf). Module 3 (Planner) uses function calling over 8 deterministic tools. Module 4 ingests SensorThings API data and flags rows: <i>Extreme</i> (>500 ug/m3), <i>Stuck</i> (identical values over 1 hour), and <i>RH_Invalid</i> (outside 0-100%). In Taichung, 28% of sensor transmissions report RH=0%; AirSleuth anchors calibration to the nearest weather station instead.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Multi-Scale Spatial Attribution (Algorithm 2):</b> Concentric radiuses of 2 km (local L), 8 km (subregional), and 15 km (regional background B) are defined. Local excess is E = L - B. A sensor is <i>rising</i> if s(t) > 1.5 * Med_6h(s) AND s(t) - Med_6h(s) >= 5 ug/m3. Neighborhood coherence ratios C (15 km), C_sub (8 km), and C_ring (8-15 km) classify events: Regional (C>=0.6, E < max(5, 0.3*B)), Subregional (C<0.6, C_sub>=0.3, C_ring<0.3), Local (E >= max(10, 0.5*B), C<0.3, nearby rising >= 2), or Suspected Fault (E>=10, nearby rising < 2).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Number Traceability Guardrail:</b> Post-generation regex scans for numbers with physical units (ug/m3, %, km). Any value differing by >0.5 from logged tool outputs triggers immediate rewriting or deterministic fallback.",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Section 4: Experimental Results
    story.append(Paragraph("4. Experimental Results and Discussion", h1_style))
    story.append(Paragraph(
        "Evaluated on 15.5 million records from Taichung and Kaohsiung (October–November 2026), AirSleuth's findings include:<br/>"
        "• <b>Calibration & Forecasting:</b> MLR achieves 6-hour MAE of 4.97 ug/m3 (vs. 5.69 for persistence). Weather-anchored RH correction reduces Taichung calibration MAE from 4.07 to 3.24 ug/m3.<br/>"
        "• <b>Spatial Attribution (880 injections):</b> AirSleuth attains 84.0% accuracy (macro-F1 0.80). Nearest-sensor rules falsely flag 100% of single-sensor faults as local pollution; AirSleuth limits false alarms to 1.0%. Ablating the 8 km tier drops subregional recall to 0.00.<br/>"
        "• <b>40-Scenario Agent Benchmark:</b> AirSleuth achieves 100% number traceability (0.00 hallucination) and 96.0% action agreement with public health guidelines (vs. 25% for standalone LLM).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Real-World Edge Cases Resolved:</b> Historical replays uncovered 3 failure modes: (1) Reference station reversion lag causing negative forecasts (resolved via +-50% delta clamp); (2) Clean-air noise triggering false alerts (resolved via +5 ug/m3 absolute threshold); (3) Exercise over-penalization at 26 ug/m3 (resolved by activating exercise discounts only above 30.5 ug/m3).",
        body_style
    ))
    story.append(Spacer(1, 6))

    # Section 5: Conclusion & OpenSpec
    story.append(Paragraph("5. Conclusion and Spec-Driven Development", h1_style))
    story.append(Paragraph(
        "AirSleuth demonstrates that tool-grounded domain agents can transform noisy public IoT streams into explainable, traceable, and actionable health decisions. Structured under OpenSpec (spec-driven development), all architecture components, delta specifications, and test suites are maintained alongside the codebase. Source code, test datasets, and interactive demos are available at https://github.com/A0966411725-png/AirSleuth.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated good PDF: {filename} ({os.path.getsize(filename)} bytes)")

if __name__ == '__main__':
    build_bad_pdf()
    build_good_pdf()

