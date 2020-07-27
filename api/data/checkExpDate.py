import schedule
import time
import json
from datetime import datetime

def findLastFrozenID():
    retval = 0
    with open("api/data/frozenPacks.json", "r") as packs:
        frozen = json.load(packs)
    for packID in frozen.keys():
        retval = int(packID)

    return retval+1

def check():
    inFreeze = []
    moved = False
    now = datetime.today().date()
    today = now.strftime("%d-%m-%Y")
    d = int(today.split("-")[0])
    m = int(today.split("-")[1])
    y = int(today.split("-")[2])
    print("Checking refrigerators for nearly-expired (30day+) packs...")
    with open("api/data/cooledPacks.json", "r") as packs:
        cooled = json.load(packs)

    with open("api/data/frozenPacks.json", "r") as packs:
        frozen = json.load(packs)

    with open("api/data/counts.json", "r") as packs:
        counts = json.load(packs)
        
    for packID, pack in cooled.items():
        al = pack["added_on"].split("-")
        d = int(al[0])
        m = int(al[1])
        y = int(al[2])
        added = datetime(day=d, month=m, year=y).date()
        if (now-added).days >= 30:
            moved = True
            inFreeze.append((packID, pack))
            counts["cooled"][pack["type"]] -= 1
            counts["frozen"][pack["type"]] += 1

    if moved:
        for pack in inFreeze:
            del cooled[pack[0]]
            movedPack = {
                "type": pack[1]["type"],
                "added_on": pack[1]["added_on"],
                "frozen_on": today
            }
            frozen[findLastFrozenID()] = movedPack
        print("Moved these packs to freezer:")
        for i in inFreeze:
            print(i[0])
    else:
        print("No packs were moved today.")

    with open("api/data/cooledPacks.json", "w") as packs:
        json.dump(cooled, packs)

    with open("api/data/frozenPacks.json", "w") as packs:
        json.dump(frozen, packs)

    with open("api/data/counts.json", "w") as packs:
        json.dump(counts, packs)

def run(name):
    schedule.every().day.at("02:00").do(check)

    #run on first launch of software to calibrate the bank
    check()
    
    #set the script to run every day at 2am
    while True:
        schedule.run_pending()
