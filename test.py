#################################################
################ ALL THE IMPORTS ################
#################################################
import Crypto
from Crypto.Hash import SHA

from datetime import datetime as dt

import requests
from flask import Flask, jsonify, request, render_template, redirect, url_for, flash
from random import randint, sample


##################################
## NUMERIC VALUES FOR THE VOTES ##
##################################
votedFor = {
    '1010' : "Amethi : Modi and Patna : Obama",
    '1001' : "Amethi : Modi and Patna : Trump",
    '0110' : "Amethi : Rahul and Patna : Obama",
    '0101' : "Amethi : Rahul and Patna : Trump",
}
votedUsers = []
userVote = []

########################
## Values for the ZKP ##
########################
p = 11                                  # PRIME NUMBER
g = 2                                   # GENERATOR
r = sample(range(0,11), 5)              # 5 RANDOM INTEGERS BETWEEN 0 AND (p-1)
b = [randint(0,1) for i in range(5)]    # LIST OF 5 INTEGRS EITHER 0 OR 1


##################
## USER DETAILS ##
##################
# users = ['1', 'f20171602', 'f20171501']
# passwords = ['1', 'chandi', 'shilbi']
users = []
passwords = []
# keys = [1,1,1]
keys = []
# y = [ (pow(g, val)%p) for val in keys]
y = []

####################################
####  Creating the Block Class  ####
####################################
class Block:
    def __init__(self, index, time, voter, votes, prevHash, nonce):
        self.index = index                      # INDEX OF THE BLOCK
        self.time = time                        # TIME AT THE TIME OF MINING
        self.voter = voter                      # USER WHO VOTED
        self.votes = votes                      # USER'S VOTE
        self.prevHash = prevHash                # HASH OF THE PREVIOUS BLOCK
        self.nonce = nonce                      # NONCE VALUE
        self.currHash = self.hashBlock()        # HASH OF THE CURRENT BLOCK

    def hashBlock(self):
        hashed = SHA.new()
        data = str(self.index) + str(self.time) + str(self.voter) + str(self.votes) + str(self.prevHash) + str(self.nonce)
        hashed.update(data.encode('utf-8'))
        return hashed


#########################################
####  Creating the Blockchain Class  ####
#########################################
class Blockchain:
    def __init__(self, diff):
        self.blockchain = []        # STORES THE BLOCKS
        self.diff = diff            # DIFFUCULTY VALUE FOR MINING
        self.verify = []            # (r + b*x)mod(p-1) VALUES FOR THE RESPECTIVE r AND b VALUES
        self.verifyIndex = 0        # INDEX OF THE USERS ACCOUNT TO BE VERIFIED

    ##########################
    ## CREATE GENESIS BLOCK ##
    ##########################
    def genesisBlock(self):
        time = dt.now()
        self.createBlock(0, time, "None", "0000", "0", 0)

    ######################
    ## CREATE NEW BLOCK ##
    ######################
    def createBlock(self, index, time, voter, votes, prevHash, nonce):
        block = Block(index, time, voter, votes, prevHash, nonce)
        self.blockchain.append(block)

    ###########################################
    ## VERIFY IF THE USER IS VALID USING ZKP ##
    ###########################################
    def verifyTransaction(self):
        ret = []
        for i in range(5):
            h = pow(g, r[i])%p
            s = self.verify[i]
            ret.append((pow(g, s)%p) == (h * (pow(y[self.verifyIndex], b[i])%p)))
        
        # print("In Verify Transaction\n")
        # print(ret.count(True))

        if ret.count(True) >= 3:
            return True
        else:
            return False

    ###########################################################
    ## CALCULATE THE NONCE FOR THE CURRENT BLOCK TO BE MINED ##
    ###########################################################
    def nonceCalcFunc(self, block):
        prev = block
        nonce = 0
        
        testHash = SHA.new()
        testHash.update((str(nonce) + str(prev.index) + str(prev.time) + str(prev.voter) + str(prev.votes) + str(prev.prevHash) + str(prev.nonce)).encode('utf-8'))
        
        while (testHash.hexdigest()[:self.diff] == '0'*self.diff):
            nonce += 1
            testHash.update((str(nonce) + str(prev.index) + str(prev.time) + str(prev.voter) + str(prev.votes) + str(prev.prevHash) + str(prev.nonce)).encode('utf-8'))

        return nonce

    ################################################
    ## MINING THE BLOCK AND ADD TO THE BLOCKCHAIN ##
    ################################################
    def mineBlock(self, voter, votes):
        prevBlock = self.blockchain[-1]
        nonce = self.nonceCalcFunc(prevBlock)
        self.createBlock((prevBlock.index + 1), dt.now(), voter, votes, prevBlock.currHash, nonce)



