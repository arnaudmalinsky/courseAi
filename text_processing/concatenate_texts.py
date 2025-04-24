import pandas as pd

# Load Excel data
excel_path = "C:/Users/bossa/Documents/courseai_data/april/excel_w_llm/llm_result_CMP_lecon1_1745144284.06419.xlsx"  # replace with your actual file
df = pd.read_excel(excel_path)
# Fill NaNs to avoid groupby issues
df.fillna('', inplace=True)
# Sort for clean structure
df.sort_values(by=['Title Context', 'Title lvl2', 'Title lvl3'], inplace=True)

# Group by title triplet
concat_text_df = (
    df.groupby(
        ['Title Context', 'Title lvl2', 'Title lvl3'],
        as_index=True
    )
    .agg(
        {
            'Text': lambda x: ' '.join(x),
            'unique_index':'first',
            'Filename':'first',
            'Index':'first'
        }
    )
    .rename(columns={"Text":"concat_texts"})
)

output_excel_path = "C:/Users/bossa/Documents/courseai_data/april/excel_w_llm/llm_result_CMP_lecon1_text_concat.xlsx"  # replace with your actual file
concat_text_df.to_excel(output_excel_path)

