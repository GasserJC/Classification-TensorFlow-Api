#!/usr/bin/python3
#Purpose: Use Research Apprenticeship Developed TensorFlow Model NameGuess.py via a Web API hosted on the cloud with a load balancer.
#Processes:
#Pull Arguments from the URL, should contain one argument of name.
#Name is to be given to the nameGuess Function which fits the data using numpy, keras, and tensorflow to infer from the model.
#Model Inference Works as follows: (FOR MORE INFORMATION CHECK MY NAMEGUESS REPO)
#   a) String Standardization = Trim name length to 9 then zero fill the char array for any open spaces and change all to lower case
#   b) Char to Int converstion = Change all chars to ascii values, then translate values such that a = 0
#   c) One Hot Encoding = change an individual ascii value to its unique one hot encode, this changes the data's dimension to 2 Dimensions
#   d) Name has now been converted to acceptable input, infer from the model and return the probabilities for M or F
#Return 2 Arguments, Porbability of more likely Gender, and the more likely Gender.
#JSON encode the data
#Return the JSON data to the browser

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
   
   #String Manipulation
   for i in range(0,len(predict_guess)):
      predict_guess[i] = predict_guess[i].zfill(nmLen)
      predict_guess[i]= predict_guess[i].lower()
   if(len(predict_guess[i]) > nmLen):
      predict_guess[i] = predict_guess[i][:nmLen]
      
   #Char to Int
   num_predict = [[0 for i in range(nmLen)] for j in range(len(predict_guess))]
   for i in range(0,len(predict_guess)):
      for j in range (0,nmLen):
         num_predict[i][j] = ord(predict_guess[i][j])
         num_predict[i][j] = num_predict[i][j] - 96 # EXP
   #Int to One Hot Encoding 2-D Array
   num_predict = np.array(num_predict)
   num_predict = (np.arange(26) == num_predict[...,None]).astype(int)
   
   #Model Inference
   answer = model.predict(num_predict)
   percentMale = (answer[0][0]) * 100
   percentFemale = (answer[0][1]) * 100
   if(percentMale <= percentFemale):
      return((str(percentFemale) , "F"))
   else:
      return((str(percentMale) , "M"))
arguments = cgi.FieldStorage()


#Initial Code Execution
Values = nameGuess(arguments["name"].value) #Grab Arguments from URL then call TF Model Inference
DictionaryValues = {"Probability":Values[0] ,"Gender":Values[1] } #Change TF Model Array to Dictionary
JSONPackage = json.dumps(DictionaryValues) #Change Dictionary to JSON Package
print(JSONPackage) #Return JSON Package















