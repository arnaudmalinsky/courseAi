import pandas as pd
from pathlib import Path

def concatenate_text_from_excel(
    all_excel_file_path,
    course_name
):
    df = pd.read_excel(all_excel_file_path)
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
                'Folder':'first',
                'Filename':'first',
                'Index':'first'

            }
        )
        .rename(columns={"Text":"concat_texts"})
    )

    
    path = Path(all_excel_file_path)

    output_path = f"{course_name}_concat_text.xlsx"

    final_path = path.parent / output_path

    print(f"Excel saved to {final_path}")
    concat_text_df.to_excel(final_path)

