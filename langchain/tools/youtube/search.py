"""
Adapted from https://github.com/venuv/langchain_yt_tools

CustomYTSearchTool searches YouTube videos related to a person
and returns a specified number of video URLs.
Input to this tool should be a comma separated list,
 - the first part contains a person name
 - and the second(optional) a number that is the
    maximum number of video results to return
 """
import datetime
import json
from typing import Optional, Type

from pydantic import BaseModel, Field

from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from langchain.tools.youtube.base import YouTubeBaseTool


class YouTubeSearchTool(BaseTool):
    name = "youtube_search"
    description = (
        "search for youtube videos associated with a person. "
        "the input to this tool should be a comma separated list, "
        "the first part contains a person name and the second a "
        "number that is the maximum number of video results "
        "to return aka num_results. the second part is optional"
    )

    def _search(self, person: str, num_results: int) -> str:
        from youtube_search import YoutubeSearch

        results = YoutubeSearch(person, num_results).to_json()
        data = json.loads(results)
        url_suffix_list = [video["url_suffix"] for video in data["videos"]]
        return str(url_suffix_list)

    def _run(
            self,
            query: str,
            run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool."""
        values = query.split(",")
        person = values[0]
        if len(values) > 1:
            num_results = int(values[1])
        else:
            num_results = 2
        return self._search(person, num_results)

    async def _arun(
            self,
            query: str,
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("YouTubeSearchTool  does not yet support async")


class SearchSchema(BaseModel):
    q: str = Field(
        ...,
        description="The q parameter specifies the query term to search for",
    )
    maxResults: Optional[int] = Field(5,
                                      description="The maxResults parameter specifies the maximum number of items that should be returned in the result set. Acceptable values are 0 to 50, inclusive. The default value is 5")
    publishedAfter: Optional[datetime.datetime] = Field(default=datetime.datetime(2023, 1, 1),
                                                        description="The publishedAfter parameter indicates that the API response should only contain resources created at or after the specified time")
    publishedBefore: Optional[datetime.datetime] = Field(default=datetime.datetime(2023, 1, 1),
                                                         description="The publishedBefore parameter indicates that the API response should only contain resources created before or at the specified time.")


class YouTubeSearch(YouTubeBaseTool):
    name: str = "youtube_search"
    description: str = (
        "Use this tool to search related videos with the provided message fields."
    )
    args_schema: Type[SearchSchema] = SearchSchema

    def _prepare_search(
            self,
            q: str,
            maxResults: Optional[int] = 5,
            publishedAfter: Optional[datetime.datetime] = None,
            publishedBefore: Optional[datetime.datetime] = None,
    ):
        publishedBefore = publishedBefore.isoformat() + "Z" if publishedBefore else None
        publishedAfter = publishedAfter.isoformat() + "Z" if publishedAfter else None
        request = self.api_resource.search().list(
            q=q,
            part="snippet",
            maxResults=maxResults,
            order="rating",
            publishedAfter=publishedAfter,
            publishedBefore=publishedBefore,
            type="video",
        )
        return request

    def _run(
            self,
            q: str,
            maxResults: Optional[int] = 5,
            publishedAfter: Optional[datetime.datetime] = None,
            publishedBefore: Optional[datetime.datetime] = None,
    ) -> dict:
        try:
            request = self._prepare_search(q=q, maxResults=maxResults, publishedAfter=publishedAfter,
                                           publishedBefore=publishedBefore)
            response = request.execute()
        except Exception as e:
            raise Exception(f"An error occurred: {e}")

        items = response["items"]
        _data = {
            "videoId": [],
            "title": [],
            "videoUrl": [],
            "description": [],
            "channelId": [],
            "publishTime": [],
            "viewCount": [],
            "likeCount": [],
            "commentCount": []
        }
        for item in items:
            videoId = _data.get("videoId")
            title = _data.get("title")
            videoUrl = _data.get("videoUrl")
            description = _data.get("description")
            channelId = _data.get("channelId")
            publishTime = _data.get("publishTime")

            videoId.append(item["id"]["videoId"])
            title.append(item["snippet"]["title"])
            videoUrl.append(f'https://www.youtube.com/watch?v={item["id"]["videoId"]}')
            description.append(item["snippet"]["description"])
            channelId.append(item["snippet"]["channelId"])
            publishTime.append(item["snippet"]["publishedAt"])

        # Obtain video information based on the video id
        videoIds = _data["videoId"]
        for i, videoId in enumerate(videoIds):
            response = self._videos_by_videoId(videoId)
            item = response["items"][0]
            viewCount = _data.get("viewCount")
            likeCount = _data.get("likeCount")
            commentCount = _data.get("commentCount")

            viewCount.append(item.get("statistics").get("viewCount"))
            likeCount.append(item.get("statistics").get("likeCount"))
            commentCount.append(item.get("statistics").get("commentCount"))
        return _data

    async def _arun(
            self,
            channelId: str,
    ) -> str:
        raise NotImplementedError(f"The tool {self.name} does not support async yet.")

    def _videos_by_videoId(self, videoId: str):
        request = self.api_resource.videos().list(
            part="statistics",
            id=videoId
        )
        try:
            response = request.execute()
            return response
        except Exception as e:
            raise Exception(f"An error occurred: {e}")
