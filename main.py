from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from datetime import datetime
import os
import requests

load_dotenv()

@tool
def calculator(a: float, b: float, operation: str = "+") -> str:
    """
    Perform basic arithmetic operations on two numbers.
    
    Parameters:
    - a (float): First number
    - b (float): Second number
    - operation (str): One of '+', '-', '*', '/', '%', '**'
    
    Returns:
    - str: Result of the calculation
    """
    
    try:
        if operation == "+":
            result = a + b
            op_name = "sum"
        elif operation == "-":
            result = a - b
            op_name = "difference"
        elif operation == "*":
            result = a * b
            op_name = "product"
        elif operation == "/":
            if b == 0:
                return "Error: Division by zero is not allowed."
            result = a / b
            op_name = "quotient"
        elif operation == "%":
            result = a % b
            op_name = "modulus"
        elif operation == "**":
            result = a ** b
            op_name = "power"
        else:
            return f"Error: Unsupported operation '{operation}'"
        
        return f"The {op_name} of {a} and {b} is {result}"
    
    except Exception as e:
        return f"An error occurred: {e}"

@tool
def get_datetime() -> str:
    """Useful for telling the current date and time"""
    return datetime.now().strftime("%A, %B %d, %Y %I:%M %p")

@tool
def get_weather(city: str) -> str:
    """Useful for getting the current weather in a city using OpenWeather API"""
    api_key = os.getenv("OPENWEATHER_API_KEY")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return f"Error fetching weather: {data.get('message', 'Unknown error')}"

    name = data["name"]
    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"].capitalize()
    humidity = data["main"]["humidity"]

    return f"The weather in {name} is {desc}, {temp}°F with {humidity}% humidity."



def main():
    model = ChatOpenAI(temperature=0) #seed

    # external service the tool can utilize
    tools = [calculator, get_datetime, get_weather]
    agent_executor = create_react_agent(model, tools)

    print("Welcome! I am your AI assistant. Type 'quit' to exit.")
    print("You can ask me to perform calculations or chat with me!")

    while True:
        user_input = input("\nYou: ").strip() 

        if user_input == "quit":
            break

        print("\nAssistant: ", end="")
        #stream the user input message to our agent 
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}
        ):
            # Checks if the current chunk we're on is a response from the agent, and if
            # there are any messages in that response
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content, end="")

        print()

if __name__ == "__main__":
    main()



