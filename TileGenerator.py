import os, sys, shutil, re
from PIL import Image

# Check if image resolutions are multiples of 128
def parsesize():
    sizestr = "size = { "
    with Image.open(os.path.join(os.path.dirname(__file__), "RandomMap/map/heightmap.bmp")) as heightmap:
        width, height = heightmap.size

    if width%128 != 0 or height%128 != 0:
        print("Width and height of your maps must be a multiple of 128. Exiting now.")
        sys.exit()
    
    tilewidth = int(width/128)
    tileheight = int(height/128)

    sizestr = sizestr + str(tilewidth) + " " + str(tileheight) + " }"
    return(sizestr)

# Copy required maps into new folder
def createfolder(tilename):
    path = os.path.join(os.path.dirname(__file__), tilename)
    # Check whether the specified path exists or not
    isExist = os.path.exists(path)
  
    if not isExist:
      # Create a new directory because it does not exist
       os.makedirs(path)
       print('''Created directory for new tile "'''+tilename+'''"''')
    return path

def copy_and_rename(src_path, dest_path, new_name):
    new_path = f"{dest_path}/{new_name}"
    shutil.copy(f"{src_path}", new_path)
 
def provincelist():
    # Generate list of provinces from definition.csv
    with open(os.path.join(os.path.dirname(__file__), "RandomMap/map/definition.csv")) as defsfile:
        provlist = defsfile.readlines()

    num_provinces = len(provlist)
    if num_provinces > 1000:
        print("The EU4 tile system cannot process more than 1000 provinces (including sea and wasteland provinces). Please use another world. Exiting now.")
        sys.exit()
    return provlist

def defs_to_tile(items):
    sea_provinces = []
    wasteland_provinces = []
    removed_lines = 0

    for item in items:
        item = item.rstrip(';x')  # Remove ';x' at the end of each line
        if "PROVINCE" in item:
            removed_lines += 1
            continue
        parts = item.split(';')[1:]  # Remove the first number on each line
        rgb_values = "{" + " ".join(parts[:3]) + "}"
        if "SEA_ZONE" in item:
            sea_provinces.append(f"sea_province = {rgb_values}")
        elif "WASTELAND" in item:
            wasteland_provinces.append(f"wasteland_province = {rgb_values}")

    num_sea_provinces = len(sea_provinces)
    num_land_provinces = removed_lines

    sea_province_str = '\n'.join(sea_provinces)
    wasteland_province_str = '\n'.join(wasteland_provinces)

    result = f"{sea_province_str}\n\n{wasteland_province_str}\n\nnum_land_provinces = {num_land_provinces}\nnum_sea_provinces = {num_sea_provinces}"
    return result

def file_to_list(name):
   path = os.path.join(os.path.dirname(__file__), name+".txt")
   isExist = os.path.exists(path)
   if isExist:
       with open(os.path.join(os.path.dirname(__file__), name+".txt")) as input_file:
        input_list = input_file.readlines()
        # Remove any empty lines
        input_list = [line.strip() for line in input_list if line.strip()]
        return input_list
   else:
        return []
    
def convert_hex_to_rgb(input_item, name):  
    # Remove the '#' character 
    input_item = input_item.lstrip('#') 
    input_item = input_item.rstrip('\n') 
    # Split the hex value into red, green, and blue components
    r = int(input_item[0:2], 16)
    g = int(input_item[2:4], 16)
    b = int(input_item[4:6], 16)
    
    # Format the RGB values as a string separated by spaces and surrounded by curly brackets
    rgb_str = name + " = " + '{{{0} {1} {2}}}'.format(r, g, b)  
    return rgb_str

# Convert each hex value to RGB format and add parameter name in front of each line
def palette_to_modifiers(name):
    input_list = file_to_list(name)
    if len(input_list) != 0:
        rgb_list = [convert_hex_to_rgb(item, name) for item in input_list]
        list_length = len(rgb_list)
        rgb_string = '\n'.join(rgb_list)
        return rgb_string, list_length
    else:
        print(name+".txt not found. Skipping.")
        return "",0

