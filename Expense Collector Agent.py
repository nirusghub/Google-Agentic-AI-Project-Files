from typing import AsyncGenerator
from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions

class ExpenseCollectorAgent(BaseAgent):
    """Collects expense input and stores it in session state."""

    async def _run_async_impl(
        self, context: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        user_input = context.session.state.get("user_input")  # e.g., "50 Van fees"
        if not user_input:
            yield Event(author=self.name)
            return

        # Parse input: assume "amount description"
        try:
            parts = user_input.split(maxsplit=1)
            amount = float(parts[0])
            description = parts[1].lower()
        except:
            yield Event(author=self.name)
            return

        # Initialize raw expenses list
        raw_expenses = context.session.state.get("raw_expenses", [])
        raw_expenses.append({"amount": amount, "description": description})
        context.session.state["raw_expenses"] = raw_expenses

        # Escalate to next agent
        yield Event(author=self.name, actions=EventActions(escalate=True))

