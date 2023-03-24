import os
import json
from collections import OrderedDict

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
    

    def get_filepath(self) -> None:
        return self.filepath
    
    
    # jsonを取得
    def get_json(self) -> object:
        with open(self.filepath) as f:
            # 要素の順番を崩さずに読み込み
            di = json.load(f, object_pairs_hook=OrderedDict)
            return di
        
    # jsonを更新
    def dump_json(self, di) -> None:
        with open(self.filepath, 'w') as f:
            json.dump(di, f, indent=4, ensure_ascii=False)