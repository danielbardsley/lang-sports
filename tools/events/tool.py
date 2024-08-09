"""Tool for find upcoming sporting schedules"""
import logging
import json
from datetime import date
from typing import Optional, Type
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool

logger = logging.getLogger(__name__)


class EventQueryInput(BaseModel):
    """Input for the EventQuery tool."""
    start: date = Field(description="the start date for the query")
    end: date = Field(description="the end date for the query")


class EventQueryRun(BaseTool):
    """Tool that searches for upcoming sporting events."""

    name: str = "event-query"
    description: str = (
        "A wrapper around a sportsbook events api. "
        "Useful for when you need to answer questions about upcoming sports schedules "
        "Input should be a start date and an end date."
    )

    data = {}

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with open('../../data/highlights.json') as f:
            self.data = json.load(f)

    def _run(
            self,
            start: date, end: date,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> list:
        """Use the events query tool."""
        return self.data
