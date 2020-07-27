import json
from datetime import datetime
from random import randint

def findLastFrozenID(frozen):
    retval = 0
    for packID in frozen.keys():
        retval = int(packID)

    return retval+1

def findLastCooledID(cooled):
    retval = 0
    for packID in cooled.keys():
        retval = int(packID)

    return retval+1

def populate():
    #Get existing data
    with open("api/data/cooledPacks.json", "r") as packs:
        cooled = json.load(packs)

    with open("api/data/frozenPacks.json", "r") as packs:
        frozen = json.load(packs)

    with open("api/data/counts.json", "r") as packs:
        counts = json.load(packs)

    #Populate files
    cooled = {}
    frozen = {}
    counts = {
        "cooled": {
            "A+": randint(10,60),
            "O+": randint(10,60),
            "B+": randint(10,60),
            "AB+": randint(10,60),
            "A-": randint(10,60),
            "O-": randint(10,60),
            "B-": randint(10,60),
            "AB-": randint(10,60)
        },
        "frozen": {
            "A+": randint(10,60),
            "O+": randint(10,60),
            "B+": randint(10,60),
            "AB+": randint(10,60),
            "A-": randint(10,60),
            "O-": randint(10,60),
            "B-": randint(10,60),
            "AB-": randint(10,60)
        }
    }

    for typ, cnt in counts["cooled"].items():
        for i in range(cnt):
            addDate = datetime(day=randint(10,25), month=7, year=2020).date().strftime("%d-%m-%Y")
            cooled[findLastCooledID(cooled)] = {
                "type": typ,
                "added_on": addDate
            }

    for typ, cnt in counts["frozen"].items():
        for i in range(cnt):
            addDate = datetime(day=randint(1,25), month=randint(1,6), year=2020).date().strftime("%d-%m-%Y")
            freezeDate = datetime(day=int(addDate.split("-")[0]), month=int(addDate.split("-")[1])+1, year=2020).date().strftime("%d-%m-%Y")
            frozen[findLastFrozenID(frozen)] = {
                "type": typ,
                "added_on": addDate,
                "frozen_on": freezeDate
            }

    #Dump data back
    with open("api/data/cooledPacks.json", "w") as packs:
        json.dump(cooled, packs)

    with open("api/data/frozenPacks.json", "w") as packs:
        json.dump(frozen, packs)

    with open("api/data/counts.json", "w") as packs:
        json.dump(counts, packs)

def setEmpty():
    #Get existing data
    with open("api/data/cooledPacks.json", "r") as packs:
        cooled = json.load(packs)

    with open("api/data/frozenPacks.json", "r") as packs:
        frozen = json.load(packs)

    with open("api/data/counts.json", "r") as packs:
        counts = json.load(packs)

    #Populate files
    cooled = {}
    frozen = {}
    counts = {
        "cooled": {
            "A+": 0,
            "O+": 0,
            "B+": 0,
            "AB+": 0,
            "A-": 0,
            "O-": 0,
            "B-": 0,
            "AB-": 0
        },
        "frozen": {
            "A+": 0,
            "O+": 0,
            "B+": 0,
            "AB+": 0,
            "A-": 0,
            "O-": 0,
            "B-": 0,
            "AB-": 0
        }
    }
    #Dump data back
    with open("api/data/cooledPacks.json", "w") as packs:
        json.dump(cooled, packs)

    with open("api/data/frozenPacks.json", "w") as packs:
        json.dump(frozen, packs)

    with open("api/data/counts.json", "w") as packs:
        json.dump(counts, packs)