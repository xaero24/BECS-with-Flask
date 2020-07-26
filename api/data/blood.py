import json
from datetime import datetime

class BECS:
    packsCount = { #frozen
        'A+': 0,
        'O+': 0,
        'B+': 0,
        'AB+': 0,
        'A-': 0,
        'O-': 0,
        'B-': 0,
        'AB-': 0
    }

    cooledPacksCount = { #obviously cooled
        'A+': 0,
        'O+': 0,
        'B+': 0,
        'AB+': 0,
        'A-': 0,
        'O-': 0,
        'B-': 0,
        'AB-': 0
    }

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

    def getMostSuitableDonors(self):
        suitability = []
        for i in range(8):
            bTypes = [x for x in self.bloodTypeDistribution.keys()]
            bCounts = [x for x in self.packsCount.values()]
            distributions = [x for x in self.bloodTypeDistribution.values()]

            suitability.append((
                bTypes[i],
                distributions[i] * bCounts[i]
                ))

        return suitability
    
    def addNewPortion(self, bloodType):
        #add new pack to cooled packs, also to file
        self.packsCount[bloodType] += 1
        return (bloodType, self.packsCount[bloodType])

    def withdrawPortion(self, bloodType, urgency):
        if urgency == "reg":
            #first check frozen, then cooled
            sortedList = self.getMostSuitableDonors()
            donorsList = self.possibleDonors[bloodType]
            sortedDonors = []
            for i in sortedList:
                if i[0] in donorsList:
                    sortedDonors.append(i)
            
            sortedDonors.sort(key=lambda tup: tup[1], reverse=True)
            chosenBloodType = sortedDonors[0][0]
            if self.packsCount[chosenBloodType] > 0:
                self.packsCount[chosenBloodType] -= 1
                return (chosenBloodType, self.packsCount[chosenBloodType])
            else:
                return ("None", 0)
        else:
            pass #get cooled as priority
    
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
        for req in amounts:
            for i in range(req[1]):
                withdrawn = (self.withdrawPortion(req[0], "emg"))[0]
                if withdrawn != "None":
                    taken[withdrawn] += 1

        return taken

    def getPackCounts(self):
        res = []
        for x in self.packsCount.values():
            res.append(x)
        return res