# Prompt for tileweight
def prompt_for_tileweight():
    print('You can apply a weight to your tile to influence the likelihood that it will appear. Skip to use default (100).')
    tileweight = input()

    if not re.match(r"^[0-9]+$", tileweight ):
        print('Using default value')
        weight = 100
    else:
        weight = tileweight
    weightline = "\nweight = "+str(weight)+"\n"
    return weightline

# Main thread
print('''Welcome to Tile Generator 0.1. This script takes the output of Haftetavenscrap's World Generator Plus, and turns it into a tile for the EU4 Random World generator. 
This script should be placed in the same folder as the generated world folder and .mod file. 
      
Please enter a name for your world. Keep it simple, only letters and numbers, dash or underscore.''')
tilename = input()
if not re.match(r"^[a-zA-Z0-9-_]+$", tilename ):
    print('''Invalid name, using "newtile" instead.''')
    tilename = "newtile"

# Initiate file
filename = tilename+".txt"
filepath = os.path.join(os.path.dirname(__file__),filename)
f = open(filename, 'w')

# Write provinces
f.write(defs_to_tile(provincelist()))
f.write('\n')

# COTs. No printing totals.
f.write(palette_to_modifiers("level_1_center_of_trade")[0])

# Estuaries. No printing totals.
f.write(palette_to_modifiers("river_estuary_modifier")[0])

# Write size
f.write('\n')
f.write(parsesize())

f.write(prompt_for_tileweight())

# Regions. Print total number.
regionstuple = palette_to_modifiers("region")
regions = regionstuple[0]
num_regions = regionstuple[1]
f.write(regions)

# Append total number of regions, if regions file found
if num_regions > 0:
    regionsline = "regions = "+str(num_regions)
    f.write('\n')
    f.write(regionsline)
    f.write('\n')

# Add extra settings to be changed manually
print("Extra settings can be set manually in the generated textfile.")
f.write('''
        
# You can uncomment these settings to activate. They are optional. The explanations come from the pdf guide at https://forumcontent.paradoxplaza.com/public/131201/Tile%20Making%20-%20an%20introduction.pdf, but have been copied in case the file goes offline.   

# You can name provinces. Works great for wastelands. Find the RGB values using GIMP. May integrate this into script later.
# province_names = {
# 	"Great Blade Lake" = { 52 54 41 }
# }    

# Same for straits, hope to integrate this in a later version.   
# strait = {
#   from = { 163 206 224 }
#	to = { 229 146 169 }
#	through = { 168 231 155 }
# }

# The tile will not be rotated. The tile can still be mirrored.
# do_not_rotate = yes 
        
# The tile will not be rotated or mirrored.
# do_not_rotate_or_mirror = yes 
        
# The tile will be place along the northern edge of the map, need for tiles which isnt surrounded bywater.
# restrict_to_north_edge = yes

# As above just placed along the southern edge of the map.     
# restrict_to_south_edge = yes
        
# Defines the tile as a continent. This should be done to large tiles, above 5 x 5. During generation the game will push these tiles north or south to try and fit two.
# Continent = yes
        
# Define the tile as a fantasy tile. Fantasy "mode" is enabled by standard in the game but can beturned off in options
# Fantasy = yes

# A tile is per standard defined as unique. Setting this to -1 makes it possible for the tile to appear more than once. Setting this to the same for two tiles will make certain that only one of the two will appear on the map at any given time.
# Unique = [number] 
''')

f.close()

# Copy and rename maps
path = createfolder(tilename)
copy_and_rename(os.path.join(os.path.dirname(__file__), "RandomMap/map/heightmap.bmp"),path,tilename+"_h.bmp")
copy_and_rename(os.path.join(os.path.dirname(__file__), "RandomMap/map/provinces.bmp"),path,tilename+"_p.bmp")
copy_and_rename(os.path.join(os.path.dirname(__file__), "RandomMap/map/rivers.bmp"),path,tilename+"_r.bmp")

print("Success.")