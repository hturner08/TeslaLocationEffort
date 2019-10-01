from TLEReader import *

testReader = TLEAnalyzer("./TLEs_Week1.txt","r")
testReader.parse()
testReader.print()
print("\n")
testReader.print_Satellite_Info()
