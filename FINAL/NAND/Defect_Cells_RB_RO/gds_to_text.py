""" Using the python-gdsii library to extract the binary 
    information in the gds file to human readable text file """
# import necessary classes from gdsii library
from gdsii import types                 
from gdsii.record import Record
from math import sqrt
import array as arr
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
# 
# Layer Map Dictionary {"Layer Number":"Layer Name"}
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
# Function to calculate length of the boundary element using XY Pair Element position
#
def length_element(inputlist):
    length = float(inputlist[2]) - float(inputlist[0])
    return abs(length)
# 
# Function to calculate width of the boundary element using XY Pair Element position
#
def width_element(inputlist):
    width = float(inputlist[5]) - float(inputlist[3])
    return abs(width)
# 
# Function to calculate area of the boundary element using length and width
#
def dimension_details(xycoordinateinput):
    # conversion of list to string to remove unnecessary paramters
    xycoordinatestring = str(xycoordinateinput).replace(" ","")
    global new_data
    new_data = xycoordinatestring[1:(len(xycoordinatestring))-1].split(",")     # Got X, Y coordinate as a list
    if((len(xycoordinateinput)) > 3):
        # list to hold the x coordinates of the element
        xcoordinateinput = []
        # list to hold the y coordinates of the element
        ycoordinateinput = []
        # appending the list with the x coordinates only
        for i in range(0,len(xycoordinateinput),2):
            xcoordinateinput.append(xycoordinateinput[i])
        # appending the list with the y coordinates only
        for i in range(1,len(xycoordinateinput),2):
            ycoordinateinput.append(xycoordinateinput[i])
        # sorting the list in the asscending order
        xcoordinateinput.sort()
        ycoordinateinput.sort()
        # deleting the list with the identical/same elements
        xcoordinateinput = list(dict.fromkeys(xcoordinateinput))
        ycoordinateinput = list(dict.fromkeys(ycoordinateinput))
        # list to hold the differences of the elements of x coordinates
        xcoordinatedifferences = []
        # list to hold the differences of the elements of y coordinates
        ycoordinatedifferences = []
        for i in range(1,len(xcoordinateinput)):
            x_value = float(xcoordinateinput[i]) - float(xcoordinateinput[i-1])
            # appending the list with the differences in x value
            xcoordinatedifferences.append(str(abs(x_value)))
        for i in range(1,len(ycoordinateinput)):
            y_value = float(ycoordinateinput[i]) - float(ycoordinateinput[i-1])
            # appending the list with the differences in y value
            ycoordinatedifferences.append(str(abs(y_value))) 
        # considering the minimum value
        xcoordinatedifferences = list(map(float,xcoordinatedifferences))
        ycoordinatedifferences = list(map(float,ycoordinatedifferences))
        min_value = []
        min_value.append(min(xcoordinatedifferences))
        min_value.append(min(ycoordinatedifferences))
        min_value = list(map(float,min_value))
        min_dimension_value = min(min_value)
        asciidatatype = 0
    else:
        min_dimension_value = 0
        asciidatatype = 1        
    return asciidatatype,min_dimension_value
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
        #minumim_distance = "Two elements either intersect or not in the same layer"  
        minumim_distance = 0

    return minumim_distance
# 
# Function to return the list with XY position of the elements 
#
def xypairposition_element(inputlist,elementposition):
    elementstr = str(inputlist[elementposition])
    elementsubstr = elementstr.split(":")         
    elementsubstrxy = elementsubstr[4]                                          # Obtaining only XY pairs string       
    elementsubstrxy = elementsubstrxy[1:len(elementsubstrxy) - 2].replace("'","")
    elementsubstrxy = elementsubstrxy.split(",")                                # Finally as list of coordinates    
    return elementsubstrxy
# 
# Function to return the string with corresponding XY position of the element
#
def xypairposition_element_string(inputlist,elementposition):
    elementstr = str(inputlist[elementposition])
    elementsubstr = elementstr.split(":")   
    elementsubstrxy = elementsubstr[5] 
    return elementsubstrxy
