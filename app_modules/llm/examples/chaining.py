import os

import streamlit as st
from langchain.chains import LLMChain, SequentialChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate

os.environ['OPENAI_API_KEY'] = "***REMOVED***"

# App framework
st.title('Your personal doctor')
prompt = st.text_input('Write your symptoms here')

# Prompt templates
symptoms_template = PromptTemplate(
    input_variables=['symptoms'],
    template='Write some remedies based on the symptoms: {symptoms}. '
)

references_template = PromptTemplate(
    input_variables=['symptoms_observation'],
    template='Give a list of hospitals in Ahmedabad, also provide reference links of medical articles and medicines on the symptoms observation: {symptoms_observation}'
)

# Memory
symptoms_memory = ConversationBufferMemory(input_key='symptoms', memory_key='chat_history')
# references_memory = ConversationBufferMemory(input_key='references_details', memory_key='chat_history')

llm = ChatOpenAI(temperature=1.0, )
symptoms_chain = LLMChain(llm=llm, prompt=symptoms_template, verbose=True, output_key='symptoms_observation',
                          memory=symptoms_memory)
references_chain = LLMChain(llm=llm, prompt=references_template, verbose=True, output_key='references_details', )
sequential_chain = SequentialChain(chains=[symptoms_chain, references_chain], input_variables=['symptoms'],
                                   output_variables=['symptoms_observation', 'references_details'])
# wiki = WikipediaAPIWrapper()

# Show stuff to the screen if there's a prompt
if prompt:
    # response = sequential_chain({"symptoms": prompt})
    # st.write(response['symptoms_observation'])
    # st.write(response['references_details'])

    symptoms_observation = symptoms_chain.run(prompt)
    # wiki_research = wiki.run(prompt)
    references_details = references_chain.run(symptoms_observation=symptoms_observation)
    # print(symptoms_observation)
    # print(references_details)

    st.write(symptoms_observation)
    st.write(references_details)

    with st.expander('Title History'):
        st.info(symptoms_memory.buffer)

    # with st.expander('Script History'):
    #     st.info(references_memory.buffer)
    #
    # with st.expander('Wikipedia Research'):
    #     st.info(wiki_research)
