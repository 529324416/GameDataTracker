import queue
import time
import logging
import threading
from pymongo import MongoClient

class GameDataTrackerUploader:

    def __init__(self, client: MongoClient, logger: logging.Logger):
        self.client = client
        self.queue = queue.Queue()
        self.time = time.time()
        self.logger = logger
        self.__is_uploading = False

    def upload_guide_mission_data(self, version, missionId, start_day, end_day) -> bool:
        '''upload guide mission receive and complete time'''

        self.queue.put({
            "type":"guide_mission",
            "data":(version, missionId, start_day, end_day)
        })
        if time.time() - self.time > 10:
            self.time = time.time()
            self._upload()
    
    def upload_check(self):
        '''upload check data'''

        if time.time() - self.time > 10:
            self.time = time.time()
            self._upload()

    def _upload(self):
        '''run a thread to do upload'''

        if self.__is_uploading:
            logging.warning("waiting for last upload mission finished")
            return
        self.__is_uploading = True
        thread = threading.Thread(target=self.__upload_thread)
        thread.start()

    def __upload_thread(self, datas: iter) -> None:
        '''upload data to mongodb'''

        organizal_datas = {}
        for data in datas:
            typeName = data["type"]
            if typeName not in organizal_datas:
                organizal_datas[typeName] = []
            
            _data = self.__convert_data(typeName, data["data"])
            if _data != None:
                organizal_datas[typeName].append(_data)
            
        
        database = self.client["game_data_tracker"]
        for typeName, datas in organizal_datas.items():
            try:
                col = database[typeName]
                col.insert_many(datas)
            except Exception as e:
                # print(f"insert data failed: {e}")
                logging.error("insert data failed: %s", e)
                continue
        self.__is_uploading = False

    def __convert_data(self, typeName:str, data:tuple) -> dict:
        '''upload mission guide data'''

        if typeName == "guide_mission":
            try:
                version, missionId, start_day, end_day = data
                return {
                    "version":version,
                    "missionId":missionId,
                    "start_day":start_day,
                    "end_day":end_day
                }
            except Exception as e:
                # print(f"convert data failed: {e}")
                logging.error("convert data (%s, %s, %i, %i) failed: %s", version, missionId, start_day, end_day, e)
                return None
        return None



        

def create_data_uploader(dblink:str, logger:logging.Logger) -> GameDataTrackerUploader:
    '''create a new GameDataTracker from given PyMongo link'''

    try:
        client = MongoClient(dblink)
        return GameDataTrackerUploader(client, logger)
    except Exception as e:
        return None