# 
# Function to return the neighbouring elements with the given position of the element in the list 
#
def neighboring_element(inputlist,elementposition):
    inputlistlength = len(inputlist)
    currentelement = str(inputlist[elementposition])
    currentelement = currentelement.split(":")
    position = elementposition - 1
    # Previous neighboring element layer
    while True: 
        if(position == 0):
            previouselement = ["","No Layer"]
            break
        previouselement = str(inputlist[position])
        previouselement = previouselement.split(":")
        if(currentelement[1] == previouselement[1]):
            position = position - 1
            continue
        break
    position = elementposition
    # Next neighboring element layer
    while True:
        if(position == inputlistlength - 1):
            nextelement = ["","No Layer"]
            break
        
        nextelement = str(inputlist[position])
        nextelement = nextelement.split(":")
        if(currentelement[1] == nextelement[1]):
            position = position + 1
            continue
        break
    return currentelement[1],previouselement[1],nextelement[1]
# 
# Function to modify the elementfile by removing the elements with text label XY pairs 
#
def modifyelementfile():
    elementpositiontextlabel = []                                        # Array to hold element position with text label
    listelementpositiontextlabel = []                                    # List to hold elements with text label  
    for i in range(1,len(updateelementlist)):
        xypairlength = updateelementlist[i].split(":")[4]
        xypairlength = xypairlength[1:len(xypairlength) -2]
        xypairlength = xypairlength.split(",")
        if(len(xypairlength) < 8):
            elementpositiontextlabel.append(i)

    # adding the elements to list "listelementpositiontextlabel" with elementposition text label
    for i in range(len(elementpositiontextlabel)):                         
        listelementpositiontextlabel.append(updateelementlist[elementpositiontextlabel[i]])

    # removing the elements from the  list "updateelementlist" with elementposition text label
    for i in range(len(listelementpositiontextlabel)):
        updateelementlist.remove(listelementpositiontextlabel[i])    
# 
# Function to return width value from the elementlist "Sl. No : Layer Name : Layer No : Minimum_Value(nm) : XY Position"
#
def sortwidth(inputlist):
    widthvalue = float(inputlist.split(":")[3])                
    return widthvalue
