from typing import AsyncGenerator
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event

class ExpenseSummaryAgent(BaseAgent):
    """Provides summary of expenses by category or answers queries."""

    async def _run_async_impl(
        self, context: InvocationContext
    ) -> AsyncGenerator[Event, None]:

        query = context.session.state.get("query")  # e.g., "Total Groceries"
        expenses = context.session.state.get("expenses", {})

        if query:
            # Extract category from query
            category = query.split()[-1].capitalize()
            total = sum(expenses.get(category, []))
            print(f"Total spent on {category}: {total}")
        else:
            # Print all categories
            print("Expenses summary by category:")
            for cat, amounts in expenses.items():
                print(f"{cat}: {sum(amounts)}")

        yield Event(author=self.name)

