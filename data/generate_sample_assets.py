"""
Generates sample multimodal test waybills (PNG and PDF).
Creates:
1. data/sample_waybill_clean.png
2. data/sample_waybill_damaged_hazmat.png
3. data/sample_waybill.pdf
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

DATA_DIR = Path(__file__).parent

def create_clean_waybill():
    img = Image.new("RGB", (800, 600), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Header border
    draw.rectangle([20, 20, 780, 580], outline=(0, 0, 0), width=3)
    draw.rectangle([20, 20, 780, 90], fill=(240, 244, 248), outline=(0, 0, 0), width=2)

    # Header Text
    draw.text((40, 35), "FREIGHT MASTER LOGISTICS - MULTIMODAL WAYBILL", fill=(0, 51, 102))
    draw.text((40, 60), "STANDARD MANIFEST & BILL OF LADING", fill=(100, 100, 100))

    # Waybill Details
    y = 120
    fields = [
        ("BILL OF LADING #:", "WB-99482-TX"),
        ("CONSIGNEE:", "Apex Industrial Distribution Corp"),
        ("ORIGIN FACILITY:", "Chicago Terminal Hub (ORD-1)"),
        ("DESTINATION FACILITY:", "Dallas Freight Gateway (DFW-4)"),
        ("SKU CODE:", "SKU-AUTO-1001"),
        ("DESCRIPTION:", "Electric Powertrain Inverter Modules (Palletized)"),
        ("CARGO WEIGHT:", "12.5 METRIC TONS"),
        ("HAZMAT STATUS:", "NONE - NON-HAZARDOUS"),
        ("PACKAGE CONDITION:", "SEALS INTACT - ZERO DAMAGE"),
        ("REQUIRED DOCK:", "STANDARD DRY TERMINAL BAY 4")
    ]

    for label, val in fields:
        draw.text((50, y), label, fill=(50, 50, 50))
        draw.text((260, y), val, fill=(0, 0, 0))
        draw.line([50, y + 25, 750, y + 25], fill=(220, 220, 220), width=1)
        y += 40

    # Barcode representation
    for i in range(50, 750, 8):
        width = 2 if (i % 3 == 0) else 4
        draw.line([i, 520, i, 560], fill=(0, 0, 0), width=width)

    target_path = DATA_DIR / "sample_waybill_clean.png"
    img.save(target_path)
    print(f"Created: {target_path}")

def create_damaged_hazmat_waybill():
    img = Image.new("RGB", (800, 600), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Header border with warning red accent
    draw.rectangle([20, 20, 780, 580], outline=(180, 0, 0), width=4)
    draw.rectangle([20, 20, 780, 90], fill=(255, 235, 235), outline=(180, 0, 0), width=2)

    # Header Text
    draw.text((40, 35), "EMERGENCY DISPATCH WAYBILL - DANGEROUS GOODS", fill=(180, 0, 0))
    draw.text((40, 60), "HAZMAT MANIFEST & DAMAGE INCIDENT REPORT", fill=(180, 0, 0))

    # Waybill Details
    y = 120
    fields = [
        ("BILL OF LADING #:", "WB-HAZ-5501-IL"),
        ("CONSIGNEE:", "ChemTech Specialty Logistics"),
        ("ORIGIN FACILITY:", "Joliet Chemical Works"),
        ("DESTINATION FACILITY:", "Houston Petrochemical Bay"),
        ("SKU CODE:", "SKU-CHEM-9012"),
        ("DESCRIPTION:", "Industrial Lithium Solvent (UN 1993)"),
        ("CARGO WEIGHT:", "8.0 METRIC TONS"),
        ("HAZMAT STATUS:", "CLASS-3-FLAMMABLE (UN 1993) - ISOLATION MANDATORY"),
        ("PACKAGE CONDITION:", "CRUSHED CORNER / PACKAGE DAMAGE DETECTED"),
        ("REQUIRED DOCK:", "HAZMAT ISOLATION BAY 7 (GROUNDING ACTIVE)")
    ]

    for label, val in fields:
        draw.text((50, y), label, fill=(100, 20, 20))
        draw.text((260, y), val, fill=(180, 0, 0) if "HAZMAT" in val or "DAMAGE" in val else (0, 0, 0))
        draw.line([50, y + 25, 750, y + 25], fill=(240, 200, 200), width=1)
        y += 40

    # Red Stamp
    draw.rectangle([500, 480, 750, 550], outline=(200, 0, 0), width=3)
    draw.text((520, 500), "DAMAGE AUDIT FLAGGED", fill=(200, 0, 0))
    draw.text((530, 525), "HAZMAT ISOLATION REQUIRED", fill=(200, 0, 0))

    target_path = DATA_DIR / "sample_waybill_damaged_hazmat.png"
    img.save(target_path)
    print(f"Created: {target_path}")

def create_pdf_waybill():
    target_path = DATA_DIR / "sample_waybill.pdf"
    c = canvas.Canvas(str(target_path), pagesize=letter)
    width, height = letter

    c.rect(30, 30, width - 60, height - 60)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 60, "GLOBAL LOGISTICS NETWORK - WAYBILL MANIFEST")
    c.setFont("Helvetica", 10)
    c.drawString(50, height - 80, "Document ID: WB-PDF-88421 | Turn-Around Latency Verified")

    c.line(50, height - 90, width - 50, height - 90)

    y = height - 130
    items = [
        ("Tracking Number (Bill ID):", "WB-99482-TX"),
        ("Consignee:", "Universal Parts Staging LLC"),
        ("Origin:", "Chicago, IL (ORD Hub)"),
        ("Destination:", "Dallas, TX (DFW Yard)"),
        ("SKU:", "SKU-AUTO-1001"),
        ("Hazardous Material:", "NONE"),
        ("Package Damage:", "NONE / INSPECTION PASSED"),
        ("Gross Weight:", "12.5 Tons"),
        ("Assigned Dock Recommendation:", "Dock-04-NorthTerminal")
    ]

    for label, val in items:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(60, y, label)
        c.setFont("Helvetica", 10)
        c.drawString(260, y, val)
        y -= 30

    c.line(50, y - 10, width - 50, y - 10)
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, y - 30, "Automated Dispatch Notice: Verified under ADK UltraFast sub-350ms pipeline.")

    c.save()
    print(f"Created: {target_path}")

if __name__ == "__main__":
    create_clean_waybill()
    create_damaged_hazmat_waybill()
    create_pdf_waybill()
