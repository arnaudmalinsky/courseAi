import pandas as pd
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

# Load Excel data
excel_path = "C:/Users/bossa/Documents/courseai_data/april/excel_w_llm/llm_result_CMP_lecon1_1745144284.06419.xlsx"  # replace with your actual file
df = pd.read_excel(excel_path)

# Create a new Word document
doc = Document()
doc.add_heading("Law References Agenda", level=0)

# Group by agenda structure
grouped = df.groupby(['Title Context', 'Title lvl2', 'Title lvl3'])
for (lvl1, lvl2, lvl3), group in grouped:
    # Only write Title lvl1 if changed
    if lvl1 != prev_lvl1:
        doc.add_heading(str(lvl1), level=1)
        prev_lvl1 = lvl1
        prev_lvl2 = ""  # reset lvl2 when lvl1 changes
    
    # Only write Title lvl2 if changed
    if lvl2 != prev_lvl2:
        doc.add_heading(str(lvl2), level=2)
        prev_lvl2 = lvl2

    # Always write Title lvl3
    doc.add_heading(str(lvl3), level=3)
    
    for _, row in group.iterrows():
        law_text = f"• {row['label']} ({row['law_type']}, {row['institution']}, {row['corpus']}, {row['location']}, {row['date'] if pd.notna(row['date']) else 'No Date'})"
        #strftime('%Y-%m-%d')
        para = doc.add_paragraph(law_text)
        para.style.font.size = Pt(10)

# Save the document
output_path = "law_references_agenda.docx"
doc.save(output_path)

print(f"Document saved to {output_path}")
