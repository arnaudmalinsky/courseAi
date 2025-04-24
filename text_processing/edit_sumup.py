import pandas as pd
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

# Load Excel data
# excel_path = "C:/Users/bossa/Documents/courseai_data/april/excel_w_llm/llm_result_CMP_lecon1_1745144284.06419.xlsx"  # replace with your actual file
# df = pd.read_excel(excel_path)

# Load Excel data
text_excel_path = "C:/Users/bossa/Documents/courseai_data/april/excel_w_llm/sumup_CMP_lecon1_1745452201.615262.xlsx"  # replace with your actual file
texts_df = pd.read_excel(text_excel_path)

law_reference_excel_path = "C:/Users/bossa/Documents/courseai_data/april/excel_w_llm/llm_result_CMP_lecon1_1745144284.06419.xlsx"  # replace with your actual file
law_ref_df = pd.read_excel(law_reference_excel_path)

merged_df = law_ref_df.merge(
    texts_df[["unique_index","Filename","Index","text_sumup"]],
    on=["unique_index","Filename", "Index"], 
    how='left'
    )

# Filter out rows where flag_law is not True
# merged_df = merged_df[merged_df['flag_law'] == True]

# Fill NaNs to avoid groupby issues
merged_df.fillna('', inplace=True)

# Create Word document
doc = Document()
doc.add_heading("CMP course sumup", level=0)

# Sort to ensure correct agenda order
merged_df.sort_values(by=['Title Context', 'Title lvl2', 'Title lvl3'], inplace=True)

# Track previous levels to avoid repetition
prev_lvl1 = ""
prev_lvl2 = ""

# Group by agenda levels
grouped = merged_df.groupby(['Title Context', 'Title lvl2', 'Title lvl3'])
for (lvl1, lvl2, lvl3), group in grouped:
    if lvl1 != prev_lvl1:
        doc.add_heading(str(lvl1), level=1)
        prev_lvl1 = lvl1
        prev_lvl2 = "" 
    if lvl2 != prev_lvl2:
        doc.add_heading(str(lvl2), level=2)
        prev_lvl2 = lvl2

    doc.add_heading(str(lvl3), level=3)
    # first_sumup = (
    #     texts_df[
    #         (texts_df['Title Context']==lvl1)
    #         & (texts_df['Title lvl2']==lvl2)
    #         & (texts_df[ 'Title lvl3']==lvl3)
    #     ].iloc[0]
    # )
    first_sumup = group.iloc[0]['text_sumup']
    print(first_sumup)
    doc.add_paragraph(first_sumup)
    for _, row in group.iterrows():
        if row["flag_law"]==True:
            law_text = f"• {row['label']}"# ({row['law_type']}, {row['institution']}, {row['corpus']}, {row['location']}, {row['date'] if pd.notna(row['date']) else 'No Date'})"
            para = doc.add_paragraph(law_text)
            para.style.font.size = Pt(10)

# Save the document
output_path = "law_references_agenda.docx"
doc.save(output_path)

print(f"Document saved to {output_path}")
