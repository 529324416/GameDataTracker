import json


class GameDataTrackerConfig:
        
    def __init__(self, dblink:str, server_host:str, server_port:int) -> None:
        
        self.__server_address = (server_host, server_port)
        self.__dblink = dblink

    @property
    def dblink(self) -> str:
        '''the url of mongodb'''

        return self.__dblink
    
    @property
    def server_address(self) -> tuple:
        return self.__server_address
    

def load_tracker_config(filepath:str) -> GameDataTrackerConfig:

    try:
        with open(filepath, "r", encoding='utf-8') as f:
            source = json.load(f)
        dblink = source["dblink"]
        server_host = source["server_host"]
        server_port = source["server_port"]
        return GameDataTrackerConfig(dblink, server_host, server_port)
    except Exception as e:
        print("error occurs when load config:")
        print(e)
        return None