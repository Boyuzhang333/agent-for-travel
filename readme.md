User
 ↓
planner_agent
 ↓
budget_agent
 ↓
ParallelAgent
 ├ flight_agent
 ├ hotel_agent
 └ attraction_agent
 ↓
itinerary_agent


用户输入 出发地，目的地，玩的天数，预算

先把预算按逻辑分给 玩 吃 住 行 （涉及天数，目的地，预算）

然后各个部分拿着给定的预算，去挑应该选的东西：这个部分涉及tools，要求用 mock数据 提供酒店信息，航班信息，餐厅信息，娱乐信息，然后对应的agent，拿着给定的预算去挑选

然后每个这一部分的agent 返回好属于他们那一部分的返回体

最后用agent整合出一套回答
