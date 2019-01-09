difficulty=3
class Node:
    def __init__(self, network, genesis, uuid=None):
        self.chain=BlockChain([genesis])
        self.uuid=uuid or str(uuid4())
        self.network=network
        
    def work(self, verbose=False):
        while True:
            if not self.mine():
                sleep(0.1) # wait due to no transactions
            else:
                if verbose: print(self.uuid, "Mined a block")
            if self.add_block():
                if verbose: print(self.uuid, "Added one block")
            self.network.post_chain(self.chain, self.uuid) # publish my blockchain
            if self.resolve_conflicts():
                if verbose: print(self.uuid, "Change chain")
    
    def mine(self):
        transactions=self.network.get_transactions(self.uuid)
        if len(transactions)==0:
            return False # cannot mine due to no transactions
        previous_hash=self.chain[-1].hash()
        block=Block(time(), tuple(transactions), previous_hash)
        
        for i, n in enumerate(self.random_generator()):
            block.nonce=n
            if self.verify_proof(block):
                break
                
            if i % 100 == 0 and self.add_block(): # someone mined a block
                return True
            if i % 100 == 0 and self.resolve_conflicts(): # someone mined a block
                return True
                
        self.network.broadcast_block(block, self.uuid)
        return True # successfully mined
    
    @staticmethod
    def random_generator(step=None):
        step = step or random.randint(1e4, 1e5)
        for c in count():
            for i in random.sample(range(c*step, (c+1)*step), step):
                yield i
        
    def add_block(self):
        for block in self.network.get_blocks(self.uuid):
            if self.verify_block(block):
                self.chain.append(block)
                if self.verify_chain(self.chain):
                    return True 
                else:
                    self.chain.pop(-1)
        return False # no block is added
    
    def resolve_conflicts(self):
        """Longest valid chain is authoritative"""
        authoritative_chain=self.chain
        for chain in self.network.get_neighbour_chains(self.uuid):
            if not self.verify_chain(chain):
                # node is incorrect
                continue
            if len(chain)>len(authoritative_chain):
                # Longest valid chain is authoritative
                authoritative_chain=deepcopy(chain)
        self.chain=authoritative_chain
        return self.chain is not authoritative_chain
        
    @staticmethod
    def verify_transaction(transaction):
        if transaction.sign is None:
            return False
        h=SHA.new(transaction.str_data().encode())
        verifier=PKCS1_v1_5.new(encode_key(transaction.sender_address))
        return verifier.verify(h, binascii.unhexlify(transaction.sign))
    
    @staticmethod
    def verify_proof(block):
        return block.hash()[:difficulty] == "0" * difficulty
    
    def verify_block(self, block) -> bool:
        is_correct_transactions = all(map(self.verify_transaction, block.transactions))
        is_correct_proof = self.verify_proof(block)
        return is_correct_transactions and is_correct_proof
    
    def verify_chain(self, chain):
        for i in range(len(chain)-1, 0, -1):
            if not self.verify_block(chain[i]):
                return False
            if chain[i-1].hash() != chain[i].previous_hash:
                return False
        return True
