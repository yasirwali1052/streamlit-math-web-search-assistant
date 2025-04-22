

# Text To Math Problem Solver and Data Search Assistant Using llama-3.3-70b-versatile

## Project Overview

This is a Streamlit app that allows users to input mathematical problems or general search queries, with the capability to process them using advanced AI models. The app uses **llama-3.3-70b-versatile** for natural language understanding and problem solving, combined with a web search feature using **DuckDuckGo** to fetch general information. The system responds with logical explanations for math problems and answers search queries with relevant data from the web.

**Features:**
- **Math Problem Solver:** Users can input math-related questions, and the model will solve them step by step.
- **Search Assistant:** Users can input search queries (prefixed with `search:`), and the system will fetch results from DuckDuckGo.
- **Interactive Chat Interface:** Provides a conversational interface where users can interact with the model in real time.

---

## Installation

Follow these steps to set up the app locally:

### 1. Clone the Repository

First, clone the repository from GitHub.

```bash
git clone https://github.com/yasirwali1052/streamlit-math-web-search-assistant.git
cd streamlit-math-web-search-assistant
```

Sure! Here's the updated section to set up a virtual environment using **Conda** instead of `venv`:

---

### 2. Set Up a Conda Environment (Recommended)

To avoid conflicts with other projects, create a Conda environment:

```bash
conda create --name myenv python=3.10
```

This command will create a new Conda environment named `myenv` with Python version 3.8.

Activate the Conda environment:

- On **Windows/macOS/Linux**:
  ```bash
  conda activate myenv
  ```

Once the environment is activated, you can proceed with installing the required dependencies.



### 3. Install Dependencies

Install the required Python libraries from the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

The `requirements.txt` file includes:

```txt
streamlit
langchain
langchain-community
langchain-groq
langchain-text-splitters
langchain-openai
python-dotenv
duckduckgo_search==5.3.1b1
```

---

## How to Use

1. **Run the App**  
   After installing dependencies, run the Streamlit app with the following command:

   ```bash
   streamlit run app.py
   ```

   This will launch the app in your default web browser.

2. **User Input**  
   - **Math Questions:** You can ask any math-related question, and the model will respond with a step-by-step solution.
   - **Search Queries:** To search for general information, prefix your query with `search:` (e.g., `search: What is quantum computing?`).

3. **Chat Interface:**  
   The app provides a chat interface where the conversation between the user and the assistant is displayed. You can continuously interact with the assistant.

---

## Groq API Setup

To use the llama-3.3-70b-versatile model, you need a **Groq API key**.

### Steps to Get Groq API Key:

1. **Sign Up on Groq**  
   Go to [Groq](https://www.groq.com/) and sign up for an account.

2. **Generate API Key**  
   Once logged in, navigate to the **API Keys** section and generate a new API key.

3. **Enter the API Key in the App**  
   In the app, you will be prompted to enter your Groq API key in the sidebar. This key is used to authenticate the app and access the llama-3.3-70b-versatile model.

---

## Dependencies

### 1. **Streamlit**  
   Streamlit is used to create the user interface for this app. It allows us to display the chat interface and handle user inputs.

### 2. **LangChain**  
   LangChain is a powerful framework used to connect large language models (LLMs) with other tools and databases. It is used here to process the math questions and search queries.

### 3. **Groq API**  
   The Groq API enables the use of the **llama-3.3-70b-versatile** model for natural language processing and problem-solving tasks.

### 4. **DuckDuckGo Search**  
   DuckDuckGo Search is used to search for general information from the web. When a user asks a question starting with `search:`, the system performs a web search and displays the top result.

---

## Code Explanation

### Streamlit Setup

1. **Streamlit Setup**:  
   We initialize the app's configuration using `st.set_page_config` and define the page title and icon.

2. **Groq API Key**:  
   The app takes the Groq API key input from the user via `st.sidebar.text_input`. If the key is missing, it prompts the user to provide it and stops further execution.

### Web Search Tool (DuckDuckGo)

The **search_duckduckgo** function uses the **DuckDuckGo search API** to retrieve relevant results based on the query. If the user inputs a query with the `search:` prefix, the app triggers this function.

```python
def search_duckduckgo(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=1)
        for r in results:
            return r["body"]
```

### Math Problem Solver

The **LLMMathChain** is used to solve math problems. It connects to the `llama-3.3-70b-versatile` model and handles input related to mathematical expressions. The math tool evaluates the expression and returns the solution.

```python
math_chain = LLMMathChain.from_llm(llm=llm)
calculator = Tool(
    name="Calculator",
    func=math_chain.run,
    description="A tool for answering math-related questions. Only input mathematical expression needs to be provided."
)
```

### Reasoning Tool

The **reasoning tool** uses an LLM chain to process complex reasoning tasks, like logical deductions or explaining the steps behind a mathematical solution. It is implemented with a custom prompt template.

```python
prompt_template = PromptTemplate(input_variables=["question"], template=prompt)
chain = LLMChain(llm=llm, prompt=prompt_template)
reasoning_tool = Tool(
    name="Reasoning Tool",
    func=chain.run,
    description="A tool for answering logic-based and reasoning questions."
)
```

### Handling User Input

The app distinguishes between math problems and search queries by checking if the question starts with `search:`. If it's a math problem, it passes the input to the `LLMMathChain` for processing. If it's a search query, it uses DuckDuckGo to fetch results.

```python
if "search:" in question.lower():
    search_query = question.replace("search:", "").strip()
    search_result = search_duckduckgo(search_query)
else:
    response = assistant_agent.run(st.session_state.messages, callbacks=[st_cb])
```


--- 

This README provides everything a new user needs to understand how to install, configure, and use your project. Let me know if you'd like any further adjustments!
