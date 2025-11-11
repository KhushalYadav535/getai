import time
from datetime import datetime

from django.core.cache import cache
from environ import environ
from langchain import PromptTemplate, LLMChain
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.chains import SequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.schema import (
    HumanMessage, SystemMessage
)
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from app_modules.llm import helpers
from base import constants


class StartChatAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        env = environ.Env()
        # user = request.user
        chat_bot_type = data.get('chat_bot_type')
        name = data.get('name')
        age = data.get('age')
        location = data.get('location')
        user_chat_cache_key = data.get('user_chat_cache_key')
        if not user_chat_cache_key:
            random_number = helpers.random_number()
            # user_chat_cache_key = helpers.get_user_cache_key(chat_bot_type, user)
            user_chat_cache_key = constants.LLMConstants.CACHE_KEYS[chat_bot_type].format(user_id=random_number)
        helpers.delete_user_cache_key(user_chat_cache_key)
        chat_llm = ChatOpenAI(temperature=1.0, openai_api_key=env('OPENAI_API_KEY'),
                              model_name=constants.LLMConstants.CHAT_LLM_MODEL, max_tokens=250)
        if chat_bot_type == constants.LLMConstants.HEALTHCARE:
            system_message = SystemMessage(
                content=constants.LLMConstants.HEALTHCARE_INITIAL_PROMPT.format(name=name, age=age,
                                                                                location=location))
            human_message = HumanMessage(content="Hi, Doctor")
        else:
            system_message = SystemMessage(
                content=constants.LLMConstants.FINANCE_INITIAL_PROMPT.format(name=name, age=age,
                                                                             location=location))
            human_message = HumanMessage(content="Hello!")
        initial_messages = [system_message, human_message]
        ai_message = chat_llm(initial_messages)
        initial_messages += [ai_message]
        cache.set(user_chat_cache_key, initial_messages)
        ai_message_content = ai_message.content

        return Response({"ai_message_content": ai_message_content, "user_chat_cache_key": user_chat_cache_key},
                        status=status.HTTP_200_OK)


class TextGenerationAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        env = environ.Env()
        # user = request.user
        data = request.data
        user_chat_cache_key = data.get('user_chat_cache_key')
        human_message_data = data.get('human_message')
        chat_llm = ChatOpenAI(temperature=1.0, openai_api_key=env('OPENAI_API_KEY'),
                              model_name=constants.LLMConstants.CHAT_LLM_MODEL, max_tokens=250)
        human_message = HumanMessage(content=human_message_data)
        chat_history = cache.get(user_chat_cache_key) + [human_message]
        ai_message = chat_llm(chat_history)
        chat_history += [ai_message]
        cache.set(user_chat_cache_key, chat_history)
        ai_message_content = ai_message.content
        return Response({"ai_message_content": ai_message_content},
                        status=status.HTTP_200_OK)


