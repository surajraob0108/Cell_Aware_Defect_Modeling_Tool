""" Using the python-gdsii library to extract 
   the binary information in the gds file 
   to human readable text file """

# import necessary classes from gdsii library
from gdsii import types                 
from gdsii.record import Record
from math import sqrt
import array as arr

# 
# Layer Map Dictionary 
#
LayerMapDictionary = {"0": "NW",
                      "1": "ACT",
                      "2": "VTH",
                      "3": "VTL",
                      "4": "THKOX",
                      "5": "NIM",
                      "6": "PIM",
                      "7": "GATEA",
                      "8": "GATEB",
                      "9": "GATEC",
                      "10": "GATEAB",
                      "11": "AIL1",
                      "12": "AIL2",
                      "13": "GIL",
                      "14": "V0",
                      "15": "M1A",
                      "16": "M1B",
                      "17": "V1",
                      "18": "MINT1A",
                      "19": "MINT2A",
                      "20": "MINT3A",
                      "21": "MINT4A",
                      "22": "MINT5A",
                      "23": "MINT1B",
                      "24": "MINT2B",
                      "25": "MINT3B",
                      "26": "MINT4B",
                      "27": "MINT5B",
                      "28": "VINT1",
                      "29": "VINT2",
                      "30": "VINT3",
                      "31": "VINT4",
                      "32": "MSMG1",
                      "33": "MSMG2",
                      "34": "MSMG3",
                      "35": "MSMG4:drawing",
                      "36": "MSMG5",
                      "37": "VSMG1",
                      "38": "VSMG2",
                      "39": "VSMG3",
                      "40": "VSMG4",
                      "41": "VSMG5",
                      "42": "MG1",
                      "43": "MG2",
                      "44": "VG1",
                      "45": "RECTV0/MSMG4:label",
                      "46": "RECTV1",
                      "47": "NCONT",
                      "48": "VINT5",
                      "49": "M1",
                      "50": "MINT1",
                      "51": "MINT2",
                      "52": "MINT3",
                      "53": "MINT4",
                      "54": "MINT5",
                      "56": "MSMG5:label",
                      "200": "prBoundary"} 

# 
# Function to map layer number to layer name
# 
def LayerMapFunction(layernumberdata):
    return LayerMapDictionary[layernumberdata]

# 
# Function to calculate length of the boundary element
#
def length_element(inputlist):
    length = float(inputlist[2]) - float(inputlist[0])
    return length

# 
# Function to calculate width of the boundary element
#
def width_element(inputlist):
    width = float(inputlist[5]) - float(inputlist[3])
    return width

# 
# Function to calculate area of the boundary element
#
def area_element(xycoordinateinput):
    lengthxypair = len(xycoordinateinput)
    xycoordinatestring = str(xycoordinateinput)
    lengthxy = len(xycoordinatestring)
    global new_data
    new_data = xycoordinatestring[1:lengthxy-1].split(",")     # Got X, Y coordinate as a list
    if(lengthxypair > 3):
        length = length_element(new_data)
        width =  width_element(new_data)
        area_value  = length * width
    else:
        area_value = 0
    return area_value

# 
# Function to calculate the minuimum distance between two elements 
#
def minimumdistance_element(firstelement,secondelement):

    element1_length =length_element(firstelement)                  # Length of first element
    element2_length =length_element(secondelement)                 # Length of second element

    element1_width = width_element(firstelement)                   # Width of first element
    element2_width = width_element(secondelement)                  # Width of second element

    # calculate centre of two elements [x,y]
    element1_centre =  arr.array("f",[element1_length/2 + float(firstelement[0]), element1_width/2 + float(firstelement[1])])
    element2_centre =  arr.array("f",[element2_length/2 + float(secondelement[0]), element2_width/2 + float(secondelement[1])])

    # distance between the centre of two elements [x,y]
    distance_elements = arr.array("f",[abs(element2_centre[0]-element1_centre[0]), abs(element2_centre[1]-element1_centre[1])])

    # Four Possible cases
    # Case 1: Two elements do not intersect, but partially overlap in Y direction, then 
    #         the minimum distance would be the distance between between the right line 
    #         of the left element and the left line of the right element         
    if((distance_elements[0] >= ((element1_length + element2_length)/ 2)) and (distance_elements[1] < ((element1_width + element2_width) / 2))):

        minumim_distance = distance_elements[0] - ((element1_length + element2_length)/ 2)

    # Case 2: Two elements do not intersect, but partially overlap in X direction, then 
    #         the minimum distance would be the distance between between the bottom line 
    #         of the upper element and the upper line of the bottom element
    elif((distance_elements[1] >= ((element1_width + element2_width) / 2)) and (distance_elements[0] < ((element1_length + element2_length)/ 2))):

        minumim_distance = distance_elements[1] - ((element1_width + element2_width)/ 2)

    # Case 3: Two elements do not intersect and do not overlap, then the minimum distance
    #         would be caluclated using Pythagora's theorem
    elif((distance_elements[0] >= ((element1_length + element2_length)/ 2)) and (distance_elements[1] >= ((element1_width + element2_width) / 2))):
        x_value = distance_elements[0] - ((element1_length + element2_length)/ 2)
        y_value = distance_elements[1] - ((element1_width + element2_width) / 2)
        minumim_distance = sqrt((x_value * x_value) + (y_value * y_value))

    # Case 4:
    else:
        minumim_distance = "Two elements either intersect or not in the same layer"  

    return minumim_distance

