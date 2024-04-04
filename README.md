# Readme

Welcome to Tile Generator 0.1. This script takes the output of Haftetavenscrap's World Generator Plus, and turns it into a tile for the EU4 Random World generator. 
The python script has the following dependencies: os, sys, shutil, re and pillow. These can be installed using pip.

First, generate a world with World Generator Plus. Both height and width must be multiples of 128. The sum of all provinces, land, sea and wasteland, must be 1000 or less. I hit the sweet spot of almost 1000 provinces with a 1280*1280 map once.

Adding a region file is recommended. Here's how:
1. Open the provinces map in GIMP, select the color picker and choose the option to "Add to palette". 
2. Open the Palettes tab
3. Create a new palette
4. Each province you pick with the color picker will be added to the palette. It will become the center of a region (and trade region). Provinces around it will be added automatically by the game.
5. When you're finished, go back to the Palettes list. Right click your new palette and Export as... > Text file. Name the file region.txt.

You can optionally follow the same steps and create "level_1_center_of_trade.txt" and/or "river_estuary_modifier.txt" files. The script will look for these two files and add the selected provinces into the final text file to be used by EU4. Provinces with these bonuses have a higher chance of becoming the center of trade for their region.

Place the script in the same folder as the generated world folder and .mod file. Add your palette files alongside it. Then run. The script will prompt you a few times. Extra settings can be set manually in the generated textfile.

The script generates a text file and copies and renames three maps. Place the text file in your EU4 install folder under map\random\tiles. For me, this was "C:\Program Files (x86)\Steam\steamapps\common\Europa Universalis IV\map\random\tiles". Place the three maps inside the data subfolder. You can remove the tiles that come with the game, but definitely leave the water1, water2 and water3 textfiles and associated maps.

## Limitations
* Lakes are not recognised, and will be seas instead. I cannot distinguish them based on any files in the Word Generator output.

## Future plans:
* Have script look for and apply all supplied province modifier palettes.
* Fix lakes.

## Thanks to
* Whoever wrote this guide, highly recommended if you're getting into tiles:  https://forumcontent.paradoxplaza.com/public/131201/Tile%20Making%20-%20an%20introduction.pdf
* Haftetavenscrap