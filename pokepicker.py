#!/usr/env/python3
# -*- coding: utf-8 -*-

'''A small tool that gives you number, name (German, English and Japanese) and picture for a randomly chosen Pokémon.

This script uses the German site "pokewiki.de" for Data and Image retreival.
CC-BY-SA Karoline "kikithegecko" Busse, kikidergecko@hannover.ccc.de'''

import random, urllib.request, os.path

#this is the source URL for Pokémon retreival
POKESOURCE = "http://pokewiki.de/Spezial:Exportieren/Pok%C3%A9mon-Liste"
SPRITEBASE = "http://www.greenchu.de/sprites/bw/"
POKEBASE = "pokemons.csv"

#extracts Pokémon information from a given source and returns a 2-dimensional array.
def parseSource(source):
   
   #print("Grabbing site...")
   site = urllib.request.urlopen(source)
   data = site.read()
   #print("Site downloaded.")

   # now parse. we only need the table containing the Pokémon information.
   # the table tag used in the source file is enclosed by "{|" and "|}",
   # so we search for those tags and throw away everyting before and after them.
   data = str(data, "utf-8")
   start = data.find("{|")
   end = data.rfind("|}") # starting the search from the end is faster :)
   #print("Table start: " + str(start+2) + " - " + data[start+2])
   #print("Table end: " + str(end) + " - " + data[end])
   data = data[start+2:end]
   #print("Table extracted.")
   
   # now split into rows, those are separated by " | "
   data = data.splitlines()
   #print("Table split in rows.")

   # the rows with Pokémon information have 10 cells each, separated by "||".
   # if a row doesn't, it doesn't contain Pokémon information and we can delete it.
  
   index = 0
   while index < len(data):
      row = data[index].split("||")
      if len(row) == 10:
         index += 1
      else:
         del data[index]

   # now split the rows in cells, so we have a nested array as a representation 
   # of the original table.

   for index in range(len(data)):
      data[index] = data[index].split("||")
      
      # out of the 10 cells, we only need the number (in cell [0] in each row),
      # the Picture (in cell [1]) and the German (cell [2]), English (cell [3])
      # and Japanese romaji transcriptioned (cell [6]) names of the Pokémon.
      
      shortrow = data[index][0:4]
      shortrow.append(data[index][6])
      
      data[index] = shortrow

   return data


# removes any Wiki formatting from the table's contents and replaces internal
# links to Sprite images with absolute URL.
# spriteBaseURL must end with a "/"
def cleanWikiCode(table, spriteBaseURL):
   for row in table:
      # make sure the first cell contains only a number
      row[0] = row[0].strip("| ")
      # remove the link tags from the German name
      row[2] = row[2].strip(" []")
      #replace the sprite Wiki code with an absolute URL to the sprite
      row[1] = spriteBaseURL + row[0] + ".png"

   return table


# saves a 2-dimensional array into a .csv file with a given name
# filename must include a file ending
def saveAsCSV(table, filename):
   
   if os.path.exists(filename):
      print("Warning! File already exists and will be overwritten")

   f = open(filename, "w")
   for row in table:
      row = ";".join(row)
      f.write(row + "\n")
   f.close()

# returns data for a random picked Pokémon
def getRandomPokemon(filename):
   
   try:
      f = open(filename, "r")
   except IOError as e:
      print("Error! File does not exist!")
      return -1

   lines = f.readlines()
   #print(str(len(lines)) + " lines read")
   num = random.randint(0,len(lines)-1)
   entry = lines[num]
   entry = entry.split(";")

   # format: [number, picture, German, English, Japanese]

   print("Your Pokémon:")
   print()
   print("#" + entry[0])
   print("German: " + entry[2])
   print("English: " + entry[3])
   print("Japanese (romaji): " + entry[4])
   print(entry[1])

   f.close()


#---- main program -----


print("P O K É M O N - P I C K E R")
print()
print()
try:
   src = open(POKEBASE,"r")
   src.close()
except IOError:
   print("No Database found. Generating...")
   print()
   db = parseSource(POKESOURCE)
   db = cleanWikiCode(db, SPRITEBASE)
   saveAsCSV(db, POKEBASE)
getRandomPokemon(POKEBASE)
