# 埋点数据收集系统|GameDataTracker
# 收集游戏中产生的各类游戏数据
# NOTE @2023.09.21 目前只收集引导任务数据

import flask
from flask import Flask
from gevent import monkey, pywsgi
monkey.patch_all()

import config
import data
import logSystem

app = Flask(__name__)
data_uploader = None

def failed(message:str) -> str:
    return flask.jsonify({
        "result":0,
        "msg":message,
    }), 400

def success():
    return flask.jsonify({
        "result":1
    }), 200


@app.route("/upload/missionGuide/<version>/<missionId>/", methods = ["GET", "POST"])
def upload_guide_mission_data(version:str, missionId:str) -> str:
    '''引导任务数据上传接口
    @version: 当前上传的游戏版本
    @missionId: 上传的任务Id'''

    req = flask.request
    if req.method != "POST":
        return failed("route should access by 'post'")
    
    if not req.is_json:
        return failed("post current route with json data")
    
    client_data = req.get_json()
    if client_data is None:
        return failed("failed to load json data")

    day_receive = None
    day_finish = None
    day_receive = client_data.get("rd")
    day_finish = client_data.get("fd")

    if not isinstance(day_receive, int):
        return failed("'rd' should be int type")
    if not isinstance(day_finish, int):
        return failed("'fd' should be int type")

    data_uploader.upload_guide_mission_data(version, missionId, day_receive, day_finish)
    return success()


def main(config_path:str) -> None:
    '''run application'''

    data_tracker_cfg = config.load_tracker_config(config_path)
    if data_tracker_cfg is None:
        print("config file missing..")
        print("app run failed..")
        return
    
    logger = logSystem.create_logger("./tracker.log")
    if logger is None:
        print("create logger system failed")
        print("app run failed..")
        return
    
    global data_uploader
    data_uploader = data.create_data_uploader(data_tracker_cfg.dblink, logger)
    if data_uploader is None:
        print("connect to mongodb failed..")
        return
    
    print(f"run app at {data_tracker_cfg.server_link}")
    server = pywsgi.WSGIServer(data_tracker_cfg.server_address, app)
    server.serve_forever()


if __name__ == '__main__':
    main("./config.json")