app = Flask(__name__)

blockchain = Blockchain(2)
blockchain.genesisBlock()
# print("#####################")
# print(blockchain.blockchain[0].index)
# print(blockchain.blockchain[0].time)
# print(blockchain.blockchain[0].voter)
# print(blockchain.blockchain[0].votes)
# print(blockchain.blockchain[0].prevHash)
# print(blockchain.blockchain[0].nonce)
# print(blockchain.blockchain[0].currHash.hexdigest())
# print("#####################")


############################
## ROUTE TO THE HOME PAGE ##
############################
@app.route('/')
@app.route('/home')
def home():
    # return redirect(url_for('login'))
    return render_template('login.html')

##############################
## ROUTE TO THE VOTING PAGE ##
##############################
@app.route('/vote/')
def vote():
    return render_template('voting.html')

#############################################################################
## ROUTE TO /login FOR USER AUTHENTICATION AND ROUTES TO VERIFICATION PAGE ##
#############################################################################
@app.route('/login', methods=['POST'])
def login():
    error = None
    if request.method == 'POST':
        currentUser = request.form['username']
        currentUserPass = request.form['password']
        if currentUser in users and currentUserPass in passwords and users.index(currentUser) == passwords.index(currentUserPass):
            return render_template('verify.html', value=currentUser, len = len(r), r = r, b = b)
        else:
            error = 'Invalid Credentials. Please try again.'
            # flash('Invalid Credentials. Please try again.')
            return render_template('login.html', error=error)
            # return render_template('login.html')

##############################################################################
## VERIFY IF THE USER A VALIC USER USING THE EARLIER FUNCTION THAT USES ZKP ##
##############################################################################
@app.route('/verifyTransaction', methods=['GET', 'POST'])
def verifyTransaction():
    if request.method == 'POST':
        blockchain.verify.append( int(request.form['one']) % (p-1))
        blockchain.verify.append( int(request.form['two']) % (p-1))
        blockchain.verify.append( int(request.form['three']) % (p-1))
        blockchain.verify.append( int(request.form['four']) % (p-1))
        blockchain.verify.append( int(request.form['five']) % (p-1))
        blockchain.verifyIndex = users.index(request.form['currUser'])
        # print(blockchain.verifyIndex)
        if blockchain.verifyTransaction():
            currentUser = request.form['currUser']
            return render_template('voting.html', value=currentUser)
        else:
            error = 'Invalid User.'
            return render_template('login.html', error=error)
    return render_template('verify.html')


############################################################################
## ROUTE TO /calculateVote THAT TAKES THE VOTES AND SENDS THEM FOR MINING ##
############################################################################
@app.route('/calculateVote', methods=['POST'])
def calVote():
    if request.method == 'POST':
        votedUsers.append(request.form['currUser'])
        userVote.append(request.form['Amethi'] + request.form['Patna'])
        voter = request.form['currUser']
        votes = request.form['Amethi'] + request.form['Patna']
        # print(voter)
        # print("\n")
        # print(votes)
        blockchain.mineBlock(voter, votes)
        # print(blockchain.blockchain[1].votes)
        # print(len(blockchain.blockchain))
    return render_template('login.html')

########################################################
## ROUTE TO /registration THAT REGISTERS NEW VOTERS ##
########################################################
@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        if request.form['username'] and request.form['password'] and request.form['key']:
            users.append(request.form['username'])
            passwords.append(request.form['password'])
            keys.append(int(request.form['key']))
            y.append((pow(g, int(request.form['key']))%p))
        # print(users)
        # print(passwords)
        # print("\n")
        # print(keys)
        # return render_template(url_for('home'))
    return render_template('registration.html')

#################################################################
## ROUTE TO /viewUser THAT LETS US SEE A PARTCULAR USER'S VOTE ##
#################################################################
@app.route('/viewUser', methods=['GET','POST'])
def viewUser():
    if request.method == 'POST':
        candidate = request.form['username']
        for block in blockchain.blockchain:
            if block.voter == candidate:
                # print("#####################")
                # print(block.index)
                # print(block.time)
                # print(block.voter)
                # print(block.votes)
                # print(block.prevHash)
                # print(block.prevHash.hexdigest())
                # print(block.nonce)
                # print(block.currHash)
                # print(block.currHash.hexdigest())
                # print("#####################")
                # print(blockchain.blockchain)
                candidateVote = votedFor[block.votes]
                return render_template('login.html', val = candidateVote)
        # index = votedUsers.index(candidate)
        # candidateVote = votedFor[userVote[index]]
        # print(candidate)
        # print(candidateVote)
        # return render_template('login.html', val = candidateVote)
    # return render_template('viewUser.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='127.0.0.1', port=5000)
    # app.run(host='0.0.0.0', port=5000)