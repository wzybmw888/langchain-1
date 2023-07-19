from abc import ABC
from typing import Any, Optional

from googleapiclient.errors import HttpError

from langchain.tools.youtube.utils import build_resource_service
import datetime


class YoutubeAPI(ABC):
    def __init__(self):
        # 加载credentials
        self.youtube = build_resource_service()

    def insert_subscriptions(self, channelId: str) -> Any:
        """
        为经过身份验证的用户的频道添加订阅。
        :param part 参数在此操作中有两个目的。它标识了写入操作将设置的属性以及 API 响应将包含的属性。
                以下列表包含您可以在参数值中包含的 part 名称：
                contentDetails
                id
                snippet
                subscriberSnippet
        :param channelId 要订阅的博主的channelId
        :return:
        """
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
        配额影响：调用此方法的配额费用为 50 个单位。
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
        配额影响：调用此方法的配额费用为 1 个单位。
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
        返回与 API 请求参数匹配的视频列表。
        配额影响：调用此方法的配额费用为 1 个单位。
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
            返回零个或多个符合请求条件的 channel 资源的集合。
            配额影响：调用此方法的配额费用为 1 个单位。
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
        ids = []
        items = res["items"]
        for item in items:
            ids.append(item.get("id"))
        for id in ids:
            self.delete_signal_subscriptions_by_Id(id)

    def delete_signal_subscriptions_by_Id(self, id: str):
        return self.delete_subscriptions(id=id)

    def insert_subscriptions_by_channelId(self, channelId: str):
        return self.insert_subscriptions(channelId=channelId)

    def list_subscriptions_by_channelId(self, channelId: str):
        """
        :param channelId 参数用于指定 YouTube 频道 ID。API 将仅返回此频道的订阅。
        :return:
        """
        return self.list_subscriptions(part="snippet", channelId=channelId)

    def list_subscriptions_by_mine(self):
        """
        :param mine 此参数只能在正确的授权请求中使用。将此参数的值设为 true，以检索已验证用户的订阅的 Feed。
        :return:
        """
        return self.list_subscriptions(part="snippet", mine=True)

    def list_subscriptions_by_Id(self, id: str):
        """
            id 参数指定要检索的资源的 YouTube 订阅 ID 列表（以英文逗号分隔）。在 subscription 资源中，id 属性用于指定 YouTube 订阅 ID。
            :return:
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
        返回与 API 请求参数匹配的视频列表。
        配额影响：调用此方法的配额费用为 1 个单位。
        :param videoId:
        :return:
        """
        return self.videos(part="statistics", id=videoId)

    def channel_by_channelId(self, channelId: str):
        """
        :param channelId:
        :return:
        """
        return self.channels(part="statistics", id=channelId)
