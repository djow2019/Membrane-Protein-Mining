# open the data file
with open("data.tab", "r") as file:
  # each entry is separated by a tab
  unparsed = file.read().split("	")

  #The IDs start at index 2 every other element
  ids = unparsed[2::2]

  #list for types and annotations to filter out
  types = []
  annotations = []

  # sort through the type/annotation mix
  for entry in unparsed[3::2]:

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

  # now open the file to write
  with open("formatted.tab", "w") as output:
    
    # write the header
    header = ["UniProtID", "Type", "Annotation"]
    output.write("	".join(header))

    # now loop through all the data
    for a, b, c in zip(ids, types, annotations):
      
      # write the line tab separated
      output.write("	".join([a, b, c]))
