## **Langchain + OpenAI Demo Agent**
This project demonstrates a custom **AI chatbot (Agent)** built with **Langchain**, **Langgraph**, and **OpenAI**.

The agent:
1) Uses OpenAI's Chat API
2) Can use a multitude of tools (calculator, weather, and date & time)
3) Responds interactively in a loop until the user quits

Essentially, it works like ChatGPT but with custom tools the user can add.
If the model detects that a user request matches one of these tools, it will automatically call it.

# **Libraries Used:**
- `langchain` – High-level framework for building AI applications
- `langgraph` – Framework for building AI Agents
- `langchain-openai` – Integrates OpenAI within Langchain and Langgraph
- `python-dotenv` – Loads environment variables from `.env` files

# **Tools:**
- **Calculator** - Performs basic arithmetic functions
- **Date & Time** - Uses Python’s `datetime` library to retrieve the current date and time
- **Weather** -  Calls the **OpenWeatherAPI** to fetch weather information for different cities
