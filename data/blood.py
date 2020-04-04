from csv import reader, writer

bloodTypesDict = {
    'O+': 0,
    'A+': 0,
    'B+': 0,
    'AB+': 0,
    'O-': 0,
    'A-': 0,
    'B-': 0,
    'AB-': 0
}

takesFromDict = {
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

distributionDict = {
    'A+': 34,
    'O+': 32,
    'B+': 17,
    'AB+': 7,
    'A-': 4,
    'O-': 3,
    'B-': 2,
    'AB-': 1
}

def checkBestBefore(pack):
    """
    Whole blood can be stored for 21 to 35 days in fridges, depending on the method of blood storage. We take the more strict 21 days.
    """
    pass

def bloodRarity():
    pass

def chooseBloodPackByRequest(bloodType):
    pass