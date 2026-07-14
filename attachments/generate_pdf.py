#!/usr/bin/env python3
"""Generate spec.pdf from the spec content, with mockups inline."""
import os
import base64
import re

ATTACHMENTS_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.dirname(ATTACHMENTS_DIR)

from playwright.sync_api import sync_playwright

# Read the spec.md
with open(os.path.join(OUT_DIR, "spec.md"), "r") as f:
    spec_md = f.read()

# Convert markdown to HTML (simplified but sufficient for the PDF)
def md_to_html(md):
    lines = md.split('\n')
    html_lines = []
    in_table = False
    in_code = False
    in_list = False
    in_num_list = False
    i = 0
    while i < len(lines):
        line = lines[i]
        # Code blocks
        if line.strip().startswith('```'):
            if in_code:
                html_lines.append('</code></pre>')
                in_code = False
            else:
                lang = line.strip().strip('`').strip()
                html_lines.append(f'<pre><code>')
                in_code = True
            i += 1
            continue
        if in_code:
            html_lines.append(line.replace('<', '&lt;').replace('>', '&gt;'))
            i += 1
            continue
        # Tables
        if '|' in line and line.strip().startswith('|'):
            if not in_table:
                html_lines.append('<table>')
                in_table = True
                # header row
                cells = [c.strip() for c in line.split('|')[1:-1]]
                header = '<tr>' + ''.join(f'<th>{c}</th>' for c in cells) + '</tr>'
                html_lines.append(header)
                i += 1
                # skip separator
                if i < len(lines) and '---' in lines[i]:
                    i += 1
                continue
            else:
                if line.strip().startswith('|---'):
                    i += 1
                    continue
                cells = [c.strip() for c in line.split('|')[1:-1]]
                row = '<tr>' + ''.join(f'<td>{c}</td>' for c in cells) + '</tr>'
                html_lines.append(row)
                i += 1
                continue
        else:
            if in_table:
                html_lines.append('</table>')
                in_table = False
        
        # Headings
        if line.startswith('# ') and not line.startswith('## '):
            html_lines.append(f'<h1 class="main-title">{line[2:]}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h1 class="section-title">{line[3:]}</h1>')
        elif line.startswith('### '):
            html_lines.append(f'<h2>{line[4:]}</h2>')
        elif line.startswith('#### '):
            html_lines.append(f'<h3>{line[5:]}</h3>')
        elif line.strip().startswith('- [ ]'):
            content = line.strip()[5:]
            html_lines.append(f'<div class="checkbox">☐ {content}</div>')
        elif line.strip().startswith('- '):
            content = line.strip()[2:]
            if not in_list:
                html_lines.append('<ul>')
                in_list = True
            html_lines.append(f'<li>{content}</li>')
        elif re.match(r'^\d+\\. ', line.strip()):
            content = re.sub(r'^\d+\. ', '', line.strip())
            if not in_num_list:
                html_lines.append('<ol>')
                in_num_list = True
            html_lines.append(f'<li>{content}</li>')
        elif line.strip() == '':
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_num_list:
                html_lines.append('</ol>')
                in_num_list = False
            html_lines.append('<br>')
        else:
            if in_list:
                html_lines.append('</ul>')
                in_list = False
            if in_num_list:
                html_lines.append('</ol>')
                in_num_list = False
            # Inline formatting
            content = line
            # Bold
            content = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', content)
            # Inline code
            content = re.sub(r'`(.+?)`', r'<code class="inline-code">\1</code>', content)
            # Images
            content = re.sub(r'!\[(.+?)\]\((.+?)\)', 
                lambda m: embed_image(m.group(1), m.group(2)), content)
            # Links
            content = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', content)
            html_lines.append(f'<p>{content}</p>')
        i += 1
    
    if in_list:
        html_lines.append('</ul>')
    if in_num_list:
        html_lines.append('</ol>')
    if in_table:
        html_lines.append('</table>')
    if in_code:
        html_lines.append('</code></pre>')
    
    return '\n'.join(html_lines)

def embed_image(caption, src):
    """Convert image reference to base64 inline image."""
    img_path = os.path.join(OUT_DIR, src)
    if os.path.exists(img_path):
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return (f'<div class="mockup-frame"><img src="data:image/png;base64,{b64}" />'
                f'<div class="mockup-caption">{caption}</div></div>')
    return f'<div class="mockup-frame"><div class="mockup-caption">{caption} (image not found: {src})</div></div>'

spec_html = md_to_html(spec_md)

