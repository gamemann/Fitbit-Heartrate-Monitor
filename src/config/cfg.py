import json

def loadCFG(path: str) -> tuple:
    cfg = {}

    # Open config file
    with open(path) as file:
        cfg = json.load(file)

    # Set defaults.
    if "Debug" not in cfg:
        cfg["Debug"] = 0
    
    if "Authorization" not in cfg:
        cfg["Authorization"] = ""

    if "UserID" not in cfg:
        cfg["UserID"] = "-" 

    if "LowThreshold" not in cfg:
        cfg["LowThreshold"] = 50

    if "HighThreshold" not in cfg:
        cfg["HighThreshold"] = 120

    if "AvgCount" not in cfg:
        cfg["AvgCount"] = 10

    if "Actions" not in cfg:
        cfg["Actions"] = []

    return cfg
