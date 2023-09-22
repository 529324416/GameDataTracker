# 埋点数据收集系统|GameDataTracker
# 收集游戏中产生的各类游戏数据
# NOTE @2023.09.21 目前只收集引导任务数据

import flask
from flask import Flask
from gevent import monkey, pywsgi
monkey.patch_all()

import config
import data

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


@app.route("/upload/missionGuide/<version>/<missionId>/", methods = ["POST"])
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

    result = data_uploader.upload_guide_mission_data(version, missionId, day_receive, day_finish)
    if result:
        return success()
    return failed("failed to insert data")

if __name__ == '__main__':

    filepath = "./config.json"
    data_tracker_cfg = config.load_tracker_config(filepath)
    if data_tracker_cfg is None:
        print("app run failed..")
        print("config file missing..")
    else:
        data_uploader = data.create_data_uploader(data_tracker_cfg.dblink)
        if data_uploader is None:
            print("app run failed..")
            print("connect to mongodb failed..")
        else:
            server = pywsgi.WSGIServer(data_tracker_cfg.server_address, app)
            print(f"start to run app on {data_tracker_cfg.server_address}")
            server.serve_forever()