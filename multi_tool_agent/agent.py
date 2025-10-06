import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents.callback_context import CallbackContext
from google.adk.models import LlmRequest
import os

import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="log.txt",  # Log to this file
    filemode="a",  # Append mode
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (f"Sorry, I don't have timezone information for {city}."),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = f'The current time in {city} is {now.strftime("%Y-%m-%d %H:%M:%S %Z%z")}'
    return {"status": "success", "report": report}


def simeple_before_model_callback(
    callback_context: CallbackContext,
    llm_request: LlmRequest,
) -> None:
    logging.debug(f"callback context: {callback_context.__dict__}")


root_agent = Agent(
    name="weather_time_agent",
    model=LiteLlm(
        model="openrouter/google/gemini-2.0-flash-lite-001",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        api_base="https://openrouter.ai/api/v1/chat/completions",
    ),
    description=("Agent to answer questions about the time and weather in a city."),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
    before_model_callback=simeple_before_model_callback,
)

a2a_app = to_a2a(root_agent, port=8001)
