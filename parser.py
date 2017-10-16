
# coding: utf-8

# In[133]:

# %load parser.py
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


# In[151]:

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
data = pd.read_table(io.StringIO(r.text), header=0, names = ["UniProtID", "Reference"])

# Add the type column
data["Type"] = data["Reference"].apply(lambda x: findType(x))

# Add the annotation column
data["Annotations"] = data["Reference"].apply(lambda x: findAnnotation(x))


# In[135]:

# now use mygene to add additional IDs
mg = mygene.MyGeneInfo()
out = mg.querymany(data["UniProtID"], scopes='uniprot', fields='entrezgene,ensembl.gene,refseq,symbol,taxid', returnall=True)


# In[136]:

def getTax(value):
    # Value might be not found, so treat as string
    value = str(value)
    if value == "9606":
        return "Human"
    elif value == "10090":
        return "Mouse"
    else:
        return "Unknown"


# In[137]:

#create a separate dictionary for duplicates
duplicates = {}
for k, v in out["dup"]:
    duplicates[k] = v

# whether or not an entry is unique
def isUnique(item):
    
    # iterate through list of duplicates
    for k, v in duplicates.items():
        if item == k:
            if v > 1:
                duplicates[k] = 1
                return True
            else:
                return False
    return True

#filter out duplicates
parsed = [entry for entry in  out["out"] if isUnique(entry["query"])]


# In[152]:

data["EntrezID"] = pd.Series(map(lambda d: d.get('entrezgene', 'Not Found'), parsed))
data["EnsemblID"] = pd.Series(map(lambda d: d.get('ensembl', 'Not Found'), parsed))
data["RefSeqID"] = pd.Series(map(lambda d: d.get('refseq', 'Not Found'), parsed))
data["Symbol"] = pd.Series(map(lambda d: d.get('symbol', 'Not Found'), parsed))
data["TaxID"] = pd.Series(map(lambda d: getTax(d.get('taxid', 'Not Found')), parsed))


# In[153]:

# now write the table to a file
data.to_csv("formatted.tab", index=False, header=True, sep="	")


# In[154]:

data


# In[ ]:



