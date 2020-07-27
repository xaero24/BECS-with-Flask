import json
from datetime import datetime

class BECS:
    possibleDonors = {
        'A+': ['A+', 'A-', 'O+', 'O-'],
        'O+': ['O+', 'O-'],
        'B+': ['B+', 'B-', 'O+', 'O-'],
        'AB+': ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-'],
        'A-': ['A-', 'O-'],
        'O-': ['O-'],
        'B-': ['B-', 'O-'],
        'AB-': ['O-', 'A-', 'B-', 'AB-']
    }

    bloodTypeDistribution = {
        'A+': 34,
        'O+': 32,
        'B+': 17,
        'AB+': 7,
        'A-': 4,
        'O-': 3,
        'B-': 2,
        'AB-': 1
    }

    def findLastFrozenID(self, frozen):
        retval = 0
        for packID in frozen.keys():
            retval = int(packID)
        return retval+1

    def findLastCooledID(self, cooled):
        retval = 0
        for packID in cooled.keys():
            retval = int(packID)
        return retval+1

    def getMostSuitableDonorsFromFrozen(self):
        suitability = []
        with open("api/data/counts.json", "r") as counts:
            data = json.load(counts)
        
        for i in range(8):
            bTypes = [x for x in self.bloodTypeDistribution.keys()]
            bCounts = [x for x in data["frozen"].values()]
            distributions = [x for x in self.bloodTypeDistribution.values()]

            suitability.append((
                bTypes[i],
                distributions[i] * bCounts[i]
                ))

        suitability = sorted(suitability, key=lambda x:x[1], reverse=True)
        return suitability

    def getMostSuitableDonorsFromCooled(self):
        suitability = []
        with open("api/data/counts.json", "r") as counts:
            data = json.load(counts)
        
        for i in range(8):
            bTypes = [x for x in self.bloodTypeDistribution.keys()]
            bCounts = [x for x in data["cooled"].values()]
            distributions = [x for x in self.bloodTypeDistribution.values()]

            suitability.append((
                bTypes[i],
                distributions[i] * bCounts[i]
                ))

        suitability = sorted(suitability, key=lambda x:x[1], reverse=True)
        return suitability

    def addNewPortion(self, bloodType):
        with open("api/data/counts.json", "r") as counts:
            cnts = json.load(counts)
        with open("api/data/cooledPacks.json", "r") as cooled:
            cld = json.load(cooled)
        
        cnts["cooled"][bloodType] += 1
        cld[self.findLastCooledID(cld)] = {
            "type": bloodType,
            "added_on": datetime.today().date().strftime("%d-%m-%Y")
        }

        with open("api/data/counts.json", "w") as packs:
            json.dump(cnts, packs)
        with open("api/data/cooledPacks.json", "w") as packs:
            json.dump(cld, packs)
        
        return (bloodType, cnts["cooled"][bloodType])

    def withdrawPortion(self, bloodType, urgency):
        with open("api/data/counts.json", "r") as counts:
            cnts = json.load(counts)
        
        if urgency == "reg":
            #first check frozen
            sortedList = self.getMostSuitableDonorsFromFrozen()
            donorsList = self.possibleDonors[bloodType]
            sortedDonors = []
            for i in sortedList:
                if i[0] in donorsList:
                    sortedDonors.append(i)
            
            sortedDonors.sort(key=lambda tup: tup[1], reverse=True)
            chosenBloodType = sortedDonors[0][0]

            print("  RESULTS OF PULLING REGULAR:")
            print(sortedList)
            print(sortedDonors)
            print(chosenBloodType)

            if cnts["frozen"][chosenBloodType] > 0:
                #Remove first found pack of this blood type
                with open("api/data/frozenPacks.json", "r") as cooled:
                    frz = json.load(cooled)
                for k,v in frz.items():
                    if v["type"] == chosenBloodType:
                        del frz[k]
                        break
                with open("api/data/frozenPacks.json", "w") as packs:
                    json.dump(frz, packs)
                
                #Update pack count
                cnts["frozen"][chosenBloodType] -= 1
                with open("api/data/counts.json", "w") as packs:
                    json.dump(cnts, packs)
                return (chosenBloodType, cnts["frozen"][chosenBloodType])
            else:
                #If not found, check cooled
                sortedList = self.getMostSuitableDonorsFromCooled()
                donorsList = self.possibleDonors[bloodType]
                sortedDonors = []
                for i in sortedList:
                    if i[0] in donorsList:
                        sortedDonors.append(i)
                
                sortedDonors.sort(key=lambda tup: tup[1], reverse=True)
                chosenBloodType = sortedDonors[0][0]
                if cnts["cooled"][chosenBloodType] > 0:
                    #Remove first found pack of this blood type
                    with open("api/data/cooledPacks.json", "r") as cooled:
                        cld = json.load(cooled)
                    for k,v in cld.items():
                        if v["type"] == chosenBloodType:
                            del cld[k]
                            break
                    with open("api/data/cooledPacks.json", "w") as packs:
                        json.dump(cld, packs)
                    
                    #Update pack count
                    cnts["cooled"][chosenBloodType] -= 1
                    with open("api/data/counts.json", "w") as packs:
                        json.dump(cnts, packs)
                    return (chosenBloodType, cnts["cooled"][chosenBloodType])
                else:
                    #If not found, return a message on failed search
                    return ("None", 0)
        else:
            #first check cooled
            sortedList = self.getMostSuitableDonorsFromCooled()
            donorsList = self.possibleDonors[bloodType]
            sortedDonors = []
            for i in sortedList:
                if i[0] in donorsList:
                    sortedDonors.append(i)
            
            sortedDonors.sort(key=lambda tup: tup[1], reverse=True)
            chosenBloodType = sortedDonors[0][0]
            if cnts["cooled"][chosenBloodType] > 0:
                #Remove first found pack of this blood type
                with open("api/data/cooledPacks.json", "r") as cooled:
                    cld = json.load(cooled)
                for k,v in cld.items():
                    if v["type"] == chosenBloodType:
                        del cld[k]
                        break
                with open("api/data/cooledPacks.json", "w") as packs:
                    json.dump(cld, packs)
                
                #Update pack count
                cnts["cooled"][chosenBloodType] -= 1
                with open("api/data/counts.json", "w") as packs:
                    json.dump(cnts, packs)
                return (chosenBloodType, cnts["cooled"][chosenBloodType])
            else:
                #If not found, check frozen
                sortedList = self.getMostSuitableDonorsFromFrozen()
                donorsList = self.possibleDonors[bloodType]
                sortedDonors = []
                for i in sortedList:
                    if i[0] in donorsList:
                        sortedDonors.append(i)
                
                sortedDonors.sort(key=lambda tup: tup[1], reverse=True)
                chosenBloodType = sortedDonors[0][0]
                if cnts["frozen"][chosenBloodType] > 0:
                    #Remove first found pack of this blood type
                    with open("api/data/frozenPacks.json", "r") as cooled:
                        frz = json.load(cooled)
                    for k,v in frz.items():
                        if v["type"] == chosenBloodType:
                            del frz[k]
                            break
                    with open("api/data/frozenPacks.json", "w") as packs:
                        json.dump(frz, packs)
                    
                    #Update pack count
                    cnts["frozen"][chosenBloodType] -= 1
                    with open("api/data/counts.json", "w") as packs:
                        json.dump(cnts, packs)
                    return (chosenBloodType, cnts["frozen"][chosenBloodType])
                else:
                    #If not found, return a message on failed search
                    return ("None", 0)

    def massWithdrawal(self, amounts):
        taken = {
            'A+': 0,
            'O+': 0,
            'B+': 0,
            'AB+': 0,
            'A-': 0,
            'O-': 0,
            'B-': 0,
            'AB-': 0
        }
        unpulled = {
            'A+': amounts[0][1],
            'O+': amounts[1][1],
            'B+': amounts[2][1],
            'AB+': amounts[3][1],
            'A-': amounts[4][1],
            'O-': amounts[5][1],
            'B-': amounts[6][1],
            'AB-': amounts[7][1]
        }
        partial = "False"
        for req in amounts:
            for i in range(req[1]):
                withdrawn = (self.withdrawPortion(req[0], "emg"))[0]
                if withdrawn != "None":
                    taken[withdrawn] += 1
                    unpulled[req[0]] -= 1
        
        for v in unpulled.values():
            if v > 0:
                partial = "True"
        
        return (taken, unpulled, partial)

    def getPackCounts(self):
        cooled = []
        frozen = []
        with open("api/data/counts.json", "r") as counts:
            cnts = json.load(counts)
        for x in cnts["cooled"].values():
            cooled.append(x)
        for x in cnts["frozen"].values():
            frozen.append(x)
        res = [cooled, frozen]
        return res