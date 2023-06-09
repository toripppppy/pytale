# Pytale

## Overview
This library makes it easy to create tales that are told on the console.

コンソール上で遊べるゲームを作る時に使える会話ライブラリです。

## Usage 1
python only
```python
import pytale

ps = pytale.Scenario()
ps.read("Hi.", sleep=1.5, speaker="King")
player_name = ps.input("What your name?")
hero_flag = ps.confirm(f"ok {player_name}, You wanna be a hero?")

if hero_flag:
    ps.read("Yes.", sleep=1.5, speaker=player_name)
    ps.read("\n-GAME CLEAR-")
else:
    ps.read("\n-GAME OVER-")
```
console
```
[King]
Hi.
What's your name?
: hoge

ok hoge, You wanna be a hero?
choices: ['y', 'n']
: y

[hoge]
Yes.

-GAME CLEAR-
```
## Usage 2
with json
```json
{
    "setting": {},
    "scenario": {
        "intro": [
            {
                "speaker": "King",
                "text": "Hi.",
                "sleep": 1.5
            },
            {
                "type": "input",
                "text": "What's your name?",
                "var_name": "player_name"
            },
            {
                "type": "select",
                "text": "ok {player_name}, You wanna be a hero?",
                "choices": ["y", "n"],
                "var_name": "hero_flag"
            },
            {
                "type": "link",
                "ref": "hero_flag",
                "to": {
                    "y": "yes",
                    "n": "no"
                }
            }
        ],
        "yes": [
            {
                "speaker": "{player_name}",
                "text": "Yes.",
                "sleep": 1.5
            },
            {
                "text": "\n-GAME CLEAR-"
            }
        ],
        "no": [
            {
                "text": "\n-GAME OVER-"
            }
        ]
    }
}
```
```python
import pytale

ps = pytale.Scenario("path/to/xxxxx.json")

ps.read_chapter("intro")
```
console
```
[King]
Hi.
What's your name?
: hoge

ok hoge, You wanna be a hero?
choices: ['y', 'n']
: y

[hoge]
Yes.

-GAME CLEAR-
```

## Methods
coming soon ...

## version
0.1.3 (Beta)

## Github
https://github.com/toripppppy/pytale