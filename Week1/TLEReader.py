"""
This code was written for the Week 1 Mini-Challenge for the
Space Situational Awareness and Artifical Intelligence Undergraduate Research
Opportunity program. Please abide by the license in the repository when utilizing
our code.
@author Herbie Turner
"""
import pandas as pd
import requests

###Challenge Information###
########################################
cols = ["ID","a","e","M","BigO","SmallO","i","MeanMotion"]
# Orbits in kilometers
LEO = [0,2000]
MEO = [2000,35800]
GEO = [35,786,500]
HEO = [30000]

########################################


class TLEAnalyzer:
    def __init__(self, fileadr,permission):
        """Initiates TLEReader with a file address"""
        try:
            if permission not in ["a", "w", "r","a+","w+","r+"]:
                raise Exception("Invalid Permission. Valid open file\
                permissions include 'a', 'w', or 'r'. ")
        except:
            print("Something went wrong.")
        try:
            self.file = open(fileadr, permission)
        except:
            print("Something went wrong.")
        self.tleData = pd.DataFrame(columns=cols)

    def parse(self):
        """Adds TLE data to pandas dataframe"""
        lines = self.file.readlines()
        for x in range(int(len(lines)/2)):
            new_row = self.parse_line(lines[2*x], lines[2*x+1])
            self.tleData = pd.concat([new_row, self.tleData]).reset_index(drop = True)

    def parse_line(self, line1, line2):
        """Returns row of values for database"""
        pick1 = []
        pick2 = [0,4,6,3,0,2]
        arrParsed = []
        arr0 = line1.split()
        arr1 = line2.split()
        #Calculate semi major axis(in km) using formula below
        period = 1/float(arr1[7])*3600*24
        a = (period*398600/(4*3.14**2))**(1/3)
        arrParsed = pd.DataFrame({"ID":arr0[1],"a":a,"e":arr1[4],"M":arr1[6],"BigO":arr1[3],"SmallO":arr1[5],"i":arr1[2],"MeanMotion":arr1[7]},index=[0])
        return arrParsed

    def find_Satellite_Info(self, id):
        """Searches https://www.celestrak.com/satcat/search-results.php for satellite info"""
        session = requests.session()
        satInfo = self.tleData.loc[self.tleData["ID"] == id]

    def print(self):
        print(self.tleData)

    # Week 1 Challenge Functions
    def print_Satellite_Info(self):
        # Logic for identify facts about satellite go below
        for index, row in self.tleData.iterrows():
            print("THe satellite ")

    # def calculate_orbit():
    #     if
