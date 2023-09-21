from pymongo import MongoClient

class GameDataTrackerUploader:

    def __init__(self, client: MongoClient):
        self.client = client

    def upload_guide_mission_data(self, version, missionId, start_day, end_day) -> bool:
        '''upload guide mission receive and complete time'''

        try:
            database = self.client.get_database("data_tracker")
            collection = database.get_collection("guide_mission")
            collection.insert_one({
                "version":version,
                "missionId":missionId,
                "day_start":start_day,
                "day_finish":end_day
            })
            return True
        except Exception as e:
            return False
        

def create_data_uploader(dblink:str) -> GameDataTrackerUploader:
    '''create a new GameDataTracker from given PyMongo link'''

    try:
        client = MongoClient(dblink)
        return GameDataTrackerUploader(client)
    except Exception as e:
        return None