from typing import Type, Optional

from langchain.tools.youtube.base import YouTubeBaseTool
from pydantic import BaseModel, Field


class SubscribeSchema(BaseModel):
    channelId: str = Field(
        ...,
        description="The id of the blogger channel",
    )


class YouTubeSubscribe(YouTubeBaseTool):
    name: str = "youtube_subscribe"
    description: str = (
        "Use this tool to follow the blogger's youtube channel with the provided message fields."
    )
    args_schema: Type[SubscribeSchema] = SubscribeSchema

    def _prepare_subscribe(
            self,
            channelId: str,
    ):
        request = self.api_resource.subscriptions().insert(
            part="snippet",
            body={
                "snippet": {
                    "resourceId": {
                        "channelId": channelId
                    }
                }
            }
        )
        return request

    def _run(
            self,
            channelId: str,
    ) -> str:
        try:
            request = self._prepare_subscribe(channelId)
            response = request.execute()
            return response
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

    async def _arun(
            self,
            channelId: str,
    ) -> str:
        raise NotImplementedError(f"The tool {self.name} does not support async yet.")
