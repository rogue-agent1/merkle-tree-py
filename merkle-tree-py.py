#!/usr/bin/env python3
"""Merkle tree with proof generation and verification."""
import sys,hashlib

def h(data):return hashlib.sha256(data.encode() if isinstance(data,str) else data).hexdigest()

class MerkleTree:
    def __init__(self,leaves):
        self.leaves=[h(l) for l in leaves]
        self.tree=self._build()
    def _build(self):
        layer=list(self.leaves)
        tree=[layer]
        while len(layer)>1:
            if len(layer)%2:layer.append(layer[-1])
            layer=[h(layer[i]+layer[i+1]) for i in range(0,len(layer),2)]
            tree.append(layer)
        return tree
    @property
    def root(self):return self.tree[-1][0] if self.tree else None
    def proof(self,index):
        proof=[];idx=index
        for layer in self.tree[:-1]:
            if idx%2==0:sibling=layer[idx+1] if idx+1<len(layer) else layer[idx];side='R'
            else:sibling=layer[idx-1];side='L'
            proof.append((sibling,side));idx//=2
        return proof
    @staticmethod
    def verify(leaf,proof,root):
        current=h(leaf)
        for sibling,side in proof:
            if side=='L':current=h(sibling+current)
            else:current=h(current+sibling)
        return current==root

def main():
    if len(sys.argv)>1 and sys.argv[1]=="--test":
        data=["tx1","tx2","tx3","tx4"]
        mt=MerkleTree(data)
        assert mt.root is not None
        # Proof for tx2
        proof=mt.proof(1)
        assert MerkleTree.verify("tx2",proof,mt.root)
        assert not MerkleTree.verify("fake",proof,mt.root)
        # All leaves verifiable
        for i,d in enumerate(data):
            p=mt.proof(i);assert MerkleTree.verify(d,p,mt.root),f"Failed for {d}"
        # Different data = different root
        mt2=MerkleTree(["a","b","c","d"])
        assert mt2.root!=mt.root
        print("All tests passed!")
    else:
        mt=MerkleTree(["tx1","tx2","tx3","tx4"])
        print(f"Root: {mt.root[:16]}...")
if __name__=="__main__":main()