# 
# Function to create a file with only metal layer boundary elements 
#
def elementmetallayer():
    metalelementstring = []                                                                   # List to hold the metal elements text data (String : VSS, VDD...)
    elementpositiontextlabel = []                                                             # Array to hold element position with text label    
    listmetallayerboundaryelements = []                                                       # List to hold the metal layer boundary elements only
    listmetallayertextelements = []                                                           # List to hold the metal layer text elements only
    listpolygonboundaryelements = []                                                          # List to hold the polygon of boundary elements
    listpositiontextelements = []                                                             # List to hold the position of text elements
    asciistring = []                                                                          # List to hold ascii string data
    with open("MetalLayerElements.txt", "w") as filemetallayerelements:
        for i in range(1,len(updateelementlist)):
            layernumber_metal = updateelementlist[i].split(":")[2]                            # Separating based on layer number
            if(layernumber_metal == "15" or layernumber_metal == "16"):
                listmetallayerboundaryelements.append(updateelementlist[i])                   # appending the list with metal layer elements (boundary and text)

        for i in range(0,len(listmetallayerboundaryelements)):
            xypairlength = listmetallayerboundaryelements[i].split(":")[4]
            xypairlength = xypairlength[1:len(xypairlength) -2]            
            xypairlength = xypairlength.replace("'","").split(",")
            if(len(xypairlength) < 3):
                elementpositiontextlabel.append(i)
                point = Point(int(xypairlength[0]),int(xypairlength[1]))
                listpositiontextelements.append(point)                                       # appending the list with XY Pair position text elements
            else:
                pointsarray = []                                                             # list to hold the XY pair of points
                for j in range(0,len(xypairlength) - 1,2):
                    pointsarray.append(Point(int(xypairlength[j]),int(xypairlength[j+1])))
                listpolygonboundaryelements.append(Polygon(pointsarray))                     # appending the list with XY Pair position boundary elements
            

        # adding the elements to list "listmetallayertextelements" with elementposition text label only
        for i in range(len(elementpositiontextlabel)):                         
            listmetallayertextelements.append(listmetallayerboundaryelements[elementpositiontextlabel[i]])
            textposition = listmetallayertextelements[i].split(":")[4]
            textposition = textposition[1:len(textposition) -2]
            textposition = textposition.replace("'","").split(",")
            point = Point(int(textposition[0]),int(textposition[1]))
            textdata = listmetallayertextelements[i].split(":")[5]
            positiontext = str(point) + ":" + textdata.replace("\n","")
            asciistring.append(positiontext)                                                    # appending the ascii text string to the list
        value = 0

        # Finding the point related it whether it lies inside the polygon
        # Updating the list by adding ascii text string to its related boundary element
        for i in listpositiontextelements:                                                  # for every point of text element
            for j in listpolygonboundaryelements:                                           # for every polygon of boundary element
                if(j.contains(i)):                                                          # will be true for one of the boundary element only
                    for k in asciistring:                                                   # for every text so that it relates with the point
                        textpointasciistring = k.split(":")[0]                      
                        textpointlistpositiontextelements = str(i)
                        if(textpointasciistring == textpointlistpositiontextelements):
                            textdataasciistring =  k.split(":")[1]                          # only if the point is in the polygon and point matches with the text                        
                            data = str(listmetallayerboundaryelements[value])
                            #data = data.replace(data[0:2],asciistring[value].replace("\n",""))      # replace Sl.No with the ascii text string
                            data = data.replace("\n","") + ":" + textdataasciistring +"\n"           # adding the ascii text string to its related boundary element
                            del listmetallayerboundaryelements[value]
                            listmetallayerboundaryelements.insert(value,data)                               
                            value = 0
                            # Every string data is added to the list - helps in mapping in the netlist
                            metalelementstring.append(textdataasciistring)
                            break
                        else:
                            continue
                    break
                else:
                    value = value + 1
                    continue
        
        # removing the elements from the  list "listmetallayerboundaryelements" with elementposition text label
        for i in range(len(listmetallayertextelements)):
            listmetallayerboundaryelements.remove(listmetallayertextelements[i]) 

        listmetallayerboundaryelements.sort(key=sortwidth)                                   # sorted metal layer boundary elements based on their width       

        filemetallayerelements.write("GDS:FileName:" + stream.name + " Text Element : Layer Name : Layer No : Minimum_Value(nm) : XY Position" + "\n")
        for i in listmetallayerboundaryelements:
            filemetallayerelements.write("%s" %i)
        filemetallayerelements.close()    

