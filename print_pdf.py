from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent
html = ROOT / "counter-cyclical-rise.html"
pdf = ROOT / "counter-cyclical-rise.pdf"

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 1200, "height": 1600})
    page.goto(html.as_uri(), wait_until="load")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(800)
    page.pdf(path=str(pdf), format="A4", print_background=True,
             margin={"top": "18mm", "bottom": "20mm", "left": "17mm", "right": "17mm"})
    b.close()
print("wrote", pdf, pdf.stat().st_size)
