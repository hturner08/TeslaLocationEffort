from TLEReader import *

testReader = TLEAnalyzer("./TLEs_Week1.txt","r")
testReader.parse()
testReader.print()
testReader.print_Satellite_Info()
