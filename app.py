import streamlit as st
from langchain_groq import ChatGroq
from langchain.chains import LLMMathChain, LLMChain
from langchain.prompts import PromptTemplate
from langchain.agents.agent_types import AgentType
from langchain.agents import Tool, initialize_agent
from langchain.callbacks import StreamlitCallbackHandler
from duckduckgo_search import DDGS  # Replaced Wikipedia

# Streamlit app setup
st.set_page_config(page_title="Text To Math Problem Solver And Data Search Assistant", page_icon="🧮")
st.title("Text To Math Problem Solver Using llama-3.3-70b-versatile")

# Input Groq API key
groq_api_key = st.sidebar.text_input(label="Groq API Key", type="password")
if not groq_api_key:
    st.info("Please add your Groq API key to continue")
    st.stop()

# Initialize LLM model
llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=groq_api_key)

# Web search tool using DuckDuckGo
def search_duckduckgo(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=1)
        for r in results:
            return r["body"]

duckduckgo_tool = Tool(
    name="DuckDuckGoSearch",
    func=search_duckduckgo,
    description="Use this to get general information about any topic via web search."
)

# Math tool setup
math_chain = LLMMathChain.from_llm(llm=llm)
calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool for answering math-related questions. Only input mathematical expression needs to be provided."
)

# Reasoning prompt template
prompt = """
You're an agent tasked with solving the user's mathematical question. Logically arrive at the solution and provide a detailed explanation displayed point-wise.
Question: {question}
Answer:
"""

prompt_template = PromptTemplate(
    input_variables=["question"],
    template=prompt
)

chain = LLMChain(llm=llm, prompt=prompt_template)
reasoning_tool = Tool(
    name="Reasoning Tool",
    func=chain.run,
    description="A tool for answering logic-based and reasoning questions."
)

# Initialize the agent
assistant_agent = initialize_agent(
    tools=[duckduckgo_tool, calculator, reasoning_tool],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=False,
    handle_parsing_errors=True
)

# Chat history setup
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, I'm a Math chatbot who can answer all your math questions!"}
    ]

# Display chat history
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

# User input field
question = st.text_area("Enter your question:",
                        "I have 5 bananas and 7 grapes. I eat 2 bananas and give away 3 grapes. Then I buy a dozen apples and 2 packs of blueberries. Each pack of blueberries contains 25 berries. How many total pieces of fruit do I have at the end?")

# Handling user input and generating a response
if st.button("Find my answer"):
    if question:
        # Check if it's a math problem or a search query
        if "search:" in question.lower():
            search_query = question.replace("search:", "").strip()
            st.session_state.messages.append({"role": "user", "content": f"Searching for: {search_query}"})
            st.chat_message("user").write(f"Searching for: {search_query}")

            # Perform DuckDuckGo search and display result
            with st.spinner("Searching..."):
                search_result = search_duckduckgo(search_query)
                st.session_state.messages.append({"role": "assistant", "content": search_result})
                st.chat_message("assistant").write(search_result)
        else:
            # Process math problem
            st.session_state.messages.append({"role": "user", "content": question})
            st.chat_message("user").write(question)

            with st.spinner("Generating response..."):
                # Call assistant agent for math problem solving
                st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)
                response = assistant_agent.run(st.session_state.messages, callbacks=[st_cb])
                st.session_state.messages.append({'role': 'assistant', "content": response})
                st.write("### Response:")
                st.success(response)
    else:
        st.warning("Please enter a question.")
