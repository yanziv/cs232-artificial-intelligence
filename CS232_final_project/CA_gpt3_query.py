import os
import sys
import math
import openai
import csv

openai.api_key = "" #auth token removed for security

def query(text,n=1):
  """Retrieve predictions from GPT-3"""
  response = openai.Completion.create(
  engine="text-davinci-002",
  prompt=text,
  temperature=0.5,
  max_tokens=10,
  top_p=1,
  n=n,
  frequency_penalty=0,
  presence_penalty=0,
  logprobs=5,
  stop="."
)
  return response["choices"]

def addOther(log_prob_dict):
  """Make a log prob dict a probability distribution by adding OTHER category"""
  total = sum([math.exp(v) for v in log_prob_dict.values()])
  other_prob = 1 - total
  log_prob_dict["OTHER"] = math.log(other_prob)
  assert sum([math.exp(v) for v in log_prob_dict.values()]) == 1 #Some probability has been lost if this fails
  return log_prob_dict

def stripKeys(prob_dict):
  """Remove newlines from generated text"""
  keys = list(prob_dict.keys())
  for i,k in enumerate(keys):
    key = k
    if "\n" in key:  #Remove newline characters
      key = key.replace("\n","\\n")
    key = key.strip()
    if key != k:
      prob_dict[key] = prob_dict[k]
      prob_dict.pop(k)
  return prob_dict

def run_one_item(textprompt,n):
  """Run one prompt through GPT-3 and calculate probabilities"""
  responses = query(textprompt,n=n) #Take n samples
  texts = []
  prob_dicts = []
  print(textprompt)
  for r in responses: #For each sample, retrieve the most likely completion (text) and the top 5 words (log_prob_dict)
    text = r["text"].strip().split('\n')[0].strip()
    texts.append(text)
    log_prob_dict = r["logprobs"]["top_logprobs"][0]
    other_dict = addOther(log_prob_dict) #Compute probability of remaining words and add to dictionary
    stripped_dict = stripKeys(other_dict) #Remove newlines and extra space from probable words
    prob_dicts.append(stripped_dict)

  all_log_probs = [i for d in prob_dicts for i in d.items()]
  new_probs = {}
  for k,v in all_log_probs: #Add probabilities across samples
    if k in new_probs:
      new_probs[k] += math.exp(v)
    else:
      new_probs[k] = math.exp(v)

  norm = sum(new_probs.values()) #Re-normalize 
  for k,v in new_probs.items(): 
    new_probs[k] = new_probs[k]/norm #Normalize the probabilities
  assert round(sum(new_probs.values()),5) == 1 #Probabilities do not form a true distribution if this fails
  return new_probs,texts

def export(fn,item_list,prob_dicts,texts):
  """Write data out to file"""
  with open(fn+"_results.tsv",'w') as of:
    writer = csv.writer(of, delimiter='\t')
    for i,item in enumerate(item_list):

      problist = [item for k in sorted(prob_dicts[i].keys()) for item in [k,prob_dicts[i][k]]]
      bits = item+problist+texts[i]
      line = [str(b) for b in bits]
      #print(line)
      writer.writerow(line)

def main():
  infile = sys.argv[1]
  outfile = infile.split('.')[0]
  items = [s.strip().split('\t') for s in open(infile,'r').readlines()]
  results = [run_one_item(item[2].strip(),5) for item in items]
  print("DONE GATHERING RESULTS")
  probs = [r[0] for r in results]
  texts = [r[1] for r in results]
  export(outfile,items,probs,texts)
  

main()