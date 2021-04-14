import Crypto

import DES

# import des

from Crypto.Hash import SHA

from datetime import datetime as dt

from random import randint, sample

from Crypto.Util.Padding import pad

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
#from des import DesKey
from Crypto.Cipher import DES
####  Creating the Block Class  ####
####################################
class Block:
    def __init__(self, index, time, user, transaction, prevHash, nonce):
        self.index = index                      # INDEX OF THE BLOCK
        self.time = time                        # TIME AT THE TIME OF MINING
        self.user = user                      # USER WHO VOTED
        self.transaction = transaction                      # USER'S VOTE
        self.prevHash = prevHash                # HASH OF THE PREVIOUS BLOCK
        self.nonce = nonce                      # NONCE VALUE
        self.currHash = self.hashBlock()        # HASH OF THE CURRENT BLOCK

    def hashBlock(self):
        data = str(self.index) + str(self.time) + str(self.user) + str(self.transaction) + str(self.prevHash) + str(self.nonce)
        hashed = SHA.new(data.encode('utf-8'))
        # hashed.update(data.encode('utf-8'))
        hashed=str(hashed).split(" ")[-1]
        hashed=hashed.rstrip(hashed[-1])
        hashed=hashed.encode()
        print(hashed)
        #DES
        anskey = b"\x13\x34\x57\x79\x9B\xBC\xDF\xF1"
        des = DES.new(anskey, DES.MODE_ECB)
        # print("hello:",str(hashed))
        encryptedtext=des.encrypt(pad(hashed, 64))
        print("ho gaya")
        return encryptedtext

        

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
        self.createBlock(0, time, "None", 0, "0" , 0)

    ######################
    ## CREATE NEW BLOCK ##
    ######################
    def createBlock(self, index, time, user, transaction, prevHash, nonce):
        block = Block(index, time, user, transaction, prevHash, nonce)
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
        testHash.update((str(nonce) + str(prev.index) + str(prev.time) + str(prev.user) + str(prev.transaction) + str(prev.prevHash) + str(prev.nonce)).encode('utf-8'))
        
        while (testHash.hexdigest()[:self.diff] == '0'*self.diff):
            nonce += 1
            testHash.update((str(nonce) + str(prev.index) + str(prev.time) + str(prev.user) + str(prev.transaction) + str(prev.prevHash) + str(prev.nonce)).encode('utf-8'))

        return nonce

    ################################################
    ## MINING THE BLOCK AND ADD TO THE BLOCKCHAIN ##
    ################################################
    def mineBlock(self, user, transaction):
        prevBlock = self.blockchain[-1]
        nonce = self.nonceCalcFunc(prevBlock)
        self.createBlock((prevBlock.index + 1), dt.now(), user, transaction, prevBlock.currHash, nonce)
        print("block ban gaya")


blockchain = Blockchain(2)
blockchain.genesisBlock()

def verifyTransaction(self,x,user):
    blockchain.verify.append( (r+b*x) % (p-1))
    blockchain.verifyIndex = users.index(user)
    if blockchain.verifyTransaction():
        currentUser = user
        Blockchain.mineBlock(self,currentUser,self.transaction)
    else:
        error = 'Invalid User.'
        #dekhte hai.. tata bye bye


def viewUser():
    inputUser = input()
    data=[]
    for block in blockchain.blockchain:
        if block.user == inputUser:
            data.append(block.transaction)
    
    return data

if __name__ == '__main__':
    user = input()
    transaction = input()
    blockchain.mineBlock(user,transaction)
    print("GREAT")

# def mineBlock(user):
#     votedUsers.append(user)
#     userVote.append(request.form['Amethi'] + request.form['Patna'])
#     voter = request.form['currUser']
#     votes = request.form['Amethi'] + request.form['Patna']
#     # print(voter)
#     # print("\n")
#     # print(votes)
#     blockchain.mineBlock(voter, votes)
#     # print(blockchain.blockchain[1].votes)
#     # print(len(blockchain.blockchain))
#     return render_template('login.html')