import os

class Scenario:

    def __init__(self, filepath: str) -> None:
        '''
        filepath: "path/to/xxxxx.json"
        '''
        # パスにファイルが存在するか
        if not os.path.exists(filepath):
            raise FileNotFoundError(f'"{filepath}" does not exist.')
        
        # jsonファイルかどうか
        if os.path.splitext(filepath)[1] != '.json':
            raise ValueError(f'"{filepath}" is not a JSON file.')
        
        self.filepath = filepath
    

    def get_filepath(self):
        return self.filepath