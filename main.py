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
r  = 0          # 5 RANDOM INTEGERS BETWEEN 0 AND (p-1)
b  = 0 # LIST OF 5 INTEGRS EITHER 0 OR 1
y = 0


open_transactions=[]
success_transactions=[]
##################
## USER DETAILS ##
##################
# users = ['1', 'f20171602', 'f20171501']
# passwords = ['1', 'chandi', 'shilbi']
# users = []
# transactions = []
# keys = [1,1,1]
# keys = []
# y = [ (pow(g, val)%p) for val in keys]
# y = []

####################################
#from des import DesKey
from Crypto.Cipher import DES
####  Creating the Block Class  ####
####################################
class Block:
    def __init__(self, index, time, transaction, prevHash, nonce):
        self.index = index                      # INDEX OF THE BLOCK
        self.time = time                        # TIME AT THE TIME OF MINING
        self.transaction = transaction                      # USER'S VOTE
        self.prevHash = prevHash                # HASH OF THE PREVIOUS BLOCK
        self.nonce = nonce                      # NONCE VALUE
        self.currHash = self.hashBlock()        # HASH OF THE CURRENT BLOCK

    def hashBlock(self):
        data = str(self.index) + str(self.time) + str(self.transaction) + str(self.prevHash) + str(self.nonce)
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
        print("ho gaya :",encryptedtext)
        return encryptedtext

        

#########################################
####  Creating the Blockchain Class  ####
#########################################
class Blockchain:
    def __init__(self, diff):
        # self.transactions = []  
        self.blockchain = []        # STORES THE BLOCKS
        self.diff = diff            # DIFFUCULTY VALUE FOR MINING

    ##########################
    ## CREATE GENESIS BLOCK ##
    ##########################
    def genesisBlock(self):
        time = dt.now()
        trans=[]
        self.createBlock(0, time, trans, "0" , 0)

    ######################
    ## CREATE NEW BLOCK ##
    ######################
    def createBlock(self, index, time, transaction, prevHash, nonce):
        block = Block(index, time, transaction, prevHash, nonce)
        self.blockchain.append(block)

    ###########################################################
    ## CALCULATE THE NONCE FOR THE CURRENT BLOCK TO BE MINED ##
    ###########################################################
    def nonceCalcFunc(self, block):
        prev = block
        nonce = 0
        
        testHash = SHA.new()
        testHash.update((str(nonce) + str(prev.index) + str(prev.time)+ str(prev.transaction) + str(prev.prevHash) + str(prev.nonce)).encode('utf-8'))
        
        while (testHash.hexdigest()[:self.diff] == '0'*self.diff):
            nonce += 1
            testHash.update((str(nonce) + str(prev.index) + str(prev.time)+ str(prev.transaction) + str(prev.prevHash) + str(prev.nonce)).encode('utf-8'))
            # testHash.update((str(prev.prevHash) + str(prev.nonce)).encode('utf-8'))
        print("test: ",testHash)
        return nonce

    ################################################
    ## MINING THE BLOCK AND ADD TO THE BLOCKCHAIN ##
    ################################################
    def mineBlock(self,mineArr):
        prevBlock = self.blockchain[-1]
        nonce = self.nonceCalcFunc(prevBlock)

        self.createBlock((prevBlock.index + 1), dt.now(), open_transactions, prevBlock.currHash, nonce)
        print("block ban gaya")


blockchain = Blockchain(2)
blockchain.genesisBlock()

def verifyTransaction():
    mineArr=[]
    print("In verifyTransaction: ",open_transactions," ",len(open_transactions))

    for i in range(len(open_transactions)):
        r=randint(0,p-1)         
        b=randint(0,1)
        amount=int(open_transactions[i]['amount'])
        y=pow(g,amount)%p
        # print(type(amount))

        s=(r+b*amount) % (p-1)
        h = pow(g,r)%p
        if (pow(g, s)%p) == (h * (pow(y, b)%p)):
            mineArr.append(open_transactions[i])
        else:
            print("The transaction ",open_transactions[i]," is invalid")

    if len(mineArr)>0:
        blockchain.mineBlock(mineArr)
        print("Valid Transactions mined")
    else:
        print("No transaction to mine")


def viewUser():
    inputUser = input("Input user's name: ")
    data=[]
    for block in blockchain.blockchain:
        for x in block.transaction:
            if x['sender'] == inputUser:
                data.append(x)
    
    print(data)

def get_transaction():
    sender = input("Input sender's name: ")
    recipient = input("Input recipient's name: ")
    amount = input("Enter the transaction amount: ")

    transaction = {'sender': sender,
                    'recipient': recipient,
                    'amount': amount}
    return transaction,sender

def printFullBlockchain():
    for i in range(len(blockchain.blockchain)):
        print("Details of block ",i," are:")
        print("\tTime=",blockchain.blockchain[i].time)
        print("\tTransactions=",blockchain.blockchain[i].transaction)
        print("\tPrevious block Hash=",blockchain.blockchain[i].prevHash)
        print("\tCurrent block Hash=",blockchain.blockchain[i].currHash)
        print("\tNonce=",blockchain.blockchain[i].nonce)


if __name__ == '__main__':
    while(True):
        print("Enter your choice:")
        print("0: Do a transaction")
        print("1: Verify transaction and then mine block")
        print("2: View user")
        print("3: Print full blockchain")
        print("4: Exit")

        st=input()
        if st=='0':
            transaction,sender=get_transaction()
            open_transactions.append(transaction)
            print(open_transactions)
            #save_data()
            #baad me (11 pm se pehle)
        elif st=='1':
            verifyTransaction()
            open_transactions=[]
            r=0
            b=0
            y=0
        elif st=='2':
            viewUser()
        elif st=='3':
            printFullBlockchain()
        elif st=='4':
            break
        else:
            print("Please choose from the following")
        
        
    print("Ho gaya.. GG")