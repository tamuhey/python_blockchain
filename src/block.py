@dataclass
class Block:
    time: float
    transactions: Tuple[Transaction]
    previous_hash: str
    nonce: int = None
        
    def json_dumps(self) -> str:
        dct=dc.asdict(self)
        dct["transactions"]=[t.json_dumps() for t in self.transactions]
        return json.dumps(dct)
    
    @classmethod
    def json_loads(cls, string) -> Block:
        dct=json.loads(string)
        dct["transactions"]=tuple([Transaction.json_loads(t) for t in dct["transactions"]])
        return cls(**dct)
        
    def hash(self): 
        block_bytes=self.json_dumps().encode()
        return hashlib.sha256(block_bytes).hexdigest()
