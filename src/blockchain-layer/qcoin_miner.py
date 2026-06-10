#!/usr/bin/env python3
"""
QCoin Basic PoW Miner Prototype
Part of Nexus Project - QCoin/XCoin Blockchain Layer

A minimal, educational Proof-of-Work miner and simple blockchain implementation.
Run this to start 'mining' QCoin locally for testing and understanding.

Not for production use. Expand in src/blockchain-layer/ for full node, P2P, wallet, mesh integration.

Usage:
  python qcoin_miner.py --help
  python qcoin_miner.py --difficulty 4 --blocks 10 --reward 50 --miner-address QMinerDemo

Author context: Starter for Sven Normen Esslinger's Nexus ecosystem (xMesh, AI swarms, QNET).
"""

import argparse
import hashlib
import json
import time
from datetime import datetime
from typing import List, Dict, Any

class Block:
    def __init__(self, index: int, timestamp: float, transactions: List[Dict], previous_hash: str, nonce: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Compute SHA256 hash of block header (simplified, no Merkle for starter)."""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty: int) -> None:
        """Perform PoW: increment nonce until hash has 'difficulty' leading zeros."""
        target = '0' * difficulty
        print(f"Mining block #{self.index} with difficulty {difficulty}...")
        start_time = time.time()
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
            if self.nonce % 100000 == 0:  # Progress every 100k attempts
                print(f"  Nonce: {self.nonce}, current hash: {self.hash[:16]}...")
        end_time = time.time()
        print(f"Block #{self.index} mined! Nonce: {self.nonce}, Hash: {self.hash}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")


class QCoinBlockchain:
    def __init__(self, difficulty: int = 4, block_reward: float = 50.0):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.block_reward = block_reward
        self.miner_address = "QGenesis"
        self.create_genesis_block()

    def create_genesis_block(self) -> None:
        """Create the first block in the chain."""
        genesis_transactions = [{
            'from': 'QCoinNetwork',
            'to': self.miner_address,
            'amount': 1000000,  # Large genesis allocation for testing/treasury
            'note': 'Genesis allocation for Nexus development and initial incentives'
        }]
        genesis_block = Block(0, time.time(), genesis_transactions, '0' * 64)
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        print("Genesis block created and mined.")

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def add_block(self, transactions: List[Dict]) -> Block:
        """Add a new block with given transactions (incl. coinbase)."""
        previous_block = self.get_latest_block()
        # Add coinbase reward transaction
        coinbase_tx = {
            'from': 'QCoinNetwork',
            'to': self.miner_address,
            'amount': self.block_reward,
            'note': f'Block reward for miner {self.miner_address}'
        }
        all_txs = [coinbase_tx] + transactions
        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=all_txs,
            previous_hash=previous_block.hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self) -> bool:
        """Validate the entire chain (hashes and links)."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.calculate_hash():
                print(f"Invalid hash at block {i}")
                return False
            if current.previous_hash != previous.hash:
                print(f"Invalid previous hash link at block {i}")
                return False
        return True

    def get_balance(self, address: str) -> float:
        """Simple balance calculation by scanning all txs (demo only)."""
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.get('to') == address:
                    balance += tx.get('amount', 0)
                if tx.get('from') == address:
                    balance -= tx.get('amount', 0)
        return balance


def main():
    parser = argparse.ArgumentParser(description='QCoin Basic PoW Miner - Nexus Project Starter')
    parser.add_argument('--difficulty', type=int, default=4, help='PoW difficulty (leading zeros, 1-6 recommended for demo)')
    parser.add_argument('--blocks', type=int, default=5, help='Number of additional blocks to mine after genesis')
    parser.add_argument('--reward', type=float, default=50.0, help='Block reward in QCoin')
    parser.add_argument('--miner-address', type=str, default='QDemoMiner', help='Miner address to receive rewards')
    parser.add_argument('--simulate-txs', action='store_true', help='Add some example transactions between blocks')
    args = parser.parse_args()

    print("=" * 60)
    print("QCOIN MINING STARTER - NEXUS PROJECT")
    print("Blockchain layer prototype for mesh + AI + hardware ecosystem")
    print(f"Miner: {args.miner_address} | Difficulty: {args.difficulty} | Reward: {args.reward} QC")
    print("=" * 60)

    blockchain = QCoinBlockchain(difficulty=args.difficulty, block_reward=args.reward)
    blockchain.miner_address = args.miner_address  # Update for rewards

    print(f"\nGenesis balance for {args.miner_address}: {blockchain.get_balance(args.miner_address)} QC")

    example_txs = [
        {'from': 'QDemoMiner', 'to': 'QRecipient1', 'amount': 10, 'note': 'Test transfer'},
        {'from': 'QDemoMiner', 'to': 'QRecipient2', 'amount': 5, 'note': 'Another tx'}
    ]

    for i in range(args.blocks):
        txs_to_add = example_txs if args.simulate_txs and i % 2 == 0 else []
        print(f"\n--- Mining block {i+1} ---")
        block = blockchain.add_block(txs_to_add)
        print(f"Chain length: {len(blockchain.chain)}")
        if args.simulate_txs:
            print(f"  Included demo txs. New balance: {blockchain.get_balance(args.miner_address)} QC")

    print("\n" + "=" * 60)
    print("MINING COMPLETE")
    print(f"Final chain length: {len(blockchain.chain)} blocks")
    print(f"Final balance for {args.miner_address}: {blockchain.get_balance(args.miner_address)} QC")
    print(f"Chain valid: {blockchain.is_chain_valid()}")
    print("=" * 60)

    # Optional: Print last block details
    last_block = blockchain.get_latest_block()
    print(f"\nLast block hash: {last_block.hash}")
    print(f"Last block nonce: {last_block.nonce}")
    print("\nTip: Increase --difficulty for harder/longer mining (demo only; real chains use adjustment algos).")
    print("Next: Integrate P2P (Yggdrasil), add tx signing, persist to disk, connect to your mesh!")


if __name__ == "__main__":
    main()