# 
# Function to return the list with XY position of the elements 
#
def xypairposition_element(inputlist,elementposition):

    elementstr = str(inputlist[elementposition])
    elementsubstr = elementstr.split(":")         
    elementsubstrxy = elementsubstr[4]           
    elementsubstrxy = elementsubstrxy[1:len(elementsubstrxy) - 2].replace("'","")
    elementsubstrxy = elementsubstrxy.split(",")                                # Finally as list of coordinates    
    return elementsubstrxy

# 
# Function to return the neighbouring elements with the given position of the element in the list 
#
def neighboring_element(inputlist,elementposition):
    inputlistlength = len(inputlist)
    currentelement = str(inputlist[elementposition])
    currentelement = currentelement.split(":")
    print("Current element Layer:" + currentelement[3])
    position = elementposition - 1
    # Previous neighboring element layer
    while True: 
        if(position == 0):
            print("Only next neighbouring element would be present")
            break
        previouselement = str(inputlist[position])
        previouselement = previouselement.split(":")
        if(currentelement[2] == previouselement[2]):
            position = position - 1
            continue
        print("Previous neighbouring element in Layer:" + previouselement[3])
        break
    position = elementposition
    # Next neighboring element layer
    while True:
        if(position == inputlistlength - 1):
            print("Only previous neighbouring element would be present")
            break
        
        nextelement = str(inputlist[position])
        nextelement = nextelement.split(":")
        if(currentelement[2] == nextelement[2]):
            position = position + 1
            continue
        print("Next neighbouring element in Layer:"+ nextelement[3])
        break
    
         
# open the given gds file for reading in binary mode
with open("INV_X1.gds", "rb") as stream:
    file_name_input = stream.name.split(".")
    file_name = (file_name_input[0],"txt")
    file_name_output =".".join(file_name)
    file_name_element = (file_name_input[0],"element","data")
    file_name_element_output = "_".join(file_name_element)
    file_name_element_output_join  = (file_name_element_output,"txt")
    global fine_name_element_final
    fine_name_element_final = ".".join(file_name_element_output_join)


    # Based on the different data type , writing the necessary information to the text file
    with open(file_name_output, "w") as result:
        with open(fine_name_element_final,"w") as elementresult:

            global linenumber 
            linenumber = 0
            result.write("GDS:FileName:" + stream.name + "\n")
            result.write("\n")
            elementresult.write("GDS:FileName:" + stream.name + "\n")
            # Iterate through all the records in the given file
            for record_details in Record.iterate(stream):
                if record_details.tag_type == types.BITARRAY:
                    result.write("RecordType:"+ str(record_details.tag_name) + "\n" + "DataType:" + str(record_details.tag_type_name) + "\n" + "Data:" + str(record_details.data) + "\n")
                    result.write("\n")
                elif record_details.tag_type == types.INT2: 
                    result.write("RecordType:"+ str(record_details.tag_name) + "\n" + "DataType:" + str(record_details.tag_type_name) + "\n" + "Data:" +  str(record_details.data) + "\n")
                    if(record_details.tag_name == "LAYER"):
                        layernumberstring = str(record_details.data)
                        layernumber = layernumberstring[1:len(layernumberstring)-2]
                        result.write("LayerNumber:"+ layernumber +"\n")
                        linenumber = linenumber + 1
                        elementresult.write(str(linenumber) + ":"+"Layer:"+ layernumber +":")
                        result.write("LayerName:"+ LayerMapFunction(layernumber) + "\n")
                        elementresult.write(LayerMapFunction(layernumber) + ":")
                    result.write("\n")
                elif record_details.tag_type == types.INT4: 
                    result.write("RecordType:"+ str(record_details.tag_name) + "\n" + "DataType:" + str(record_details.tag_type_name) + "\n" + "Data:" +  str(record_details.data) + "\n")
                    result.write("Area:" + str(area_element(record_details.data))+"U" + "\n")
                    elementresult.write(str(new_data) + "\n")
                    result.write("\n")
                elif record_details.tag_type == types.REAL8: 
                    result.write("RecordType:"+ str(record_details.tag_name) + "\n" + "DataType:" + str(record_details.tag_type_name) + "\n" + "Data:" +  str(record_details.data) + "\n")
                    result.write("\n")          
                elif record_details.tag_type == types.ASCII:            
                    result.write("RecordType:"+ str(record_details.tag_name) + "\n" + "DataType:" + str(record_details.tag_type_name) + "\n" + "Data:" +  record_details.data.decode('utf-8') + "\n")
                    result.write("\n")
                elif record_details.tag_type == types.NODATA:            
                    result.write("RecordType:"+ str(record_details.tag_name) + "\n" + "DataType:" + str(record_details.tag_type_name) + "\n" + "Data:" +  str(record_details.data) + "\n") 
                    result.write("\n")
                else:
                    result.write("\n")
            elementresult.close()
            result.close()

# open the given element position details file for reading 
# and calculate minimum distance between two elements

with open(fine_name_element_final, "r") as elementfile:
    # read all the lines and return as list
    elementlist = elementfile.readlines() 

    # Pass the list and also the position of the elements in the list for which the minimum distance has to be calculated
    firstelementpositionxy = xypairposition_element(elementlist,5)
    secondelementpositionxy = xypairposition_element(elementlist,6)

    # distance between two elements 
    min_distance = minimumdistance_element(firstelementpositionxy,secondelementpositionxy)
    print("Minimum distance between the elements :" + str(min_distance) + "nm")
    
    # Pass the list and also the position of the element in the list for which the neighbouring elements has to be found
    neighboring_element(elementlist,5)

