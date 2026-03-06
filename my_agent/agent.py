from google.adk.agents import LlmAgent, SequentialAgent, ParallelAgent
import os

from .tools.travel_tools import (
    search_flights,
    search_hotels,
    search_restaurants,
    search_activities
)

MODEL = os.getenv("ADK_MODEL_NAME", "ollama/qwen2.5:7b")
# -------------------------
# 1 Planner Agent
# -------------------------

planner_agent = LlmAgent(
    name="planner_agent",
    model=MODEL,
    instruction="""Extract travel information and return ONLY valid JSON (no markdown, no prose).

{
 "departure": "...",
 "destination": "...",
 "days": number,
 "budget": number
}""",
    output_key="travel_info"
)

# -------------------------
# 2 Budget Tool
# -------------------------

def allocate_budget(travel_info: dict) -> dict:
    total = int(travel_info["budget"])

    return {
        "transport_budget": int(total * 0.25),
        "hotel_budget": int(total * 0.40),
        "food_budget": int(total * 0.20),
        "activity_budget": int(total * 0.15)
    }

# -------------------------
# 3 Budget Agent
# -------------------------


budget_agent = LlmAgent(
    name="budget_agent",
    model=MODEL,
    tools=[allocate_budget],
    instruction="""
You MUST call the tool exactly once:

allocate_budget(travel_info)

After calling the tool:
Return ONLY the JSON returned by the tool.

Rules:
- Do NOT call allocate_budget again
- Do NOT modify the JSON
- Do NOT add explanations
""",
    output_key="budget_plan"
)
# -------------------------
# 4 Transport Agent
# -------------------------

transport_agent = LlmAgent(
    name="transport_agent",
    model=MODEL,
    tools=[search_flights],
    instruction="""
You are a flight selection agent.

Input:
{travel_info}
{budget_plan}

You have EXACTLY ONE available tool:
search_flights(departure, destination)

Rules:
1. Extract:
   - departure = departure_city from travel_info
   - destination = destination from travel_info
   - transport_budget from budget_plan
2. Call ONLY this tool exactly once:
   search_flights(departure, destination)
3. After the tool returns flight options, DO NOT call any tool again.
4. DO NOT invent tool names.
5. DO NOT call select_flight.
6. You must choose the cheapest flight within transport_budget.
7. If none fit the budget, choose the cheapest flight overall.

Return ONLY valid JSON:

{
  "airline": "...",
  "price": number
}
""",
    output_key="flight_option"
)

# -------------------------
# 5 Hotel Agent
# -------------------------

hotel_agent = LlmAgent(
    name="hotel_agent",
    model=MODEL,
    tools=[search_hotels],
    instruction="""
Return ONLY valid JSON (no markdown, no prose).

Input keys available:

travel info:
{travel_info}

budget:
{budget_plan}

destination = travel_info["destination"]
days = travel_info["days"]

You MUST call the tool exactly once:

search_hotels(destination)

Do not call any other tools.

Tool returns:

[
 {"hotel": "...", "price": number}
]

price = price per night

Calculate:

total_cost = price * days

CRITICAL: Choose a hotel ONLY FROM THE TOOL'S RETURNED HOTELS. NO INVENTING NEW HOTELS.
Select a hotel within budget_plan["hotel_budget"] (if none fit, pick the cheapest from the returned list).

Return JSON with EXACT data from the tool:

{
 "hotel": "...",
 "price_per_night": number,
 "total_cost": number
}

CRITICAL: Return ONLY hotels that the tool returned. Do NOT invent new hotels. Call the tool once, then produce the final JSON. Do NOT call the tool again.
""",
    output_key="hotel_option"
)

# -------------------------
# 6 Food Agent
# -------------------------

food_agent = LlmAgent(
    name="food_agent",
    model=MODEL,
    tools=[search_restaurants],
    instruction="""
Return ONLY valid JSON.

Input:

travel info:
{travel_info}

budget:
{budget_plan}

Extract:

destination = travel_info["destination"]
days = travel_info["days"]

STEP 1
Call tool exactly once:

search_restaurants(destination)

STEP 2
The tool will return a list of restaurants.

You MUST select restaurants ONLY from that returned list.

Rules:

• Do NOT invent restaurants
• Do NOT change prices
• Use EXACT values from the tool
• If days <= number of restaurants → return first N restaurants
• If days > number of restaurants → return all restaurants

Return JSON:

{
 "restaurants": [
   {"restaurant": "...", "avg_price": number}
 ]
}
""",
    output_key="food_plan"
)

# -------------------------
# 7 Activity Agent
# -------------------------

activity_agent = LlmAgent(
    name="activity_agent",
    model=MODEL,
    tools=[search_activities],
    instruction="""
Return ONLY valid JSON (no markdown, no prose).

Input keys available:

travel info:
{travel_info}

budget:
{budget_plan}

destination = travel_info["destination"]

You MUST call the tool exactly once:

search_activities(destination)

Do not call any other tools.

Tool returns:

[
 {"activity": "...", "price": number}
]

CRITICAL: You MUST ONLY SELECT FROM THE TOOL'S RETURNED ACTIVITIES. NO INVENTING OR ADDING NEW ONES.
Choose activities within activity_budget from the list above.

Return JSON - EXACT DATA FROM TOOL ONLY:

{
 "activities":[
   {"activity":"...", "price":number}
 ]
}

CRITICAL: Return ONLY activities that the tool returned. Do NOT invent new activities. Call the tool once, then produce the final JSON. Do NOT call the tool again.
""",
    output_key="activities"
)

# -------------------------
# 8 Parallel research workflow
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
# 9 Final Itinerary Agent
# -------------------------

final_agent = LlmAgent(
    name="final_itinerary_agent",
    model=MODEL,
    instruction="""
You MUST ONLY combine the provided inputs. Do NOT invent new flights/hotels/restaurants/activities.
Return ONLY valid JSON (no markdown, no prose).

Inputs:

{travel_info}
{budget_plan}
{flight_option}
{hotel_option}
{food_plan}
{activities}

Return JSON with this shape:

{
  "trip_summary": {
    "departure": "...",
    "destination": "...",
    "days": number,
    "budget": number
  },
  "budget_plan": {...},
  "flight_option": {...},
  "hotel_option": {...},
  "food_plan": {...},
  "activities": {...},
  "itinerary": "A readable itinerary as plain text (still inside this JSON string)."
}
""",
    output_key="final_plan"
)


presentation_agent = LlmAgent(
    name="presentation_agent",
    model=MODEL,
    instruction="""
You receive the final structured travel plan in JSON.

Input:
{final_plan}

Your task:
Convert this JSON into a clear natural language travel plan for the user.

Requirements:
- Explain the trip summary
- Show the chosen flight
- Show the hotel
- Mention restaurants
- Mention activities
- Present the itinerary day by day

Write in friendly natural language.

Do NOT output JSON.
Do NOT invent new data.
Only use the provided data.
""",
    output_key="final_answer"
)
# -------------------------
# Root workflow
# -------------------------

root_agent = SequentialAgent(
    name="travel_system",
    sub_agents=[
        planner_agent,
        budget_agent,
        research_workflow,
        final_agent,
        presentation_agent
    ]
)