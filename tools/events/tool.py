"""Tool for finding upcoming sporting schedules"""
import requests
from datetime import date
from typing import Optional, Type
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool


class EventsQueryInput(BaseModel):
    """Input for the EventQuery tool."""
    start: date = Field(description="the start date for the query in yyy-mm-dd format")


class EventsQueryRun(BaseTool):
    """Tool to find upcoming events for a sport from a given start date."""

    name: str = "events-query"
    description: str = (
        "A wrapper around a sports catalog api. "
        "Useful for when you need to know what events are available. "
        "Required input is a start date in the correct format"
    )

    def _run(
            self,
            start: date,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> list:
        """Use the events query tool."""
        return requests.get('http://host.docker.internal:5000/events?dateFrom=' + str(start)).json()
