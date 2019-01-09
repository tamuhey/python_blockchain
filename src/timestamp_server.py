class TimestampServer:
    def __init__(self):
        key=RSA.generate(1024)
        self.public_key=key.publickey()
        self.signer=PKCS1_v1_5.new(key)
        
        genesis=Block(time(), (), "0")
        self.block_chain=[genesis]
        
    def generate_block(self, transactions: Sequence[Transaction]):
        # generate block
        block=Block(time(), tuple(transactions), self.block_chain[-1].hash())
        
        # sign the block
        dct=dc.asdict(block)
        del dct["sign"]
        block.sign=self.signer.sign(SHA.new(json.dumps(dct).encode())).hex()
        
        # publish the block
        self.block_chain.append(block)
