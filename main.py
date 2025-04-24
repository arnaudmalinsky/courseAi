import logging

import typer

from text_processing.parsers import CorpusParser
from prompting.batch_llm_call import batch_call 


app = typer.Typer()

@app.command()
def process_documents(
        input_files_folder_path : str,
        output_excel_file_path : str,
        max_length: int = 5000,
        overlap: int = 0,
        verbose: bool = True 
    ):
    lvl = logging.WARNING
    fmt = "%(message)s"
    if verbose is True:
        lvl = logging.DEBUG
    logging.basicConfig(level=lvl, format=fmt)
    
    CorpusParser(
        input_files_folder_path,
        output_excel_file_path,
        max_length,
        overlap
    ).parse_all_documents()

@app.command()
def batch_llm_call(
        open_ai_key: str,
        input_excel_file_path:str,
        output_excel_file_path: str=None,
        flag_law_ref:bool=True,
        batch_size:int=200,
        limit:int=None,
        verbose: bool = True 
    ):
    lvl = logging.WARNING
    fmt = "%(message)s"
    if verbose is True:
        lvl = logging.DEBUG
    logging.basicConfig(level=lvl, format=fmt)
    batch_call(
        open_ai_key,
        input_excel_file_path,
        output_excel_file_path, 
        flag_law_ref,
        batch_size ,
        limit 
    )


if __name__ == "__main__":
    app()