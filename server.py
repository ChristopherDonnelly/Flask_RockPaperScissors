'''
Create a site that when a user loads it creates a random number between 1-100 and stores the number in session. Allow the user to guess at the number and tell them when they are too high or too low. If they guess the correct number tell them and offer to play again.

In order to generate a random number you can use the "random" python module:

import random # import the random module

# The random module has many useful functions. This is one that gives a random number in a range
random.randrange(0, 101) # random number between 0-100

In order to remove something from the session, you must "pop" it off of the session dictionary.

# Set session like so:
session['someKey'] = 50

# Remove something from session like so:
session.pop('someKey')\
'''

from flask import Flask, render_template, request, redirect, session
import random

app = Flask(__name__)

app.secret_key = 'RPC_Key'

rpcDict = { 1: 'rock', 2: 'paper', 3: 'scissors' }
rpcDictRev = { 'rock': 1, 'paper': 2, 'scissors': 3 }

@app.route('/')

def index():
  if not 'wlt' in session:
    session['wlt'] = ''
  if not 'wins' in session:
    session['wins'] = 0
  if not 'lose' in session:
    session['lose'] = 0
  if not 'ties' in session:
    session['ties'] = 0
  if not 'color' in session:
    session['color'] = 'black'
    
  session['randomNum'] = random.randrange(1, 4)

  print session['randomNum']

  return render_template("index.html")

@app.route('/rpc', methods=['POST'])

def rpc():
  guess = request.form['submit']
  guess = int(rpcDictRev[guess.lower()])  
  serverGuess = int(session['randomNum'])

  if serverGuess == guess:
    session['ties'] = int(session['ties']) + 1
    session['wlt'] = 'You both picked {} so you have tied!'.format(rpcDict[guess])
    session['color'] = 'black'

  elif (serverGuess == 1 and guess == 2) or (serverGuess == 2 and guess == 3) or (serverGuess == 3 and guess == 1):
    session['wins'] = int(session['wins']) + 1
    session['wlt'] = 'You picked {} and the server picked {} so you have won!'.format(rpcDict[guess], rpcDict[serverGuess])
    session['color'] = 'green'

  elif (serverGuess == 1 and guess == 3) or (serverGuess == 2 and guess == 1) or (serverGuess == 3 and guess == 2):
    session['lose'] = int(session['lose']) + 1
    session['wlt'] = 'You picked {} and the server picked {} so you have lost!'.format(rpcDict[guess], rpcDict[serverGuess])
    session['color'] = 'red'

  return redirect('/')

@app.route('/reset', methods=['POST'])

def reset():
  session.pop('wlt')
  session.pop('wins')
  session.pop('lose')
  session.pop('ties')

  return redirect('/')

app.run(debug=True)