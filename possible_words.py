letters_possible = "abcdefghijklmnopqrstuvwxyz" #@param {type:"string"}
letters_definitely = "q" #@param {type:"string"}
letters_position = "??e??" #@param {type:"string"}
show_graph = False #@param {type:"boolean"}

one_random = False #@param {type:"boolean"}

import numpy as np
possible = list(letters_possible) 
position = list(letters_position) 
definitely = list(letters_definitely) 

import urllib.request
url = "https://raw.githubusercontent.com/dwyl/english-words/master/words_alpha.txt"
file = urllib.request.urlopen(url)
list_o_words = [((line.decode('utf-8').strip()).split()) for line in file]
file.close()

list_o_words = np.array(list_o_words)
length = np.char.str_len(list_o_words)
list_o_words = list_o_words[length == 5]
matrix_o_char = np.array([list(w) for w in list_o_words])

words = list_o_words

req = np.ones(len(words)).astype(bool)
i = 0
for L in position:
  if L == '?' or L == ' ':
    pass
  else:
    req = np.logical_and(req, matrix_o_char[:,i] == L)
  i = i+1
words = words[req]
matrix_o_char = matrix_o_char[req]

has = np.ones(len(words)).astype(bool)
for k in definitely:
  if k != ' ':
    has = np.logical_and(has,np.sum(matrix_o_char == k, axis = 1) > 0)
words = words[has]
matrix_o_char = matrix_o_char[has]

hits = np.zeros(len(words))
for l in possible:
  out  = np.sum(matrix_o_char == l, axis = 1)
  hits = hits + out
words = words[hits > 4]
matrix_o_char = matrix_o_char[hits > 4]

if one_random == False:
  print(words)
else:
  ind = int(np.random.rand()*len(words))
  print(words[ind])

if show_graph == True:
  let, count = np.unique(matrix_o_char, return_counts = True)
  ord = let[np.argsort(-count)]
  import matplotlib.pyplot as plt
  plt.bar(ord,count[np.argsort(-count)])
  plt.title('5 letter word charachter frequency')
  plt.show()
