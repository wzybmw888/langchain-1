"""
自定义youtube工具，可实现更为精准化的控制
1. 获取相关视频
2. 自动关注博主
3. 写入数据库
4. 数据库推送
"""
import datetime

import numpy as np
import pandas as pd
from typing import Tuple, List, Type

from pydantic import BaseModel, Field
from sklearn import preprocessing

from langchain.tools.youtube.api import YouTubeAPIOperate
from langchain.tools.youtube.base import YouTubeBaseTool
from workspace.custom_tools.json_utils import load_json
from workspace.custom_tools.path import LOCAL_JSON_PATH
from peewee import MySQLDatabase, Model, CharField, DateTimeField, IntegerField, BooleanField

_dict = load_json(LOCAL_JSON_PATH)
db = MySQLDatabase(_dict["database"], user=_dict["username"], password=_dict["password"],
                   host=_dict["host"], port=int(_dict["port"]))

max_nums = _dict["max_nums"]
begin_time = datetime.datetime.strptime(_dict["begin_time"], '%Y-%m-%d')
Top_blogger_num = _dict["Top_blogger_num"]
blogger_video_num = _dict["blogger_video_num"]
filter_store_num = _dict["filter_store_num"]


# 根据得分进行一次过滤
def fetch_data_by_q(loader, q, max_nums, publishedAfter):
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
    response = loader.search_by_q(q=q, maxResults=max_nums, publishedAfter=publishedAfter)
    items = response["items"]

    # 根据输入内容获取视频信息
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

    # 根据视频id获取视频信息
    videoIds = _data["videoId"]
    for i, videoId in enumerate(videoIds):
        response = loader.videos_by_videoId(videoId)
        item = response["items"][0]
        viewCount = _data.get("viewCount")
        likeCount = _data.get("likeCount")
        commentCount = _data.get("commentCount")

        viewCount.append(item.get("statistics").get("viewCount"))
        likeCount.append(item.get("statistics").get("likeCount"))
        commentCount.append(item.get("statistics").get("commentCount"))
    return _data


def fetch_data_by_channelId(loader: YouTubeAPIOperate, channelId: str, max_nums: int):
    _data = {
        "videoId": [],
        "title": [],
        "videoUrl": [],
        "description": [],
        "channelId": [],
        "publishTime": []
    }
    response = loader.search_by_channelId(channelId=channelId, maxResults=max_nums)
    items = response["items"]

    # 根据输入内容获取视频信息
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
    return _data


# 获取视频ids的各个信息
def fetch_data_by_videoId(loader: YouTubeAPIOperate, videoIds: List[str]):
    _data = {
        "videoId": [],
        "viewCount": [],
        "likeCount": [],
        "commentCount": []
    }
    for i, videoId in enumerate(videoIds):
        response = loader.videos_by_videoId(videoId)
        item = response["items"][0]
        videoIds = _data.get("videoId")
        viewCount = _data.get("viewCount")
        likeCount = _data.get("likeCount")
        commentCount = _data.get("commentCount")

        videoIds.append(videoId)
        viewCount.append(item.get("statistics").get("viewCount"))
        likeCount.append(item.get("statistics").get("likeCount"))
        commentCount.append(item.get("statistics").get("commentCount"))
    return _data


# 获取视频的所有信息
def fetch_data_all(loader: YouTubeAPIOperate, channelId: str, max_nums: int, publishedAfter: datetime, **kwargs):
    publishedAfter = publishedAfter.isoformat() + "Z" if publishedAfter else None
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
    response = loader.search_by_channelId(channelId=channelId, maxResults=max_nums, publishedAfter=publishedAfter,
                                          **kwargs)
    items = response["items"]
    # 根据输入内容获取视频信息
    for item in items:
        videoId = _data.get("videoId")
        title = _data.get("title")
        videoUrl = _data.get("videoUrl")
        description = _data.get("description")
        channelId = _data.get("channelId")
        publishTime = _data.get("publishTime")

        videoId.append(item.get("id").get("videoId"))

        title.append(item["snippet"]["title"])
        videoUrl.append(f'https://www.youtube.com/watch?v={item.get("id").get("videoId")}')
        description.append(item["snippet"]["description"])
        channelId.append(item["snippet"]["channelId"])
        publishTime.append(item["snippet"]["publishedAt"])

    videoIds = _data.get("videoId")
    for i, videoId in enumerate(videoIds):
        viewCount = _data.get("viewCount")
        likeCount = _data.get("likeCount")
        commentCount = _data.get("commentCount")
        if videoId is not None:
            response = loader.videos_by_videoId(videoId=videoId)
            item = response["items"][0]
            viewCount.append(item.get("statistics").get("viewCount"))
            likeCount.append(item.get("statistics").get("likeCount"))
            commentCount.append(item.get("statistics").get("commentCount"))
        else:
            viewCount.append("")
            likeCount.append("")
            commentCount.append("")
    return _data


def filter_blogger(loader: YouTubeAPIOperate, channelIds: List[str], TopN: int) -> list:
    """
    根据频道id，过滤出前TopN个大v博主
    :param loader:
    :param channelIds:
    :param TopN:
    :return:
    """
    _data = {
        "channelId": [],
        "subscriberCount": []
    }
    subscriberCounts = _data.get("subscriberCount")
    channel_list = _data.get("channelId")
    for channelId in channelIds:
        response = loader.channel_by_channelId(channelId)
        item = response.get("items")[0]
        subscriberCount = item.get("statistics").get("subscriberCount")
        subscriberCounts.append(subscriberCount)
        channel_list.append(channelId)
    tuples_list = [(_data["channelId"][i], _data["subscriberCount"][i]) for i in range(len(_data["channelId"]))]
    sorted_list = sorted(tuples_list, key=lambda x: x[1], reverse=True)
    top_n_tuples = sorted_list[:TopN]
    top_n_channel_ids = [x[0] for x in top_n_tuples]
    return top_n_channel_ids