# Code starts here ...!!!!
# CellName.txt and CellName_element_data.txt (Partial)
# open the given gds file for reading in binary mode
with open("NAND2_X1.gds", "rb") as stream:
    file_name_input = stream.name.split(".")
    file_name = (file_name_input[0],"txt")
    file_name_output =".".join(file_name)                                           # TEXT FILE NAME CREATION
    
    file_name_element = (file_name_input[0],"element","data")
    file_name_element_output = "_".join(file_name_element)
    file_name_element_output_join  = (file_name_element_output,"txt")

    file_name_element_width = (file_name_input[0],"element","width","order") 
    file_name_element_width_output = "_".join(file_name_element_width)
    file_name_element_width_output_join = (file_name_element_width_output,"txt")

    file_name_layer_info = (file_name_input[0],"Layer","Information")
    file_name_layer_info_output = "_".join(file_name_layer_info)
    file_name_layer_info_output_join = (file_name_layer_info_output,"txt")

    file_name_spice_file_output = (file_name_input[0],"sp")

    global file_name_element_final
    global file_name_element_width_final
    global file_name_layer_info_final
    global file_name_spice_file_final
    file_name_element_final = ".".join(file_name_element_output_join)               # ELEMENT FILE NAME CREATION
    file_name_element_width_final = ".".join(file_name_element_width_output_join)   # ELEMENT FILE WIDTH ORDER CREATION
    file_name_layer_info_final = ".".join(file_name_layer_info_output_join)         # LAYER INFORMATION FILE CREATION
    file_name_spice_file_final = ".".join(file_name_spice_file_output)              # SPICE FILE 

    # Based on the different data type , writing the necessary information to the text file
    with open(file_name_output, "w") as result:
        with open(file_name_element_final,"w") as elementresult:
            global linenumber 
            linenumber = 0
            result.write("GDS:FileName:" + stream.name + "\n")
            result.write("\n")
            elementresult.write("GDS:FileName:" + stream.name + " : Sl. No : Layer Name : Layer No : Minimum_Value(nm) : XY Position" + "\n")
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
                        result.write("LayerName:"+ LayerMapFunction(layernumber) + "\n")
                        linenumber = linenumber + 1
                        elementresult.write(str(linenumber) + ":" + LayerMapFunction(layernumber) + ":" + layernumber +":")
                    result.write("\n")
                elif record_details.tag_type == types.INT4: 
                    result.write("RecordType:"+ str(record_details.tag_name) + "\n" + "DataType:" + str(record_details.tag_type_name) + "\n" + "Data:" +  str(record_details.data) + "\n")
                    dimension_details_result = dimension_details(record_details.data)
                    result.write("Minimum Value: " + str(dimension_details_result[1]) + "nm" + "\n")
                    if(str(dimension_details_result[0]) == "0"):
                        elementresult.write(str(dimension_details_result[1]) + ":" + str(new_data)+"\n")
                    else:
                        elementresult.write(str(dimension_details_result[1]) + ":" + str(new_data)+":")
                    result.write("\n")
                elif record_details.tag_type == types.REAL8: 
                    result.write("RecordType:"+ str(record_details.tag_name) + "\n" + "DataType:" + str(record_details.tag_type_name) + "\n" + "Data:" +  str(record_details.data) + "\n")
                    result.write("\n")          
                elif record_details.tag_type == types.ASCII:            
                    result.write("RecordType:"+ str(record_details.tag_name) + "\n" + "DataType:" + str(record_details.tag_type_name) + "\n" + "Data:" +  record_details.data.decode('utf-8') + "\n")
                    if(record_details.tag_name == "STRING"):
                        elementresult.write(record_details.data.decode('utf-8') + "\n" )
                    result.write("\n")
                elif record_details.tag_type == types.NODATA:            
                    result.write("RecordType:"+ str(record_details.tag_name) + "\n" + "DataType:" + str(record_details.tag_type_name) + "\n" + "Data:" +  str(record_details.data) + "\n") 
                    result.write("\n")
                else:
                    result.write("\n")      
            elementresult.close()
        result.close()
#           
# CellName_element_data.txt (removing XY pair - text elements)
# Reading the elementfile (CellName_element_data.txt) and creating the global list of elements
with open(file_name_element_final, "r") as updateelementfile:
    # read all the lines and return as list
    global updateelementlist 
    updateelementlist = updateelementfile.readlines()               
    updateelementfile.close()
#
# Separating the elements belongng to metal layer - information with metal layer elements only
elementmetallayer()
#
# Modify the elementfile (removing XY pair - text elements)
modifyelementfile()
#
# Writing the elementfile with updated list "updateelementlist"
#
with open(file_name_element_final, "w") as updateelementfile:
    # read all the lines and return as list
    for i in updateelementlist:
        updateelementfile.write("%s" %i)
    updateelementfile.close()
