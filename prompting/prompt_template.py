from openai import OpenAI
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import OutputParserException
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, ValidationError
import json


class ResponseSchema(BaseModel):
    flag_law: bool
    label: str
    corpus: str
    institution: str
    type: str
    location: str
    date: str


# Function to process a DataFrame using the LLM
def iterate_llm_call(df, instruction, llm):
    # Ensure the DataFrame has a 'text' column
    if 'Text' not in df.columns:
        raise ValueError("DataFrame must contain a 'text' column")

    # Initialize output parser
    # parser = PydanticOutputParser(pydantic_model=ResponseSchema)

    results_list = []

    for _, row in df.iterrows():
        text = row['Text']
        parser = PydanticOutputParser(pydantic_object=ResponseSchema)

        prompt = PromptTemplate(
            template=instruction + "\n{format_instructions}\n{query}\n",
            input_variables=["query"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        prompt_and_model = prompt | llm 

        response= prompt_and_model.invoke({"query": text})

        try:
            response_dict = parser.invoke(response).dict()
        except (ValidationError, OutputParserException) as e:
            print(f"Error processing text: {text}\n{e}")
            response_dict = {
                'flag_law': '',
                'label': '',
                'corpus': '',
                'institution': '',
                'type': '',
                'location': '',
                'date': ''
            }
        response_dict["unique_id"] = row['unique_id']
        results_list.append(response_dict)
    return results_list