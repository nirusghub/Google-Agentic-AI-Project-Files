from typing import AsyncGenerator
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions

class ExpenseCategorizationAgent(BaseAgent):
    """Automatically classifies expenses into categories based on keywords."""

    KEYWORD_MAP = {
        "Groceries": ["milk", "veggies", "fruits", "groceries"],
        "Household": ["rent", "electricity", "water"],
        "Children": ["van fees", "school fees", "books"],
        "Transport": ["bus", "fuel", "taxi", "uber"],
        "Entertainment": ["movie", "concert", "games"]
    }

    async def _run_async_impl(
        self, context: InvocationContext
    ) -> AsyncGenerator[Event, None]:

        raw_expenses = context.session.state.get("raw_expenses", [])
        categorized = context.session.state.get("expenses", {})

        for exp in raw_expenses:
            matched = False
            for category, keywords in self.KEYWORD_MAP.items():
                if any(k in exp["description"] for k in keywords):
                    if category not in categorized:
                        categorized[category] = []
                    categorized[category].append(exp["amount"])
                    matched = True
                    break
            if not matched:
                # Uncategorized goes to Others
                if "Others" not in categorized:
                    categorized["Others"] = []
                categorized["Others"].append(exp["amount"])

        context.session.state["expenses"] = categorized
        yield Event(author=self.name, actions=EventActions(escalate=True))

