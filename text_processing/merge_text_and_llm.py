import pandas as pd

# Load Excel data
text_excel_path = "C:/Users/bossa/Documents/courseai_data/april/excel_w_llm/sumup_CMP_lecon1_1745452201.615262.xlsx"  # replace with your actual file
texts_df = pd.read_excel(text_excel_path)

law_reference_excel_path = "C:/Users/bossa/Documents/courseai_data/april/excel_w_llm/llm_result_CMP_lecon1_1745144284.06419.xlsx"  # replace with your actual file
law_ref_df = pd.read_excel(law_reference_excel_path)

# merged_df = law_ref_df.merge(
#     texts_df[["unique_index","Filename","Index","text_sumup"]],
#     on=["unique_index","Filename", "Index"], 
#     how='left'
#     )

merged_df = law_ref_df.merge(
    texts_df[['Title Context', 'Title lvl2', 'Title lvl3',"text_sumup"]],
    on=['Title Context', 'Title lvl2', 'Title lvl3'], 
    how='left'
    )

merged_path = "C:/Users/bossa/Documents/courseai_data/april/excel_w_llm/llm_result_CMP_lecon1_merged_output.xlsx"  # replace with your actual file
merged_df.to_excel(merged_path)