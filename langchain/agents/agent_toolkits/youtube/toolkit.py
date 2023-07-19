from __future__ import annotations

from typing import TYPE_CHECKING, List

from pydantic import Field

from langchain.agents.agent_toolkits.base import BaseToolkit
from langchain.tools import BaseTool
from langchain.tools.youtube.utils import build_resource_service
from langchain.tools.youtube import YouTubeSubscribe, YouTubeSearch

if TYPE_CHECKING:
    # This is for linting and IDE typehints
    from googleapiclient.discovery import Resource
else:
    try:
        # We do this so pydantic can resolve the types when instantiating
        from googleapiclient.discovery import Resource
    except ImportError:
        pass

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly",
          "https://www.googleapis.com/auth/youtubepartner"]


class YouTubeToolkit(BaseToolkit):
    """Toolkit for interacting with YouTube."""

    api_resource: Resource = Field(default_factory=build_resource_service)

    class Config:
        """Pydantic config."""

        arbitrary_types_allowed = True

    def get_tools(self) -> List[BaseTool]:
        """Get the tools in the toolkit."""
        return [
            YouTubeSubscribe(api_resource=self.api_resource),
            YouTubeSearch(api_resource=self.api_resource)
        ]
