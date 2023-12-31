from langchain import PromptTemplate

from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
memory = ConversationBufferMemory(memory_key="history",return_messages=True)
import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI


template="""
Your goal is to:
- Generate {long} paragraph long text in a {level} proficiency level 
- Give the first sentence of the text, Jump to a new line, Write the translation of the first sentence to user's preferred {translate} language within ().
- Continue by first writing the sentence, Jump to a new line, Then its translation within ()
- For example,
This is the text: 
Es regnete den ganzen Tag lang. Aufgrund des anhaltenden Regens verschoben sich die Pläne, die Insel zu besuchen. Dies war eine schöne Erfahrung.
Give the first sentence of the text: Es regnete den ganzen Tag lang. \n\n
Translation of that first sentence, it should be {translate} language, I am giving it in English as an example: It rained all day long.
Give the second sentence of the text: Aufgrund des anhaltenden Regens verschoben sich die Pläne, die Insel zu besuchen.
Translation of that second sentence: Due to the persistent rain, plans to visit the island were postponed.
Give the third sentence of the text:Dies war eine schöne Erfahrung.
Translation of that third sentence: This was a nice experience.
- Generate texts that are easy to read and follow in {level} level.
- Generate texts that are creative,arouse a sense of curiosity and related with the respective language's spoken country or countries culture,cousine,ancient cities,historical places,music,climate,architecture,landscapes

Level: {level}
Language: {language}
Long: {long}
Preference: {translate}"""

prompt = PromptTemplate(template=template, input_variables=["level","language","long","translate"])

def load_llm(openai_api_key):
    llm= OpenAI(temperature=.8,openai_api_key=openai_api_key)
    conversation=ConversationChain(llm=llm, memory=memory)
    return llm

st.set_page_config(page_title="Reading-Writing", page_icon=":robot:")
st.header("Generate Text")

st.markdown("**Read & Write**")


def get_api_key():
    input_text=st.text_input(label="OpenAI API Key", placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text
openai_api_key=get_api_key()


col1,col2,col3,col4 = st.columns(4)
with col1:
    language_inputs= st.selectbox("Which language would you like your text to have?",('German','English','Spanish','Turkish'))

with col2:
    level=st.selectbox("What is your level of proficiency",('A1','A2','B1','B2','C1'))    

with col3:
    translate_input= st.selectbox("Which language do you want to translate to?",('English','Turkish','German','Spanish','Portuguese'))

with col4:
    long_inputs= st.selectbox("How many paragraphs would you like to read?",('1-2','2-3','3-4','4-5','5-6'))


if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()

llm= load_llm(openai_api_key=openai_api_key)
prompt_with_sum=prompt.format(level=level, translate=translate_input, long=long_inputs, language=language_inputs)
result=llm(prompt_with_sum)
st.write(result)

template2="""
- After the user writes a summary, evaluate that summary, explain what the user did wrong grammatically
- Do not write the user' summary 
- Show 2 other alternative ways to write summary about that text.
- Explain the sentence sturucture and grammatical rules of these alternatives, and they should be short. 
- If user asks questions about sentence sturucture and grammatical rules, answer them. But do not answer other type of questions.
- Write all these things in {translate} language.
Input: {summary}
Preference: {translate}
Your Response:
"""

prompt = PromptTemplate(template=template2,input_variables=["translate","summary"])

def get_summary():
    input_text= st.text_area(label="Summary Input", label_visibility="collapsed", placeholder="Your Summary...", key="summary_input")
    return input_text
input_=get_summary()

if len(input_.split(" ")) > 1000:
    st.write("Please enter a shorter email. The maximum length is 1000 words.")
    st.stop()

st.markdown("### Your Evaluated Summary:")

if input_:
    if not openai_api_key:
        st.warning('Please insert OpenAI API Key. Instructions [here](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key)', icon="⚠️")
        st.stop()
    
    llm= load_llm(openai_api_key=openai_api_key)
    prompt_with_sum= prompt.format(summary=input_, translate=translate_input)
    summary_result= llm(prompt_with_sum)
    st.write(summary_result)
