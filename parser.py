# open the data file
file = open("data.tab", "r")

#The IDs start at index 2 every other element
ids = ["UniProtId"]
types = ["Type"]
annotations = ["Annotation"]

#skip the first line
file.readline()

# loop through each line skipping header
for line in file:

  # each entry is separated by a tab
  entries = line.split("	")

  # ID is first
  ids.append(entries[0]);

  # second part is the mixed content
  entry = entries[1]

  # Check for single, multi, beta or other
  if entry.find("Single-pass") != -1:
    types.append("Single-pass membrane protein")
  elif entry.find("Multi-pass") != -1:
    types.append("Multi-pass membrane protein")
  elif entry.find("Beta-barrel") != -1:
    types.append("Beta-barrel membrane protein")
  else:
    types.append("Data unknown")

  # Now check for an annotation dictionary
  if entry.find("{") != -1:
    annotations.append(entry[entry.find("{") + 1: entry.find("}")])
  else:
    annotations.append("None")

# now close the reader
file.close()

# now open the file to write
with open("formatted.tab", "w") as output:
    
  # now loop through all the data
  for a, b, c in zip(ids, types, annotations):
      
    # write the line tab separated
    output.write("	".join([a, b, c]) + "\n")
