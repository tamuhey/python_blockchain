class Network:
    def __init__(self, neighbours=()):
        self.manager=mp.Manager()
        self.chains=self.manager.dict()
        self.blocks=self.manager.dict()
        self.transactions=self.manager.dict()
        self.neighbours=dict(neighbours)
        
    def post_chain(self, chain, uuid):
        self.chains[uuid]=chain.json_dumps()
    
    def get_chain(self, uuid) -> BlockChain:
        if uuid not in self.chains:
            return []
        return BlockChain.json_loads(self.chains[uuid])
    
    def get_neighbour_chains(self, uuid) -> List[BlockChain]:
        return [self.get_chain(neigh) for neigh in self.neighbours[uuid] if neigh != uuid]
    
    def post_block(self, block, uuid):
        if uuid not in self.blocks:
            self.blocks[uuid]=self.manager.list([block.json_dumps()])
        else:
            self.blocks[uuid].append(block.json_dumps())
            
    def broadcast_block(self, block, uuid):
        for receiver in self.neighbours[uuid]:
            self.post_block(block, receiver)
            
    def get_blocks(self, uuid) -> List[Block]:
        if uuid not in self.blocks:
            return []
        res=[Block.json_loads(s) for s in self.blocks[uuid]]
        self.blocks[uuid][:]=[]
        return res
    
    def post_transaction(self, transaction, uuid):
        if uuid not in self.transactions:
            self.transactions[uuid]=self.manager.list([transaction.json_dumps()])
        else:
            self.transactions[uuid].append(transaction.json_dumps())
            
    def get_transactions(self, uuid) -> Tuple[Transaction]:
        if uuid not in self.transactions:
            return []
        res=[Transaction.json_loads(s) for s in self.transactions[uuid]]
        self.transactions[uuid][:]=[]
        return res
    
    def shutdown(self):
        self.manager.shutdown()
