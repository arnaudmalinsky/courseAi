import logging
import os

import typer

from text_processing.parsers import CorpusParser
from prompting.batch_llm_call import batch_call 
from text_processing.edit_sumup import edit_sumup
from text_processing.concatenate_texts import concatenate_text_from_excel
from text_processing.pdf_to_docx import convert_pdf_to_docx
from text_processing.chapter_pipeline import (
    assemble_chapter_summaries,
    split_docx_by_chapter,
    summarize_chapter_manifest,
)
from text_processing.boxed_case_law_pipeline import extract_boxed_case_law_chapters


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

@app.command()
def edit_sumup_doc(
    sumup_excel_path:str,
    law_ref_excel_path:str,
    course_name:str,
    verbose: bool = True 
):
    lvl = logging.WARNING
    fmt = "%(message)s"
    if verbose is True:
        lvl = logging.DEBUG
    logging.basicConfig(level=lvl, format=fmt)
    edit_sumup(
        sumup_excel_path,
        law_ref_excel_path,
        course_name,
    )

@app.command()
def concatenate_excel_text(
    all_excel_file_path,
    course_name,
    verbose: bool = True 
):
    lvl = logging.WARNING
    fmt = "%(message)s"
    if verbose is True:
        lvl = logging.DEBUG
    logging.basicConfig(level=lvl, format=fmt)
    concatenate_text_from_excel(
        all_excel_file_path,
        course_name,
    )


@app.command()
def pdf_to_docx(
    input_pdf_path: str,
    output_docx_path: str = None,
    preserve_page_breaks: bool = False,
    max_heading_chars: int = 140,
    chapters_dir: str = None,
    manifest_path: str = None,
    verbose: bool = True,
):
    lvl = logging.WARNING
    fmt = "%(message)s"
    if verbose is True:
        lvl = logging.DEBUG
    logging.basicConfig(level=lvl, format=fmt)
    convert_pdf_to_docx(
        input_pdf_path,
        output_docx_path,
        preserve_page_breaks,
        max_heading_chars,
        chapters_dir,
        manifest_path,
    )


@app.command()
def split_chapters(
    source_docx_path: str,
    output_dir: str,
    manifest_path: str = None,
):
    split_docx_by_chapter(source_docx_path, output_dir, manifest_path)


@app.command()
def summarize_chapters(
    manifest_path: str,
    open_ai_key: str = None,
    model: str = None,
    concurrency: int = 4,
    retries: int = 3,
    retry_invalid: bool = False,
    env_path: str = ".env",
    chapter_id: list[str] = typer.Option(None, "--chapter-id"),
    order: list[int] = typer.Option(None, "--order"),
    from_order: int = typer.Option(None, "--from-order"),
    to_order: int = typer.Option(None, "--to-order"),
    force: bool = False,
    verbose: bool = True,
):
    logging.basicConfig(
        level=logging.INFO if verbose else logging.WARNING,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )
    summarize_chapter_manifest(
        manifest_path,
        open_ai_key or os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_KEY"),
        model,
        concurrency,
        retries,
        retry_invalid,
        env_path=env_path,
        chapter_ids=chapter_id,
        orders=order,
        from_order=from_order,
        to_order=to_order,
        force=force,
    )


@app.command()
def assemble_summaries(
    manifest_path: str,
    output_docx_path: str,
    title: str = None,
):
    assemble_chapter_summaries(manifest_path, output_docx_path, title)


@app.command()
def extract_boxed_case_law(
    chapters_dir: str,
    example_image_path: str,
    output_docx_path: str,
    output_xlsx_path: str = None,
    cache_dir: str = None,
    open_ai_key: str = None,
    model: str = None,
    concurrency: int = 2,
    retries: int = 3,
    env_path: str = ".env",
    force: bool = False,
    from_chapter: int = None,
    to_chapter: int = None,
    verbose: bool = True,
):
    """Extrait visuellement les jurisprudences présentes dans les encadrés."""
    logging.basicConfig(
        level=logging.INFO if verbose else logging.WARNING,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%H:%M:%S",
    )
    extract_boxed_case_law_chapters(
        chapters_dir=chapters_dir,
        example_image_path=example_image_path,
        output_docx_path=output_docx_path,
        output_xlsx_path=output_xlsx_path,
        cache_dir=cache_dir,
        open_ai_key=open_ai_key,
        model=model,
        concurrency=concurrency,
        retries=retries,
        env_path=env_path,
        force=force,
        from_chapter=from_chapter,
        to_chapter=to_chapter,
    )
    

if __name__ == "__main__":
    app()
