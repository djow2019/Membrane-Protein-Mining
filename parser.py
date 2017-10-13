# import the panda, request, io, and mygene libraries
import pandas as pd
import requests
import io
import mygene

# construct the query data
query = {

  "query": "annotation:(type:transmem) (organism:\"Homo sapiens (Human) [9606]\" OR organism:\"Mus musculus (Mouse) [10090]\")",
  "columns":"id,comment(SUBCELLULAR LOCATION)",
  "format": "tab"

}

# get the data from uni prot
r = requests.get("http://www.uniprot.org/uniprot/", params = query)

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

# now use mygene to add additional IDs
mg = mygene.MyGeneInfo()
out = mg.querymany(data["UniProtId"], scopes='uniprot', fields='entrezgene,ensembl.gene,refseq,symbol')
data["EntrezID"] = pd.Series(map(lambda d: d.get('entrezgene', 'Not Found'), out))
data["EnsembleID"] = pd.Series(map(lambda d: d.get('ensembl', 'Not Found'), out))
data["RefSeqID"] = pd.Series(map(lambda d: d.get('refseq', 'Not Found'), out))
data["Symbol"] = pd.Series(map(lambda d: d.get('symbol', 'Not Found'), out))

# now write the table to a file
data.to_csv("formatted.tab", index=False, header=True, sep="	")
