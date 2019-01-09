class BlockChain(list):
    def json_dumps(self) -> str:
        return json.dumps([block.json_dumps() for block in self])
    @classmethod
    def json_loads(cls, string) -> BlockChain:
        return cls([Block.json_loads(s) for s in json.loads(string)])
