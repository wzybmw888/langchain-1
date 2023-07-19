import os.path

ROOT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom_tools")

STATIC_DIR_PATH = os.path.join(ROOT_PATH, "static")
LOG_DIR_PATH = os.path.join(STATIC_DIR_PATH, "log")
CSS_DIR_PATH = os.path.join(STATIC_DIR_PATH, "css")

SETTING_DIR_PATH = os.path.join(ROOT_PATH, "setting")

TOKEN_PICKLE_PATH = os.path.join(STATIC_DIR_PATH, "token.pickle")

LOCAL_JSON_PATH = os.path.join(SETTING_DIR_PATH, "local.json")

CLIENT_SECRET_PATH = os.path.join(SETTING_DIR_PATH, "client_secret2.json")

YOUTUBE_LOG = os.path.join(LOG_DIR_PATH, "youtube_operate.log")

CUSTOM_CSS = os.path.join(CSS_DIR_PATH, "custom.qss")

YOUTUBE_DATA_PATH = os.path.join(SETTING_DIR_PATH, "youtube_search_data.json")

if __name__ == '__main__':
    print(LOCAL_JSON_PATH)