def already_subscriptions(loader: YouTubeAPIOperate) -> List[str]:
    response = loader.list_subscriptions_by_mine()
    items = response.get("items")
    channelId = []
    for item in items:
        channelId.append(item.get("snippet").get("resourceId").get("channelId"))
    return channelId


def merge_dicts(dict1: dict, dict2: dict):
    """字典拼接"""
    dict3 = {}
    for key in dict1.keys():
        dict3[key] = dict1[key] + dict2[key]
    return dict3


def filter_data(data: dict, N: int) -> Tuple[dict, dict]:
    df = pd.DataFrame(data)
    # 根据id列去除重复的行
    df = df.drop_duplicates(subset='videoId')
    df.replace('', np.nan, inplace=True)
    df = df.fillna(0)

    # 标准化DataFrame
    min_max_scaler = preprocessing.MinMaxScaler()
    df_scaled = min_max_scaler.fit_transform(df.iloc[:, 6:])
    # 计算每个属性的权重
    epsilon = 1e-8  # 定义一个小偏移量
    entropy = -np.sum(df_scaled * np.log(df_scaled + epsilon), axis=0)
    weights = (1 - entropy) / np.sum(1 - entropy)
    # 计算每个样本的得分
    ideal_best = np.max(df_scaled, axis=0)
    ideal_worst = np.min(df_scaled, axis=0)
    distance_best = np.sqrt(np.sum(weights * (df_scaled - ideal_best) ** 2, axis=1))
    distance_worst = np.sqrt(np.sum(weights * (df_scaled - ideal_worst) ** 2, axis=1))
    score = distance_worst / (distance_worst + distance_best)

    # 将得分添加到DataFrame中
    df['score'] = score

    # 根据age和salary列进行降序排列
    df = df.sort_values(by=['score'], ascending=False)
    df1 = df[:N]  # 筛选推送
    df2 = df[N:]  # 不推送
    return df1.to_dict("list"), df2.to_dict("list")


# 创建ORM模型
class Video(Model):
    video_id = CharField(unique=True)
    title = CharField(null=True)
    video_url = CharField(null=True)
    description = CharField(null=True)
    channel_id = CharField(null=True)
    publish_time = DateTimeField(null=True)
    view_count = IntegerField(null=True)
    like_count = IntegerField(null=True)
    comment_count = IntegerField(null=True)
    write_time = DateTimeField()
    flag = BooleanField(default=True)
    record = BooleanField(default=False)

    class Meta:
        database = db


def write_database(data: dict, flag: bool):
    unique_video_ids = set(data['videoId'])  # 去重
    db.connect()
    db.create_tables([Video])
    existing_video_ids = set([row[0] for row in Video.select(Video.video_id).tuples()])
    new_video_ids = unique_video_ids - existing_video_ids
    # 将数据写入MySQL数据库
    try:
        for i in range(len(data['videoId'])):
            if data['videoId'][i] in new_video_ids:
                Video.create(video_id=data['videoId'][i],
                             title=data['title'][i],
                             video_url=data['videoUrl'][i],
                             description=data['description'][i],
                             channel_id=data['channelId'][i],
                             publish_time=data['publishTime'][i],
                             view_count=data['viewCount'][i],
                             like_count=data['likeCount'][i],
                             comment_count=data['commentCount'][i],
                             write_time=datetime.datetime.now().date(),
                             flag=flag,
                             record=False)
    except Exception as e:
        print(e)
    finally:
        db.close()


class CustomSchema(BaseModel):
    q: str = Field(
        ...,
        description=("Video name searched by the user")
    )


class YouTubeCustom(YouTubeBaseTool):
    name: str = "youtube_custom"
    description: str = (
        "Use this tool to save youtube videos of interest in the database "
    )
    args_schema: Type[CustomSchema] = CustomSchema

    def _run(
            self,
            q: str
    ):
        data = {
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
        loader = YouTubeAPIOperate()
        # # 根据得分进行一次过滤，获取主动搜索的视频信息
        new_data = fetch_data_by_q(loader, q, max_nums, begin_time)
        data = merge_dicts(data, new_data)
        # 从视频中筛选N个粉丝多的博主
        channelIds = data.get("channelId")
        Top_channelIds = filter_blogger(loader, channelIds=channelIds, TopN=Top_blogger_num)
        # 删除所有关注的博主
        loader.delete_all_subscriptions()
        # 关注新博主
        for channelId in Top_channelIds:
            print(f"{channelId}关注成功")
            loader.insert_subscriptions_by_channelId(channelId=channelId)

        # 加载博主视频信息
        for channelId in Top_channelIds:
            _data = fetch_data_all(loader, channelId=channelId, max_nums=blogger_video_num, publishedAfter=begin_time,
                                   q=q,
                                   order="relevance")
            data = merge_dicts(data, _data)

        # 对data数据进行筛选过滤
        data1, data2 = filter_data(data, filter_store_num)
        # 写入数据库
        write_database(data1, flag=True)
        write_database(data2, flag=False)
        return "The task is complete and saved to the database"

    async def _arun(
            self,
            channelId: str,
    ) -> str:
        raise NotImplementedError(f"The tool {self.name} does not support async yet.")