class ChainingAPIView(APIView):

    def post(self, request):
        organic_results = None
        env = environ.Env()
        user = request.user
        data = request.data
        cache_key = f"USER_ID_{user.id}"
        human_message_data = data.get('human_message')
        start = time.time()
        print("--------------------NEW-------------------")
        print("Execution Started at", datetime.now())
        print("-------------------------------------------")
        chat = ChatOpenAI(temperature=1.0, openai_api_key=env('OPENAI_API_KEY'))
        #       Your replies/answers must include:
        #         1) Links of articles
        #         2) Medicines
        #         3) Addresses of nearby pharmacies and hospitals
        system_message_data = """
        I want you to act like a Doctor with an experience of 15 years. I want you to respond and answer 
        like a Doctor using the tone, manner and vocabulary a Doctor would use. "Do not write any explanations". 
        You have to answer based on the knowledge you have till September 2021.

        User Profile Data:
        1) My name is Prashant.
        2) Location: Indore, Madhya Pradesh, India
        3) Age: 24 years 
        """

        symptoms_template = PromptTemplate(
            input_variables=['symptoms'],
            template=system_message_data
        )

        references_template = PromptTemplate(
            input_variables=['symptoms_observation'],
            template='Give a list of hospitals in Ahmedabad, also provide reference links of medical articles and medicines on the symptoms observation: {symptoms_observation}'
        )

        # symptoms_memory = ConversationBufferMemory(input_key='symptoms', memory_key='chat_history')
        # references_memory = ConversationBufferMemory(input_key='references_details', memory_key='chat_history')

        symptoms_chain = LLMChain(llm=chat, prompt=symptoms_template, verbose=True, output_key='symptoms_observation')
        references_chain = LLMChain(llm=chat, prompt=references_template, verbose=True,
                                    output_key='references_details', )
        sequential_chain = SequentialChain(chains=[symptoms_chain, references_chain], input_variables=['symptoms'],
                                           output_variables=['symptoms_observation', 'references_details'])

        response = sequential_chain({"symptoms": human_message_data})
        print(response)

        # system_message = SystemMessage(content=system_message_data)
        # human_message = HumanMessage(content=human_message_data)

        # cached_messages = cache.get(cache_key)
        # print(cached_messages)
        # if not cached_messages:
        #     messages = [system_message, human_message]
        # else:
        #     messages = cached_messages + [human_message]
        # chat_message = chat(messages)
        # ai_message = [chat_message]
        # cache.set(cache_key, messages + ai_message)
        # chat_message_content = chat_message.content
        print("-------------------------------------------")
        print("Execution Ended at", datetime.now())
        print("-------------------------------------------")
        end = time.time()
        print(f"Total execution time- {end - start}")
        return Response({"ai_generated_text": ai_generated_text},
                        status=status.HTTP_200_OK)


class AgentTextGenerationAPIView(APIView):

    def post(self, request):
        # env = environ.Env()
        user = request.user
        data = request.data
        cache_key = f"USER_ID_{user.id}"
        human_message_data = data.get('human_message')
        start = time.time()
        print("--------------------NEW-------------------")
        print("Execution Started at", datetime.now())
        print("-------------------------------------------")
        system_message = "Act as an AI Assistant, who can find and answer anything. You will give appropriate answers in detail. Any part of the question should not be missed. Provide references, links if possible with answer"
        agent_kwargs = {
            "system_message": system_message,
        }
        chat_llm = ChatOpenAI(temperature=0.4)
        tools = load_tools(["google-serper"], llm=chat_llm)
        # search = GoogleSerperAPIWrapper()
        # tools = [
        #     Tool(
        #         name="Intermediate Answer",
        #         func=search.run,
        #         description='google search'
        #     )
        # ]
        cached_memory = cache.get(cache_key)
        print(cached_memory)
        print(type(cached_memory))
        print(dir(cached_memory))
        if not cached_memory:
            new_memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
            cached_memory = new_memory
            agent_chain = initialize_agent(tools, chat_llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                                           verbose=True,
                                           memory=cached_memory, agent_kwargs=agent_kwargs)
        else:
            agent_chain = initialize_agent(tools, chat_llm, agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
                                           verbose=True,
                                           memory=cached_memory, agent_kwargs=agent_kwargs)
        agent_response = agent_chain.run(input=human_message_data)
        cached_memory.chat_memory.add_user_message(human_message_data)
        cached_memory.chat_memory.add_ai_message(agent_response)
        cache.set(cache_key, cached_memory)
        end = time.time()
        print("-------------------------------------------")
        print("Execution Ended at", datetime.now())
        print("-------------------------------------------")
        print(f"Total execution time- {end - start}")
        return Response({"generated_text": agent_response}, status=status.HTTP_200_OK)

# class ClearCacheAPIView(APIView):
#
#     def post(self, request):
#         user = request.user
#         chat_bot_type = request.data.get('chat_bot_type')
#
#         cache_key = f"USER_ID_{user.id}"
#         helpers.clear_user_cache(chat_bot_type, cache_key)
#         cache.delete(cache_key)
#         return Response({"message": "History removed"}, status=status.HTTP_200_OK)
