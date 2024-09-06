"""Tool for returning a list of available sports"""
import requests

from typing import Optional
from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool


class SportsQueryRun(BaseTool):
    """Tool that knows which sports are currently available."""
    name: str = "sports-query"
    description: str = (
        "A wrapper around a sports catalog api. "
        "Useful for when you need to know what sports are available. "
        "No input is required"
    )

    def _run(
            self,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> list:
        """Use the sports query tool."""
        return requests.get('http://host.docker.internal:5000/sports').json()
