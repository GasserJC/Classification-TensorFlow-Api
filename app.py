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

if __name__ == '__main__':
   app.run()
