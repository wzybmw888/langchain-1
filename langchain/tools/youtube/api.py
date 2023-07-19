from abc import ABC
from typing import Any, Optional

from googleapiclient.errors import HttpError

from langchain.tools.youtube.utils import build_resource_service
import datetime


class YoutubeAPI(ABC):
    def __init__(self):
        # load credentials
        self.youtube = build_resource_service()

    def insert_subscriptions(self, channelId: str) -> Any:
        request = self.youtube.subscriptions().insert(
            part="snippet",
            body={
                "snippet": {
                    "resourceId": {
                        "channelId": channelId
                    }
                }
            }
        )
        try:
            response = request.execute()
            return response
        except HttpError as error:
            raise error

    def delete_subscriptions(self, **kwargs) -> dict:
        """
        https://developers.google.com/youtube/v3/docs/subscriptions/delete?hl=zh-cn
        """
        request = self.youtube.subscriptions().delete(
            **kwargs
        )
        try:
            response = request.execute()
            return response
        except HttpError as error:
            raise error

    def list_subscriptions(self, **kwargs) -> dict:
        """
        https://developers.google.com/youtube/v3/docs/subscriptions/list?hl=zh-cn
        """
        request = self.youtube.subscriptions().list(
            **kwargs
        )
        try:
            response = request.execute()
            return response
        except HttpError as error:
            raise error

    def search(self, **kwargs) -> dict:
        """
        https://developers.google.com/youtube/v3/docs/search/list?hl=zh-cn
        :return:
        """
        request = self.youtube.search().list(
            **kwargs
        )
        try:
            response = request.execute()
            return response
        except HttpError as error:
            raise error
        except Exception as error:
            raise error

    def videos(self, **kwargs):
        """
        https://developers.google.com/youtube/v3/docs/videos/list?hl=zh-cn
        :return:
        """
        request = self.youtube.videos().list(
            **kwargs
        )
        try:
            response = request.execute()
            return response
        except HttpError as error:
            raise error
        except Exception as error:
            raise error

    def channels(self, **kwargs):
        """
            https://developers.google.com/youtube/v3/docs/channels/list?hl=zh-cn
            :return:
        """
        request = self.youtube.channels().list(
            **kwargs
        )
        try:
            response = request.execute()
            return response
        except HttpError as error:
            raise error
        except Exception as error:
            raise error


class YouTubeAPIOperate(YoutubeAPI):
    def __init__(self):
        super().__init__()

    def delete_all_subscriptions(self):
        res = self.list_subscriptions_by_mine()
        for item in res["items"]:
            self.delete_signal_subscriptions_by_Id(item.get("id"))

    def delete_signal_subscriptions_by_Id(self, id: str):
        return self.delete_subscriptions(id=id)

    def insert_subscriptions_by_channelId(self, channelId: str):
        return self.insert_subscriptions(channelId=channelId)

    def list_subscriptions_by_channelId(self, channelId: str):
        """
        :param channelId The channelId parameter is used to specify the YouTube channel ID. The API will only return subscriptions for this channel.
        :return:
        """
        return self.list_subscriptions(part="snippet", channelId=channelId, maxResults=50)

    def list_subscriptions_by_mine(self):
        """
        :param mine This parameter can only be used in the correct authorization request. Set the value of this parameter to true to retrieve the Feed of the verified user's subscription.
        :return:
        """
        return self.list_subscriptions(part="snippet", mine=True, maxResults=50)

    def list_subscriptions_by_Id(self, id: str):
        """
        The ID parameter specifies a list of YouTube subscription ids (separated by commas) for the resource to retrieve.
        In the subscription resource, the id attribute is used to specify the YouTube subscription ID.
        """
        return self.list_subscriptions(part="snippet", id=id)

    def search_by_channelId(self, channelId: str, **kwargs):
        return self.search(part="snippet", channelId=channelId, **kwargs)

    def search_by_q(self, q: str, maxResults: Optional[int] = 5, publishedAfter: Optional[datetime.datetime] = None,
                    publishedBefore: Optional[datetime.datetime] = None):
        publishedBefore = publishedBefore.isoformat() + "Z" if publishedBefore else None
        publishedAfter = publishedAfter.isoformat() + "Z" if publishedAfter else None
        return self.search(q=q,
                           part="snippet",
                           maxResults=maxResults,
                           order="rating",
                           publishedAfter=publishedAfter,
                           publishedBefore=publishedBefore,
                           type="video",
                           )

    def videos_by_videoId(self, videoId: str):
        """
        Returns a list of videos that match the API request parameters.
        Quota impact: The quota cost for calling this method is 1 unit.
        :param videoId: the id of video
        :return:
        """
        return self.videos(part="statistics", id=videoId)

    def channel_by_channelId(self, channelId: str):
        """
        :param channelId: the channelId of channel
        :return:
        """
        return self.channels(part="statistics", id=channelId)
