import asyncio
import json

from openai import OpenAI
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import OutputParserException
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, ValidationError
from langchain.chains import LLMChain


class ResponseSchema(BaseModel):
    flag_law: bool
    label: str
    corpus: str
    institution: str
    type: str
    location: str
    date: str

def get_chain(instruction, llm, parser):
    

    prompt = PromptTemplate(
        template=instruction + "\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser
    # chain = LLMChain(llm=llm, prompt=prompt)
    return chain

# Asynchronous function to process a single response
def parse_response(response, parser):
    try:
        response_dict = parser.invoke(response).dict()
    except (ValidationError, OutputParserException) as e:
        print(f"Error processing \n{e}")
        response_dict = {
            "flag_law": "",
            "label": "",
            "corpus": "",
            "institution": "",
            "type": "",
            "location": "",
            "date": ""
        }
    return response_dict

# Asynchronous processing with astream
async def process_texts_async(chain,texts, parser):
    results = []

    async for text, result in zip(texts, chain.astream({"query": text} for text in texts)):
        # parsed_result_dict = parse_response(result, parser)
        print("##### TEXT, ", text )
        print("###### result, ", result)
        results.append(result.dict())
    return results

async def get_results(chain, batches, parser):
    all_results = []
    for batch in batches:
        batch_results = await process_texts_async(chain, batch, parser)
        all_results.extend(batch_results)
    return all_results

def get_batches(df, batch_size):
    return [df['Text'][i:i + batch_size].fillna("").tolist() for i in range(0, len(df), batch_size)]

# Function to process a DataFrame using the LLM
def batch_call(df, instruction, llm, batch_size = 500):
    # Ensure the DataFrame has a 'text' column
    if 'Text' not in df.columns:
        raise ValueError("DataFrame must contain a 'text' column")
    
    batches_list = get_batches(df, batch_size)
    parser = PydanticOutputParser(pydantic_object=ResponseSchema)
    
    chain=get_chain(instruction, llm, parser)

    #results_list =asyncio.run(get_results(chain, batches, parser))
    loop = asyncio.get_event_loop()
    results_list = loop.run_until_complete(get_results(chain, batches_list, parser))

    return results_list