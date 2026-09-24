from pyforge.tools.json_tools.core import format_json, json_statistics

source = '{"project":"PyForge","tools":["json","files"]}'
print(format_json(source))
print(json_statistics(source))
