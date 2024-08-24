import streamlit as st
import logging
import json
import time
from concurrent.futures import ThreadPoolExecutor
from math import ceil
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_qdrant import Qdrant
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

import os


class OpenAIApp:
    def __init__(self, user_token):
        load_dotenv()  # Load environment variables from .env file

        self.OPENAI_API_KEY = user_token  # Replace with your actual API key

    def start_gpt_process(
        self,
        refine_template,
        content,
    ):
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", refine_template),
                ("human", "{input}"),
            ]
        )
        model = ChatOpenAI(
            model="gpt-4o-2024-08-06",
            temperature=0,
            openai_api_key=self.OPENAI_API_KEY,
        )

        chain = create_stuff_documents_chain(llm=model, prompt=prompt)

        answer = self.invoke_chain_segment(
            content,
            chain,
        )

        return answer

    def invoke_chain_segment(
        self,
        content_segment,
        chain,
    ):
        retries = 0
        while retries < 2:
            try:
                answer = chain.invoke(
                    {
                        "context": content_segment,
                        "input": f"Return all needed",
                    }
                )
                print("this is my answer ", answer)
                return answer
            except Exception as e:
                logging.info("Error encountered: ", str(e))
                retries += 1
                if retries < 3:
                    logging.info(f"Retrying in {5} seconds... ({retries}/{3})")
                    time.sleep(5)
                else:
                    print("Max retries reached. Moving to the next task.")
                    return None
