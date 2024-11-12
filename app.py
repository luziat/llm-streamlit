import os
import streamlit as st
from dotenv import load_dotenv
from langchain import hub
from langchain.agents import AgentExecutor, create_openai_tools_agent, load_tools
from langchain.memory import ConversationBufferMemory
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_community.chat_message_histories import StreamlitChatMessageHistory
from langchain_openai import ChatOpenAI

load_dotenv()

def create_agent_chain(history):
  chat = ChatOpenAI(
    model_name="gpt-4o-mini"
    temperature=0
  )

  tools = load_tools(["ddg-search", "wikipedia"])

  prompt = hub.pull("hwchase17/openai-tools-agent")

  memory = ConversationBufferMemory(
    chat_memory=history, memory_key="chat_history", return_messages=True
  )

  agent = create_openai_tools_agent(chat, tools, prompt)
  return AgentExecutor(agent=agent, tools=tools, memory=memory)

st.title("langchain-streamlit-app")

history = StreamlitChatMessageHistory()

for message in history.messages:
  st.chat_message(message.type).write(message.content)
