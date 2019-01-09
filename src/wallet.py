class Wallet:
    def __init__(self, network, nodes=None):
        key=RSA.generate(1024)
        self.private_key = decode_key(key)
        self.address = decode_key(key.publickey())
        self.network=network
        self.nodes=nodes or []
    
    def sign_transaction(self, transaction):
        signer=PKCS1_v1_5.new(encode_key(self.private_key))
        h=SHA.new(transaction.str_data().encode())
        return dc.replace(transaction, sign=signer.sign(h).hex())
    
    def send(self, receiver_address, value):
        transaction=Transaction(self.address, receiver_address, value)
        self.broadcast(self.sign_transaction(transaction))
    
    def broadcast(self, transaction):
        for uuid in self.nodes:
            self.network.post_transaction(transaction, uuid)
