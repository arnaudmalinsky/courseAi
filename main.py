import typer
from text_processing.parsers import CorpusParser 

def process_documents(
        input_files_folder_path: str,
        output_excel_file_path:str
    ):
    CorpusParser(
        input_files_folder_path,
        output_excel_file_path
    ).parse_all_documents()


if __name__ == "__main__":
    typer.run(process_documents)