"""
This code was written for the Week 1 Mini-Challenge for the
Space Situational Awareness and Artifical Intelligence Undergraduate Research
Opportunity program. Please abide by the license in the repository when utilizing
our code.
"""

# Libaries used are pandas, requests, and math
import pandas as pd
import requests
import math

#######################################
####### Challenge Information ##########
########################################
cols = ["ID","a","e","M","BigO","SmallO","i","MeanMotion"]
# Orbits in kilometers
LEO = [0,2000]
MEO = [2000,35800]
GEO = [35786,500]
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
        """Prints orbital information about each satellite"""
        for index, row in self.tleData.iterrows():
            print("-------------------------" + row[0] + "------------------------------")
            orbit = self.calculate_orbit(row)
            print("The satellite is in " + orbit)
            ecc = self.orbit_style(row)
            print("The satellite is in " + ecc)
            ang = self.crit_ang(row)
            print("The satellite is " + ang)
            sun = self.sun_sync(row)
            print("The satellie is " + sun)
            print("\n")

    def calculate_orbit(self,row):
        """Calculates which orbit a satellite is in"""
        MeanMotion = float(row[7])
        if float(row[6]) < .05 and MeanMotion - 1 <= .01:
            return "Geostationary Orbit"
        else:
            if MeanMotion > 11:
                return "Low Earth Orbit"
            elif MeanMotion < 11 and MeanMotion > 1:
                return "Medium Earth Orbit"
            else:
                return "Highly-Elliptical Orbit"
        return "an unknown orbit"

    def orbit_style (self,row):
        """Determins nature of orbit based on eccentricity"""
        ecc = float("."+row[2])
        if ecc <= .01:
            return "Circular Orbit"
        elif ecc <= .02:
            return "Near-Circular Orbit"
        else:
            return "Elliptical Orbit"

    def crit_ang(self, row):
        """Checks if satellite is in a critically inclined orbit"""
        ang = float(row[6])
        arg_perg = float(row[5])
        orb_per = 1 / float(row[7])
        a = float(row[1])
        if abs(ang - 63.4) <= 2:
            if abs(arg_perg - 270) <= 16 and abs(orb_per - .5) <= .1:
                return "in Molniya Orbit (Critically Inclined)"
            else:
                return "Critically Inclined"
        else:
            return "Not Critically Inclined"

    def sun_sync(self, row):
        """Determines whether or not a satellite is in a Sun Synchronous orbit"""
        a = float(row[1])
        i = float(row[6])
        u = 5.167 * (10**12)
        if self.orbit_style(row) == "Circular Orbit"\
         or self.orbit_style(row) == "Near-Circular Orbit":
                T = 2 * math.pi * ((a**3) / u)** (.5)
                x = -(T/3.796)**(7/3)
                if abs(x - math.cos(i)) <= .1 * abs(math.cos(i)):
                    return "in Sun Synchronous Orbit"
                else:
                    return "in non Sun Synchronous Orbit"
        else:
            return "Elliptical N/A"
