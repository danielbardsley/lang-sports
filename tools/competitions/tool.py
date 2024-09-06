"""Tool for finding upcoming sporting schedules"""
import requests
from datetime import date
from typing import Optional, Type
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.tools import BaseTool


class CompetitionsQueryInput(BaseModel):
    """Input for the CompetitionsQuery tool."""
    sport: str = Field(description="The sport ID as returned by the sports-query tool")


class CompetitionsQueryRun(BaseTool):
    """Tool to find upcoming events for a sport from a given start date."""

    name: str = "competitions-query"
    description: str = (
        "A wrapper around a sports catalog api. "
        "Useful for when you need to know what competitions are available. "
        "Required input is sport id as returned by the sports-query tool"
    )

    def _run(
            self,
            sport: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> list:
        """Use the competitions query tool."""
        return requests.get('http://host.docker.internal:5000/sports/' + sport + '/competitions').json()