#  
# open the given element position details file for reading 
# and calculate minimum distance between two elements
with open(file_name_element_final, "r") as elementfile:
    # read all the lines and return as list
    elementlist = elementfile.readlines() 

    # Pass the list and also the position of the elements in the list for which the minimum distance has to be calculated
    firstelementpositionxy = xypairposition_element(elementlist,12)
    secondelementpositionxy = xypairposition_element(elementlist,13)

    # distance between two elements 
    min_distance = minimumdistance_element(firstelementpositionxy,secondelementpositionxy)
    #print("Minimum distance between the elements :" + str(min_distance) + "nm")

    
    # Pass the element list and write the information on neighboring layers to the file "
    list_layer_info = ["Current Layer : Previous Layer : Next Layer"]                            # LAYER INFORMATION FILE LINE1                                                              # LIST containing Layer Information

    for i in range(1,len(elementlist)):
        layerinfo = neighboring_element(elementlist,i)
        list_layer_info.append(":".join(layerinfo))

    # Deleting the duplicate items in the list "list_layer_info" 
    list_layer_info = list(dict.fromkeys(list_layer_info))

    # CellName_Layer_Information.txt
    # Writing the Layer Information to the file
    with open(file_name_layer_info_final,"w") as file_open_layer_info: 
        # write into the file 
        for i in list_layer_info:
            file_open_layer_info.write("%s \n" %i)
        file_open_layer_info.close()


    # To sort the elementlist based on increasing order of width's element
    global listwidthsort
    listwidthsort = elementlist[1:len(elementlist)]
    listwidthsort.sort(key=sortwidth)
#
# CellName_element_width_order.txt
# Writing the elementfilewidth with  list "listwidthsort" updated based on element's width value
with open(file_name_element_width_final, "w") as elementwidthfile:
    # write into the file
    elementwidthfile.write("GDS:FileName:" + stream.name + " : Sl. No : Layer Name : Layer No : Minimum_Value(nm) : XY Position" + "\n")
    for i in listwidthsort:
        elementwidthfile.write("%s" %i)
    elementwidthfile.close() 
# List to hold the string of first given metal element for resistive bridges
metalelementstringfirstresistivebridge = []
# List to hold the string of metal elements with the closest elements for a given metal element
metalelementstringsecond = []
# List to hold the string of metal elements for resistive open (minimum width)
metalelementresistiveopen = []
# List to hold the string of variables for resistive bridges
resistivebridgestring = []
# List to hold the string of variables for resistive opens
resistiveopenstring = []
# List to hold the string of variables for nodes of resistive opens
resistiveopennodesstring = []

# For gds file with extra metal elements other than inputs and outputs
# Reading the MetalLayerElements.txt file 
metallayerelementsfileinread = open("MetalLayerElements.txt","rt")
metallayerelementsupdate = metallayerelementsfileinread.readlines()
j = 1
for i in range(1,len(metallayerelementsupdate)): 
    elementstr = str(metallayerelementsupdate[i])
    elementsubstr = elementstr.split(":")
    if(len(elementsubstr) <= 5):
        metallayerelementsupdate[i] = metallayerelementsupdate[i].replace("\n","") + ":M" + str(j) + "\n"
        j = j + 1

# Writing the data to the MetalLayerElements.txt file 
metallayerelementsfileoutwrite = open("MetalLayerElements.txt","wt")
metallayerelementsfileoutwrite.writelines(metallayerelementsupdate)
metallayerelementsfileoutwrite.close() 

