import pytale

s = pytale.Scenario('tests/scenario.json')
print(s.get_json())
s.dump_json({"a":['a','b','c']})