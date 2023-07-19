import json
import os
import shutil
from typing import Any


def load_json(file_path: str) -> dict:
    """
    读取JSON文件并返回解析后的Python对象
    """
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding="UTF-8") as f:
            data = json.load(f)
        return data
    else:
        return {}


def save_json(data: dict, file_path: str) -> None:
    """
    将Python对象转换为JSON格式并保存到指定文件
    """
    with open(file_path, 'w', encoding="UTF-8") as f:
        json.dump(data, f, indent=4)


def get_value(data: dict, key_path: list) -> dict:
    """
    获取嵌套在JSON中的值
    key_path: 由字符串组成的列表，表示嵌套的键的路径。例如，["person", "name"]表示data["person"]["name"]。
    """
    for key in key_path:
        data = data.get(key, {})
    return data


def set_value(data: dict, key_path: list, value: Any) -> None:
    """
    设置嵌套在JSON中的值
    key_path: 由字符串组成的列表，表示嵌套的键的路径。例如，["person", "name"]表示data["person"]["name"]。
    """
    for key in key_path[:-1]:
        data = data.setdefault(key, {})
    data[key_path[-1]] = value


def append_dict_to_json(dict_obj: dict, json_file_path: str) -> bool:
    with open(json_file_path, 'r+') as file:
        # 加载JSON文件中的数据
        data = json.load(file)

        # 追加字典到数据列表中
        data.update(dict_obj)

        # 将更新后的数据写回JSON文件
        file.seek(0)  # 将文件指针移动到文件开头
        json.dump(data, file, indent=4)
        file.truncate()  # 清空文件剩余部分
    return True


def copy_json_file(src_path: str, dest_path: str) -> bool:
    """
    :param src_path:要复制的JSON文件的源路径。
    :param dest_path:复制后的JSON文件的目标路径。
    :return:
    """
    shutil.copy(src_path, dest_path)
    return True


def get_json_value(json_file_path: str, key: str) -> Any:
    """
    获取json文件中某个key的值
    :param json_file_path: 要读取的JSON文件的路径。
    :param key: 要获取值的JSON对象中的键。
    :return:
    """
    with open(json_file_path) as file:
        data = json.load(file)
        return data[key]