# Finding the minimum distance between the boundary elements in the metal layer only and finding the closest one
with open("MetalLayerElements.txt", "r") as boundaryelementsmetallayerfile:
    with open("NeighboringElementsList.txt","w") as neighboringelementsfile:
        neighboringelementsfile.writelines("Distance between the metal elements" + "\n")
        boundaryelementsmetallayerlist = boundaryelementsmetallayerfile.readlines()

        # appending the list with the string of minimum width metal elements
        for i in range(1,len(boundaryelementsmetallayerlist)):
            elementstr = str(boundaryelementsmetallayerlist[i])
            elementsubstr = elementstr.split(":")
            if(float(elementsubstr[3]) <= 40.0):
                elementstring = xypairposition_element_string(boundaryelementsmetallayerlist,i)
                elementstring = elementstring.replace("\n","")
                metalelementresistiveopen.append(elementstring)
        
        # Variable to hold the position of first element 
        for j in range(1,len(boundaryelementsmetallayerlist)):
            # Pass the list and also the position of the elements in the list for which the minimum distance has to be calculated
            firstelementpositionxy = xypairposition_element(boundaryelementsmetallayerlist,j)                # First Element : To obtain XY Pair Position
            firstelementstring = xypairposition_element_string(boundaryelementsmetallayerlist,j)             # First Element : To obtain string corresponding to the position of element
            firstelementstring = firstelementstring.replace("\n","")
            # appending the list with the first given metal element for resistive brdiges
            metalelementstringfirstresistivebridge.append(firstelementstring)            
            # List to hold the distance between a given metal element w.r.t other metal elements
            min_distance = []
            # List to hold the string of metal elements other than the first given metal element
            min_distance_metalelementstring = []
            # Variable to hold the position of second element
            for i in range(1,len(boundaryelementsmetallayerlist)):
                if(i == j):
                    # dummy assignment
                    dummy_variable_value = 100
                else:
                    secondelementpositionxy = xypairposition_element(boundaryelementsmetallayerlist,i)         # Second Element : To obtain XY Pair Position
                    secondelementstring = xypairposition_element_string(boundaryelementsmetallayerlist,i)      # Second Element : To obtain string corresponding to the position of element
                    secondelementstring = secondelementstring.replace("\n","")
                    # appending to the list all the metal elements other than the first given metal element
                    min_distance_metalelementstring.append(secondelementstring)
                    # distance between two elements                     
                    min_distance_value = minimumdistance_element(firstelementpositionxy,secondelementpositionxy)
                    # appending to the list all the distances so that the minimum one to be found
                    min_distance.append(min_distance_value)
                    neighboring_string_data = firstelementstring + " and " + secondelementstring + " is " + str(min_distance_value) + " nm" + "\n"
                    neighboringelementsfile.writelines(neighboring_string_data)
            # min_distance.index(min(min_distance)) - Will give the position of the element with least value
            # min_distance_metalelementstring[min_distance.index(min(min_distance))] - extract the string from the index value
            # appending to the list the metal elements with closest ones  []
            closestvalue = "Closest Element to " + firstelementstring + "-" + min_distance_metalelementstring[min_distance.index(min(min_distance))]
            metalelementstringsecond.append(min_distance_metalelementstring[min_distance.index(min(min_distance))])
            # Finding the minimum value in the list
            min_value_list = min(min_distance)
            # replacing it with the maximum value : helps in finding if there is another value with the same minimum value
            min_distance[min_distance.index(min(min_distance))] = max(min_distance)
            # iterate through the list with k - element position and x - element value
            for k,x in enumerate(min_distance):
                if x == min_value_list: 
                    # Element string added in case if the list has same multiple minimum values - string in the NeighboringElementsList.txt, firstmetal element, secondmetal element
                    closestvalue = closestvalue + " and " + min_distance_metalelementstring[k]
                    metalelementstringfirstresistivebridge.append(firstelementstring)
                    metalelementstringsecond.append(min_distance_metalelementstring[k])
            closestvalue = closestvalue + "\n"   
            neighboringelementsfile.writelines(closestvalue)        

# appeding the list with number of resistive bridges depending on the number of metal elements
for i in range(len(metalelementstringfirstresistivebridge)):
    resistivebridgestring.append("RB"+str(i+1))

# appeding the list with number of resistive opens depending on the number of metal elements with minimum width
for i in range(len(metalelementresistiveopen)):
    resistiveopenstring.append("RO"+str(i+1))

# appeding the list with number of nodes depending on the number of metal elements with minimum width
for i in range(len(metalelementresistiveopen)):
    resistiveopennodesstring.append("N"+str(i+1))

