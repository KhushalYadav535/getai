import datetime
import time

import environ
from django.core.management.base import BaseCommand
from langchain import PromptTemplate
from langchain.agents import initialize_agent, AgentType, load_tools
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import (
    HumanMessage, SystemMessage
)

env = environ.Env()


def generate_text():
    llm = OpenAI(openai_api_key=env('OPENAI_API_KEY'), temperature=0.6, model_name="text-davinci-003")
    multiple_input_prompt = PromptTemplate(
        input_variables=["adjective", "content"],
        template="Tell me a {adjective} joke about {content}."
    )
    prompt_template = multiple_input_prompt.format(adjective="funny", content="science")
    response = llm(prompt_template)
    print(response, end='\n')


def generate_chat_messages():
    chat = ChatOpenAI(temperature=0.3, openai_api_key=env('OPENAI_API_KEY'))
    messages = [
        SystemMessage(content="You are an expert in healthcare."),
        HumanMessage(content="Tell me a word for a healthy person")
    ]
    response = chat(messages)
    print(response.content, end='\n')


def use_agent():
    llm = OpenAI(temperature=0.9)
    tools = load_tools(["google-serper"], llm=llm)
    agent_chain = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)
    agent_response = agent_chain.run("What is the price of paracetamol in India?")
    print(agent_response)


def agent_with_chat():
    system_message = "Act as an ecommerce expert in India. Provide shopping links, if the user mentions buying or shopping any product."
    agent_kwargs = {
        "system_message": system_message,
    }
    chat_llm = ChatOpenAI(temperature=0.2)
    tools = load_tools(["google-serper"], llm=chat_llm)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    agent_chain = initialize_agent(tools, chat_llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION, verbose=True,
                                   memory=memory, agent_kwargs=agent_kwargs)
    agent_response = agent_chain.run(input="What is the price of the apple airpods 2 pro?")
    print(agent_response)


class Command(BaseCommand):
    def handle(self, *args, **options):
        start = time.time()
        print("-------------------------------------------")
        print("Execution Started at", datetime.datetime.now())
        print("-------------------------------------------")
        agent_with_chat()
        end = time.time()
        print("-------------------------------------------")
        print("Execution Ended at", datetime.datetime.now())
        print("-------------------------------------------")
        print(f"Total execution time- {end - start}")
