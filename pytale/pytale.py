import os
import json
import time
from collections import OrderedDict


class Scenario:

    def __init__(self, filepath = None, reset_setting = True) -> None:
        '''
        filepath: "path/to/xxxxx.json"
        '''
        if filepath != None:
            # パスにファイルが存在するか
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"'{filepath}' does not exist.")
            
            # jsonファイルかどうか
            if os.path.splitext(filepath)[1] != ".json":
                raise ValueError(f"'{filepath}' is not a JSON file.")
        
        self.filepath = filepath

        # 話者保存用
        self.current_speaker = ""

        # 設定のリセット（デフォルトではTrue）
        if reset_setting and filepath != None:
            self.reset_setting()
    

    ### CRUD関連
    def get_filepath(self) -> str:
        filepath = self.filepath
        if filepath is None:
            raise TypeError("No JSON file specified")

        return self.filepath
    
    
    def get_json(self) -> dict[str, dict]:
        filepath = self.get_filepath()
        with open(filepath) as f:
            # 要素の順番を崩さずに読み込み
            di = json.load(f, object_pairs_hook=OrderedDict)
            return di
        

    def dump_json(self, di: dict) -> None:
        filepath = self.get_filepath()
        with open(filepath, "w") as f:
            json.dump(di, f, indent=4, ensure_ascii=False)


    # TODO setting関連
    def get_setting(self, key = None) -> any:
        try:
            setting = self.get_json()["setting"]
        except KeyError:
            raise KeyError(f"'setting' expected but not found in '{self.get_filepath()}'")

        # キーが指定されていない場合はsettingを返す
        return setting.get(key) if key is not None else setting
    

    def dump_setting(self, setting: dict) -> None:
        di = self.get_json()
        di["setting"] = setting
        self.dump_json(di)


    def set_setting(self, key: str, value) -> None:
        # settingに値を挿入
        setting = self.get_setting()
        setting[key] = value
        self.dump_setting(setting)


    def reset_setting(self) -> None:
        self.dump_setting({})


    def get_chapter(self, chapter_name: str) -> list[dict]:
        di = self.get_json()
        scenario = di.get("scenario")
        if scenario is None:
            raise ValueError(f"'scenario' expected but not found in '{self.get_filepath()}'")

        chapter = scenario.get(chapter_name)
        if chapter is None:
            raise ValueError(f"chapter name '{chapter_name}' not found in '{self.get_filepath()}'")
        
        return chapter


    ### 主要メソッド
    def read(self, text: str, sleep = 0.0, speaker = None) -> None:
        '''
        Parameters
        ----------
        text: str
            表示するテキスト\n
        sleep: float
            次に進むまでの待機時間（省略可）\n
        speaker: str
            表示する話者名。textの頭に[名前]のように表示されます（省略可）
        '''
        # 話者を表示
        if speaker is not None:
            if speaker != self.current_speaker:
                self.current_speaker = speaker
                print("[" + speaker + "]", end="\n")

        # 文章を表示
        if type(text) is str:
            print(text)
        else:
            raise TypeError("'text' must be str")

        time.sleep(sleep)


    def input(self, text = None) -> str:
        '''
        Parameters
        ----------
        text: str
            回答待機時に表示するテキスト（省略可）\n
        '''
        if text != None:
            self.read(text)

        while True:
            answer = input(": ")
            # 回答なしは無効
            if answer != "": break

        print()
        return answer
    

    def select(self, text: str, choices = None) -> str:
        '''
        Parameters
        ----------
        text: str
            回答待機時に表示するテキスト（省略可）\n
        choices: list
            選べる選択肢のリスト。str型のlist。
        '''
        if text != None:
            self.read(text)

        if choices is not None:
            print(f"choices: {choices}")

        while True:
            answer = input(": ")

            # 回答が選択肢に含まれているかを確認
            if answer in choices:
                break
            
            # else
            print("try again.")

        print()
        return answer
    

    def confirm(self, text: str, yes = "y", no = "n") -> bool:
        '''
        Parameters
        ----------
        text: str
            回答待機時に表示するテキスト（省略可）\n
        '''
        answer = self.select(text, [yes, no])

        return True if answer == yes else False

    
    def link(self, to: str | dict, ref = None) -> None:
        '''
        Parameters
        ----------
        ref: str
            リンク先を先を分岐させる際に参考にするsetting変数\n
        to: str | dict
            リンク先。refを使用する場合はdict型で{"refの値": "リンク先"}のように指定
        '''
        if ref is not None:
            if type(to) is not dict and type(to) is not OrderedDict:
                raise TypeError("'to' must be dict if using 'ref'")
            
            ref_value = self.get_setting(ref)

            for k, v in to.items():
                if k == ref_value:
                    self.read_chapter(v)
                    return
            
            raise ValueError(f"'{ref_value}' not found in 'to'")
            
        else:
            if type(to) is not str:
                raise TypeError("'to' must be str")
            
            self.read_chapter(to)
    

    def replace_vars(self, text: str) -> str:
        setting = self.get_setting()
        for k, v in setting.items():
            text = text.replace("{" + k + "}", v)

        return text


    # チャプターを読み上げ
    def read_chapter(self, chapter_name: str) -> None:
        '''
        Parameters
        ----------
        chapter_name: str
            読み上げるチャプター名
        '''

        chapter = self.get_chapter(chapter_name)
        current_speaker = None

        def raise_missing_argument_error(scenario_type: str, missing_arguments : list[str]):
            l = len(missing_arguments)
            if l > 0:
                raise TypeError(f"Scenario type '{scenario_type}' missing {l} required argument: '{','.join(missing_arguments)}'")


        def _read(data: dict):
            missing_arguments = []
            
            speaker = data.get("speaker")

            text = data.get("text")
            if text is None:
                missing_arguments.append("text")
            
            sleep = data.get("sleep")
            if sleep is None:
                sleep = 0

            raise_missing_argument_error("read", missing_arguments)

            text = self.replace_vars(text)

            self.read(text, sleep, speaker)


        def _input(data: dict):
            # selectはinputの派生形として処理
            missing_arguments = []

            text = data.get("text")
            if text is None:
                missing_arguments.append("text")

            var_name = data.get("var_name")
            if var_name is None:
                missing_arguments.append("var_name")

            choices = data.get("choices")

            raise_missing_argument_error("input", missing_arguments)
            
            if choices is None:
                answer = self.input(text)
            else:
                answer = self.select(text, choices)

            self.set_setting(var_name, answer)


        def _select(data: dict):
            _input(data)


        def _link(data: dict):
            ref = data.get("ref")

            to = data.get("to")
            if to is None:
                raise_missing_argument_error("link", ["to"])

            self.link(to, ref)


        for c in chapter:
            c_type = c.get("type")

            if c_type == "input":
                _input(c)
            elif c_type == "select":
                _select(c)
            elif c_type == "link":
                _link(c)
            else:
                _read(c)
