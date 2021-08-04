import stanza
from whoosh import index
from whoosh.fields import Schema, TEXT, ID, STORED
from whoosh.qparser import QueryParser
import json

nlp = stanza.Pipeline('en', processors='tokenize, pos')

with open('2021_automatic_evaluation_topics_v1.0.json') as json_file:
  data = json.load(json_file)



schema = Schema(content=TEXT(stored=True), id=ID(stored=True))


ix = index.create_in("indexdir", schema)
ix = index.open_dir("indexdir")
writer = ix.writer()

number = data[0]["number"]

for i in range(10):
  turn = data[0]["turn"][i]
  writer.add_document(content=turn["passage"],
                      id=(f"{number}_{turn['number']}"))

writer.commit()

s = ix.searcher()

qp = QueryParser("content", schema=schema)



input = "Does freezing work for breast cancer?"

doc = nlp(input)

input_nouns=[]

for sent in doc.sentences:
  for word in sent.words:
    if word.upos == 'NOUN':
      input_nouns.append(word.text)

# for i, sentence in enumerate(doc.sentences):
#   print(f'====== Sentence {i+1} tokens =======')
#   print(*[f'id: {token.id}\ttext: {token.text}' for token in sentence.tokens], sep='\n')
#   print(*[f'word: {word.text}\tupos: {word.upos}\txpos: {word.xpos}\tfeats: {word.feats if word.feats else "_"}' for sent in doc.sentences for word in sent.words], sep='\n')

scores = {}

for noun in input_nouns:
  q = qp.parse(noun)
  results = s.search(q)
  print(noun)
  if results:
    for i in range(min(len(results), 5)):
      if results[i]['id'] in scores:
        scores[results[i]['id']] += (5 - i)
      else:
        scores[results[i]['id']] = (5 - i)

print(scores)




# print(results[0])