# List to hold string lines of resistive bridges between the metal elements as nodes
# String Format RBi ME1 ME2 xi
resistivebridgedata = []
# List to hold string lines of resistive open in resistive bridges between the node and metal element
# String Format ROi N1 ME2 50
resistivebridgeresistiveopendata = [] 
for i in range(len(metalelementstringfirstresistivebridge)):
    resistivebridgeelementdata = resistivebridgestring[i] + " " + metalelementstringfirstresistivebridge[i] + " " + metalelementstringsecond[i] + " x0"
    resistivebridgeelementdata_ro = "RO1" + " " + metalelementstringsecond[i] + " "
    resistivebridgedata.append(resistivebridgeelementdata)
    resistivebridgeresistiveopendata.append(resistivebridgeelementdata_ro)

# List to hold string lines of resistive opens 
# String Format ROi ME1 N1 yi
resistiveopendata = []
for i in range(len(metalelementresistiveopen)):
    resistiveopenelementdata = resistiveopenstring[i] + " " + metalelementresistiveopen[i] + " " + resistiveopennodesstring[i] + " x0"
    resistiveopendata.append(resistiveopenelementdata)

# Reading netlist file in "read-text" mode
fileinread = open(file_name_spice_file_final,"rt")
data = fileinread.read()
# appending the line containing string ".SUBCKT" with the resistive bridge value so that it can be varied for every cell instance called
# string to list 
datalist = data.split("\n")
data = ""
for i in range(len(datalist)):
    # finding the line only with ".SUBCKT" and changing the contents of the line 
    if ".SUBCKT" in datalist[i]:
        datalist[i] = datalist[i]+ "x0=1000"
    data = data + datalist[i] + "\n"
 
# Creating list of complete file data for Resistive bridges defect cell model
filedataresistivebridge = []
for i in range(len(resistivebridgedata)):
    filestringdata = data.replace(".ENDS",resistivebridgedata[i] + "\n" +  resistivebridgeresistiveopendata[i] + "\n" + ".ENDS")
    
    # string to list 
    filestringdatalist = filestringdata.split("\n")
    filestringdata = ""
    for j in range(len(filestringdatalist)):
        # Equation line to be updated
        if "*.EQN" in filestringdatalist[j]:
            filestringdatalist[j] = filestringdatalist[j].replace("="," =") 
            filestringdatalist[j] = filestringdatalist[j].replace(")"," )")
        # Replacing nodes with ZN with ZN_0
        if metalelementstringsecond[i] in filestringdatalist[j]:
            filestringdatalist[j] = filestringdatalist[j].replace(metalelementstringsecond[i] + " " ,metalelementstringsecond[i] + "_0 ")
        # appending the line containing string ".RO1" with the second metal element node and resistive open value "50"
        if "RO1" in filestringdatalist[j]:
            filestringdatalist[j] = filestringdatalist[j]  + metalelementstringsecond[i] + " 50"
        # finding the ".SUBCKT line" and "PIN_INFO line" and replacing ZN_0 with ZN
        if ".SUBCKT" in filestringdatalist[j]:
            filestringdatalist[j] = filestringdatalist[j].replace(metalelementstringsecond[i] + "_0",metalelementstringsecond[i])
            filestringdatalist[j+1] = filestringdatalist[j+1].replace(metalelementstringsecond[i] + "_0",metalelementstringsecond[i])
        filestringdata = filestringdata + filestringdatalist[j] + "\n"
    filedataresistivebridge.append(filestringdata)

for i in range(len(resistivebridgedata)):
    # Writing the data related to resistive bridge to the netlist file
    fileoutwrite = open("Defect_Cell_" + resistivebridgestring[i] + ".sp" ,"wt")
    fileoutwrite.write(filedataresistivebridge[i])
    fileoutwrite.close()

# Creating list of complete file data for Resistive opens defect cell model
filedataresistiveopen = []
for i in range(len(resistiveopendata)):
    filestringdata = data.replace(".ENDS", resistiveopendata[i] + "\n" + ".ENDS")
    filedataresistiveopen.append(filestringdata)

for i in range(len(resistiveopendata)):
    # Writing the data related to resistive open to the netlist file
    fileoutwrite = open("Defect_Cell_" + resistiveopenstring[i] + ".sp" ,"wt")
    fileoutwrite.write(filedataresistiveopen[i])
    fileoutwrite.close()
fileinread.close()