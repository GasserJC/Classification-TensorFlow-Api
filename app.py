  GNU nano 4.8                                                                                                                   world.py                                                                                                                             
#!/usr/bin/python3

import cgitb
import cgi
import json
cgitb.enable()

print("Content-Type: text/plain\r\n")

def nameGuess( nameToGuess ):
   import numpy as np
   import tensorflow as tf
   from tensorflow import keras
   model = keras.models.load_model("./NameGuess")
   nmLen = 9
   predict_guess = [ nameToGuess ]
   for i in range(0,len(predict_guess)):
      predict_guess[i] = predict_guess[i].zfill(nmLen)
      predict_guess[i]= predict_guess[i].lower()
   if(len(predict_guess[i]) > nmLen):
      predict_guess[i] = predict_guess[i][:nmLen]
   num_predict = [[0 for i in range(nmLen)] for j in range(len(predict_guess))]
   for i in range(0,len(predict_guess)):
      for j in range (0,nmLen):
         num_predict[i][j] = ord(predict_guess[i][j])
         num_predict[i][j] = num_predict[i][j] - 96 # EXP
   num_predict = np.array(num_predict)
   num_predict = (np.arange(26) == num_predict[...,None]).astype(int)
   answer = model.predict(num_predict)
   percentMale = (answer[0][0]) * 100
   percentFemale = (answer[0][1]) * 100
   if(percentMale <= percentFemale):
      return((str(percentFemale) , "F"))
   else:
      return((str(percentMale) , "M"))
arguments = cgi.FieldStorage()

Values = nameGuess(arguments["name"].value)
DictionaryValues = {"Probability":Values[0] ,"Gender":Values[1] }
JSONPackage = json.dumps(DictionaryValues)
print(JSONPackage)















