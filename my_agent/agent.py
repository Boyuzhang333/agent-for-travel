from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
from google.adk.tools import AgentTool
import os

MODEL = os.getenv("ADK_MODEL_NAME", "ollama/gemma2:2b")

# -------------------------
# 1 Planner Agent
# -------------------------

planner_agent = LlmAgent(
    name="planner_agent",
    model=MODEL,
    instruction="""
Extract travel info from user input.

Return format:

departure_city: ...
destination: ...
days: ...
budget: ...
""",
    output_key="travel_info"
)

# -------------------------
# 2 Budget Agent
# -------------------------

budget_agent = LlmAgent(
    name="budget_agent",
    model=MODEL,
    instruction="""
Given travel info:

{travel_info}

Split the total budget into:

transport_budget
hotel_budget
food_budget
activity_budget

Return structured text.
""",
    output_key="budget_plan"
)

# -------------------------
# 3 Transport Agent
# -------------------------

transport_agent = LlmAgent(
    name="transport_agent",
    model=MODEL,
    instruction="""
You are responsible ONLY for selecting flights.

Use:
{travel_info}
{budget_plan}

Return:

flight_option:
- airline
- price

Do not generate itinerary.
""",
    output_key="flight_option"
)

# -------------------------
# 4 Hotel Agent
# -------------------------

hotel_agent = LlmAgent(
    name="hotel_agent",
    model=MODEL,
    instruction="""
You are responsible ONLY for selecting a hotel.

Return:

hotel_option:
- hotel name
- price per night
""",
    output_key="hotel_option"
)

# -------------------------
# 5 Food Agent
# -------------------------

food_agent = LlmAgent(
    name="food_agent",
    model=MODEL,
    instruction="""
You are responsible ONLY for selecting restaurants.

Return:

restaurant_list:
- name
- average price
""",
    output_key="food_plan"
)

# -------------------------
# 6 Activity Agent
# -------------------------

activity_agent = LlmAgent(
    name="activity_agent",
    model=MODEL,
    instruction="""
You are responsible ONLY for selecting activities.

Input:
{travel_info}
{budget_plan}

Select activities within activity_budget.

Return ONLY:

activity_list:
- activity name
- price

Do NOT generate a travel itinerary.
Do NOT suggest hotels or flights.
""",
    output_key="activities"
)
# -------------------------
# Parallel workflow
# -------------------------

research_workflow = ParallelAgent(
    name="research_agents",
    sub_agents=[
        transport_agent,
        hotel_agent,
        food_agent,
        activity_agent
    ]
)

# -------------------------
# Final Itinerary Agent
# -------------------------

final_agent = LlmAgent(
    name="final_itinerary_agent",
    model=MODEL,
    instruction="""
Create final travel itinerary.

Inputs:

{travel_info}
{budget_plan}
{flight_option}
{hotel_option}
{food_plan}
{activities}

Generate a clear day-by-day travel plan.
""",
    output_key="final_plan"
)

# delegation example (AgentTool)

flight_tool = AgentTool(agent=transport_agent)

# -------------------------
# Root workflow
# -------------------------

root_agent = SequentialAgent(
    name="travel_system",
    sub_agents=[
        planner_agent,
        budget_agent,
        research_workflow,
        final_agent
    ]
)