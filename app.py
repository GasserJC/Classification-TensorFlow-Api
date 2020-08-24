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

from flask import Flask
from flask_restful import Api, Resource, request
from flask import Response, jsonify

app = Flask(__name__)
api = Api(app)

def nameGuess( nameToGuess ):
   import numpy as np
   import tensorflow as tf
   from tensorflow import keras
   
   print( nameToGuess )
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
   print (percentFemale)
   print (percentMale)
   if(percentMale <= percentFemale):
      return((str(percentFemale) + "F"))
   else:
      return((str(percentMale) + "M"))

@app.route('/')
def apiReturn():
   percent = nameGuess(request.args.get("name"))
   gender = percent[len(percent) - 1]
   percent = percent[:len(percent) - 1]

   return jsonify(Gender=gender, Percent=percent)



