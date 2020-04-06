from csv import reader, writer


class BECS:
    packsCount = {
        'A+': 530,
        'O+': 320,
        'B+': 308,
        'AB+': 190,
        'A-': 120,
        'O-': 80,
        'B-': 63,
        'AB-': 20
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

    givesToDict = {
        'A+': ['A+', 'AB+'],
        'O+': ['O+', 'A+', 'B+', 'AB+'],
        'B+': ['B+', 'AB+'],
        'AB+': ['AB+'],
        'A-': ['A+', 'A-', 'AB+', 'AB-'],
        'O-': ['O+', 'A+', 'B+', 'AB+', 'O-', 'A-', 'B-', 'AB-'],
        'B-': ['B+', 'B-', 'AB+', 'AB-'],
        'AB-': ['AB+', 'AB-']
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

    def checkBestBefore(this, pack):
        """
        Whole blood can be stored for 21 to 35 days in fridges, depending on the method of blood storage. We take the more strict 21 days.
        """
        pass

    def getMostSuitableDonors(this):
        suitability = []
        for i in range(8):
            bTypes = [x for x in this.bloodTypeDistribution.keys()]
            bCounts = [x for x in this.packsCount.values()]
            distributions = [x for x in this.bloodTypeDistribution.values()]

            suitability.append((
                bTypes[i],
                distributions[i] * bCounts[i]
                ))

        return suitability

    def massWithdrawal(this, amounts):
        taken = {
            'O+': 0,
            'A+': 0,
            'B+': 0,
            'AB+': 0,
            'O-': 0,
            'A-': 0,
            'B-': 0,
            'AB-': 0
        }
        for req in amounts:
            for i in range(req[1]):
                withdrawn = (this.withdrawPortion(req[0]))[0]
                if withdrawn != "None":
                    taken[withdrawn] += 1

        return taken
    
    def addNewPortion(this, bloodType):
        this.packsCount[bloodType] += 1
        return (bloodType, this.packsCount[bloodType])

    def withdrawPortion(this, bloodType):
        sortedList = this.getMostSuitableDonors()
        donorsList = this.possibleDonors[bloodType]
        sortedDonors = []
        for i in sortedList:
            if i[0] in donorsList:
                sortedDonors.append(i)
        
        sortedDonors.sort(key=lambda tup: tup[1], reverse=True)
        chosenBloodType = sortedDonors[0][0]
        if this.packsCount[chosenBloodType] > 0:
            this.packsCount[chosenBloodType] -= 1
            return (chosenBloodType, this.packsCount[chosenBloodType])
        else:
            return ("None", 0)
