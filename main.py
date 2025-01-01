import typer
from text_processing.parsers import CorpusParser
from prompting.batch_llm_call import batch_call 


app = typer.Typer()

@app.command()
def process_documents(
        input_files_folder_path: str,
        output_excel_file_path:str
    ):
    CorpusParser(
        input_files_folder_path,
        output_excel_file_path
    ).parse_all_documents()

@app.command()
def batch_llm_call(
        open_ai_key: str,
        input_excel_file_path:str,
        output_excel_file_path: str,
        batch_size:int  ,
        limit:int         
    ):
    batch_call(
        open_ai_key,
        input_excel_file_path,
        output_excel_file_path,
        batch_size ,
        limit 
    )


if __name__ == "__main__":
    app()