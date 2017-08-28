# import the panda, request, and io library
import pandas as pd
import requests
import io

# get the data from uni prot
r = requests.get("http://www.uniprot.org/uniprot/?query=annotation%3A(type%3Atransmem)%20AND%20(organism%3A%22Homo%20sapiens%20(Human)%20%5B9606%5D%22%20OR%20organism%3A%22Mus%20musculus%20(Mouse)%20%5B10090%5D%22)&sort=score&columns=id%2Ccomment(SUBCELLULAR%20LOCATION)&format=tab")

# Simple expression to find annotation data
def findAnnotation(text):
  text = str(text)
  # Now check for an annotation dictionary
  if text.find("{") != -1:
    return text[text.find("{") + 1: text.find("}")]
  else:
    return "None"

# expression to check for the type of protein
def findType(entry):
  entry = str(entry)
  # Check for single, multi, beta or other
  if entry.find("Single-pass") != -1:
    return "Single-pass membrane protein"
  elif entry.find("Multi-pass") != -1:
    return "Multi-pass membrane protein"
  elif entry.find("Beta-barrel") != -1:
    return "Beta-barrel membrane protein"
  else:
    return "Data unknown"

# read in the table data and set column names
data = pd.read_table(io.StringIO(r.text), header=0, names = ["UniProtId", "Subcellular"])

# Add the type column
data["Type"] = data["Subcellular"].apply(lambda x: findType(x))

# Add the annotation column
data["Annotations"] = data["Subcellular"].apply(lambda x: findAnnotation(x))

# now delete the subcellular column
del data["Subcellular"]

# now write the table to a file
data.to_csv("formatted.tab", index=False, header=True, sep="	")
