# -*- coding: utf-8 -*-
"""
Created on Sun Jan 30 02:09:45 2022

@author: SAHIL
"""

# Module 1 - Create a Blockchain



# Importing the libraries
import datetime
import hashlib
import json
from flask import Flask, jsonify
# json is commonly used for transmitting data in web applications (e.g., sending some data from the server to the client, so it can be displayed on a web page, or vice versa)

# Part 1 - Building a Blockchain


#this is a class of blockchain 

class Blockchain:
# this __init__ is a constructor here 
# genesis block is created with create_block function 


    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')
        
        
#here we made a dictionary
#here to get the time we use timestamp by importing datetime 
# proof that we get after proof of work
    def create_block(self, proof, previous_hash):
        #here block is data variable that we used for storing all the information of the new blocks
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block) #this is for appending the new block to our chain 
        return block




#function for getting the previous block 
    def get_previous_block(self):
        return self.chain[-1]  #here -1 is for the left block of the chain 
    
    
    
    
#function for getting the proof of work 
#proof of work is the data that the miners need to find in order to mine the block 
#here we define a problem in proof of work   it will be hard to find and easy to verify
    def proof_of_work(self, previous_proof):
        new_proof = 1  #here we are making it 1 because we try it finding by the value of 1 and then increment the value 
        check_proof = False #to check whether it is a right proof or not here it is initialised to false because initial proof is not the right one 
        #sha256 is a cryptographic function 
        #here encode will encode the string into right format
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()  #here hash operation is a variable
            
            if hash_operation[:4] == '0000': #if first 4 char of this hash operation are 0s or not we can also do it for 50s to make the complex problem for the miners
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    
    
    
    
    #dumps takes the object and makes it a string 
    #and importing dumps from the json 
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    
    
    #here this function will check whether our chain is valid or not
    def is_chain_valid(self, chain):
        previous_block = chain[0]  #first block of the chain  
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
    




# Part 2 - Mining our Blockchain

# Creating a Web App
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Creating a Blockchain
#instance of blockchain 
blockchain = Blockchain()


# Mining a new block

#use the route() decorator to tell Flask what URL should trigger our function.
@app.route('/mine_block', methods = ['GET']) #for mining we just need to use get method
def mine_block():
    previous_block = blockchain.get_previous_block()  #this will give last block of the chain
    previous_proof = previous_block['proof'] 
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash) #that is used for creating the block here blockchain is an instance 
    response = {'message': 'Congratulations!!!, you just mined a block!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200 #200 is just http response for successful http request 200 is for everthing is ok

# Getting the full Blockchain

@app.route('/get_chain', methods = ['GET'])
#that is for displaying the full chain of our blockchain 
def get_chain():
    response = {'chain': blockchain.chain, # this tells what will be displayed when we send a get request 
                'length': len(blockchain.chain)}
    return jsonify(response), 200

# Checking if the Blockchain is valid
@app.route('/is_valid', methods = ['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200

# Running the app
app.run(host = '0.0.0.0', port = 5000)