full_html = f"""<!DOCTYPE html>
<html><head>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Inter', system-ui, sans-serif; font-size: 13px; color: #1a1a2e; line-height: 1.6; }}
  .cover {{
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    color: #fff; height: 297mm; display: flex; flex-direction: column;
    justify-content: center; align-items: flex-start; padding: 60px 64px;
    page-break-after: always;
  }}
  .cover .cover-label {{
    font-size: 12px; font-weight: 700; text-transform: uppercase;
    letter-spacing: 2px; color: #7c3aed; margin-bottom: 24px;
  }}
  .cover h1 {{ font-size: 42px; font-weight: 700; line-height: 1.2; margin-bottom: 16px; }}
  .cover h1 span {{ color: #818cf8; }}
  .cover .cover-sub {{ font-size: 16px; color: #94a3b8; max-width: 500px; line-height: 1.6; margin-bottom: 40px; }}
  .cover .cover-meta {{ font-size: 14px; color: #64748b; }}
  .cover .cover-meta div {{ margin-bottom: 6px; }}
  .page {{ padding: 28px 40px; }}
  .page-break {{ page-break-before: always; }}
  h1.main-title {{ font-size: 26px; font-weight: 700; color: #1e1b4b; margin: 0 0 20px; padding-bottom: 10px; border-bottom: 3px solid #7c3aed; }}
  h1.section-title {{ font-size: 22px; font-weight: 700; color: #1e1b4b; border-bottom: 3px solid #7c3aed; padding-bottom: 10px; margin: 36px 0 20px; }}
  h2 {{ font-size: 16px; font-weight: 600; color: #312e81; margin: 28px 0 12px; border-left: 4px solid #7c3aed; padding-left: 12px; }}
  h3 {{ font-size: 14px; font-weight: 600; color: #312e81; margin: 20px 0 10px; }}
  pre {{ background: #1e1b4b; color: #c7d2fe; font-family: 'JetBrains Mono', monospace; font-size: 10px; padding: 16px 18px; border-radius: 8px; margin: 12px 0; line-height: 1.55; overflow-x: auto; white-space: pre-wrap; }}
  pre code {{ font-family: inherit; font-size: inherit; }}
  table {{ width: 100%; border-collapse: collapse; margin: 14px 0; font-size: 11px; }}
  th {{ background: #312e81; color: #e0e7ff; font-weight: 600; padding: 8px 12px; text-align: left; font-size: 11px; }}
  td {{ padding: 8px 12px; border-bottom: 1px solid #e5e7eb; vertical-align: top; }}
  tr:nth-child(even) td {{ background: #f5f3ff; }}
  .inline-code {{ background: #f0edff; color: #7c3aed; padding: 1px 5px; border-radius: 4px; font-family: 'JetBrains Mono', monospace; font-size: 11px; }}
  .checkbox {{ font-size: 12px; line-height: 1.8; color: #374151; }}
  ul, ol {{ margin: 8px 0 8px 0; padding-left: 28px; }}
  li {{ font-size: 12px; color: #374151; line-height: 1.7; margin-bottom: 4px; }}
  p {{ font-size: 12.5px; color: #374151; line-height: 1.65; margin-bottom: 8px; }}
  strong {{ font-weight: 600; color: #1e1b4b; }}
  .badge-ok {{ background: #dcfce7; color: #15803d; font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 12px; }}
  .badge-warn {{ background: #fef9c3; color: #92400e; font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 12px; }}
  .badge-fail {{ background: #fee2e2; color: #991b1b; font-size: 10px; font-weight: 600; padding: 2px 8px; border-radius: 12px; }}
  .mockup-frame {{ border: 1px solid #e5e7eb; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin: 16px 0; }}
  .mockup-frame img {{ width: 100%; display: block; }}
  .mockup-caption {{ font-size: 10px; font-weight: 600; color: #6b7280; text-align: center; padding: 8px; background: #f9fafb; border-top: 1px solid #e5e7eb; text-transform: uppercase; letter-spacing: 0.5px; }}
  a {{ color: #7c3aed; text-decoration: none; }}
</style>
</head><body>

<div class="cover">
  <div class="cover-label">Technical & Functional Specification</div>
  <h1>JackHamr<br><span>Documentation Website</span></h1>
  <div class="cover-sub">Single-page scroll website documenting the JackHamr AI agent orchestration platform — technical documentation for developers and users.</div>
  <div class="cover-meta">
    <div><strong>Date:</strong> 2026-07-13</div>
    <div><strong>Version:</strong> 1.0</div>
    <div><strong>Status:</strong> In design — ready for implementation</div>
    <div><strong>Stack:</strong> Vanilla HTML + Tailwind CSS + minimal vanilla JS</div>
  </div>
</div>

<div class="page">
{spec_html}
</div>

</body></html>"""

pdf_html_path = os.path.join(ATTACHMENTS_DIR, "spec_pdf.html")
with open(pdf_html_path, "w") as f:
    f.write(full_html)

pdf_path = os.path.join(OUT_DIR, "spec.pdf")

with sync_playwright() as p:
    browser = p.chromium.launch(
        executable_path="/usr/local/bin/chromium",
        args=["--no-sandbox", "--disable-setuid-sandbox"],
    )
    page = browser.new_page()
    page.set_viewport_size({"width": 1200, "height": 1600})
    page.goto(f"file://{pdf_html_path}", wait_until="networkidle")
    page.wait_for_timeout(2000)
    page.pdf(
        path=pdf_path,
        format="A4",
        margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"},
        print_background=True,
    )
    browser.close()

print(f"✓ spec.pdf generated at {pdf_path}")
print(f"  Size: {os.path.getsize(pdf_path) / 1024:.0f} KB")
