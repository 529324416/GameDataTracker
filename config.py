import json


class GameDataTrackerConfig:

    @staticmethod
    def load(filepath:str) -> object:

        try:
            with open(filepath, "r", encoding='utf-8') as f:
                source = f.read()
            dblink = source["dblink"]
            return GameDataTrackerConfig(dblink)
        except Exception as e:
            return None
        
    def __init__(self, dblink:str) -> None:
        
        self.__dblink = dblink

    @property
    def dblink(self) -> str:
        '''the url of mongodb'''

        return self.__dblink