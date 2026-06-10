#!/usr/bin/env python3
"""
QCoin Enhanced PoW Miner Prototype (v0.2)
Part of Nexus Project - QCoin/XCoin Blockchain & Economic Layer

Educational yet functional Proof-of-Work miner with:
- Dynamic difficulty adjustment
- JSON chain persistence (save/load)
- Hashrate estimation and improved stats
- Coinbase rewards + demo transactions
- Full chain validation

Run standalone for local testing or as starting point for mesh-integrated nodes.

Not production-ready. Expand into qcoin_core.py + full node/wallet for real deployment.

Usage examples:
  python qcoin_miner.py --help
  python qcoin_miner.py --difficulty 4 --blocks 5 --miner-address SvenQMiner
  python qcoin_miner.py --difficulty 3 --blocks 10 --simulate-txs --persist my_chain.json
  python qcoin_miner.py --load my_chain.json --blocks 3

Context: Starter for Sven Normen Esslinger's Nexus ecosystem
(xMesh/NovaNet/QNET mesh + AI swarms + hardware prototypes).
"""

import argparse
import hashlib
import json
import time
from datetime import datetime
from typing import List, Dict, Any, Optional


class Block:
    """Represents a single block in the QCoin blockchain."""
    def __init__(self, index: int, timestamp: float, transactions: List[Dict],
                 previous_hash: str, nonce: int = 0, difficulty: int = 4):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.difficulty = difficulty
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """SHA256 hash of the block header (JSON-serialized for simplicity)."""
        block_header = {
            'index': self.index,
            'timestamp': self.timestamp,
            'transactions': self.transactions,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce,
            'difficulty': self.difficulty
        }
        block_string = json.dumps(block_header, sort_keys=True).encode('utf-8')
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty: Optional[int] = None) -> float:
        """Perform Proof-of-Work by incrementing nonce until hash meets difficulty target.
        Returns approximate hashrate (hashes per second)."""
        if difficulty is None:
            difficulty = self.difficulty
        target = '0' * difficulty
        print(f"  Mining block #{self.index} (difficulty={difficulty})...")
        self.nonce = 0
        start_time = time.time()
        hashes_tried = 0
        last_report = start_time

        while self.hash[:difficulty] != target:
            self.nonce += 1
            hashes_tried += 1
            self.hash = self.calculate_hash()

            # Progress report every ~2 seconds or 200k hashes
            now = time.time()
            if now - last_report > 2.0 or self.nonce % 200000 == 0:
                elapsed = now - start_time
                hps = hashes_tried / elapsed if elapsed > 0 else 0
                print(f"    Nonce: {self.nonce:,} | Hash: {self.hash[:16]}... | ~{hps:,.0f} H/s")
                last_report = now

        end_time = time.time()
        elapsed = end_time - start_time
        hashrate = hashes_tried / elapsed if elapsed > 0 else 0
        print(f"  ✓ Block #{self.index} mined! Nonce={self.nonce:,} | {hashrate:,.0f} H/s | {elapsed:.2f}s")
        return hashrate


class QCoinBlockchain:
    """Simple blockchain with PoW mining, dynamic difficulty, and persistence."""
    def __init__(self, difficulty: int = 4, block_reward: float = 50.0,
                 target_block_time: float = 60.0, adjust_every: int = 5):
        self.chain: List[Block] = []
        self.difficulty = difficulty
        self.block_reward = block_reward
        self.target_block_time = target_block_time
        self.adjust_every = adjust_every
        self.miner_address = "QGenesis"
        self.total_hashes = 0
        self.total_time = 0.0

    def create_genesis_block(self) -> None:
        """Create and mine the genesis block."""
        genesis_txs = [{
            "from": "QCoinNetwork",
            "to": self.miner_address,
            "amount": 1_000_000,
            "note": "Genesis allocation - Nexus development & initial incentives"
        }]
        genesis = Block(0, time.time(), genesis_txs, "0" * 64, difficulty=self.difficulty)
        hashrate = genesis.mine_block()
        self.chain.append(genesis)
        self.total_hashes += genesis.nonce
        print(f"Genesis block created (hashrate ~{hashrate:,.0f} H/s).\n")

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def adjust_difficulty(self, actual_times: List[float]) -> int:
        """Simple dynamic difficulty adjustment.
        Target: keep average block time close to self.target_block_time.
        Adjusts every self.adjust_every blocks."""
        if len(actual_times) == 0:
            return self.difficulty

        avg_time = sum(actual_times) / len(actual_times)
        if avg_time < self.target_block_time * 0.7:
            new_diff = self.difficulty + 1
        elif avg_time > self.target_block_time * 1.5:
            new_diff = max(1, self.difficulty - 1)
        else:
            new_diff = self.difficulty

        if new_diff != self.difficulty:
            print(f"  Difficulty adjustment: {self.difficulty} → {new_diff} (avg block time {avg_time:.1f}s)")
        return new_diff

    def add_block(self, transactions: List[Dict[str, Any]] = None) -> Block:
        """Mine and append a new block. Returns the new block."""
        if transactions is None:
            transactions = []

        prev_block = self.get_latest_block()

        # Coinbase reward transaction
        coinbase = {
            "from": "QCoinNetwork",
            "to": self.miner_address,
            "amount": self.block_reward,
            "note": f"Block reward for {self.miner_address}"
        }
        all_txs = [coinbase] + transactions

        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=all_txs,
            previous_hash=prev_block.hash,
            difficulty=self.difficulty
        )

        hashrate = new_block.mine_block()
        self.total_hashes += new_block.nonce
        self.total_time += (time.time() - new_block.timestamp)  # rough

        self.chain.append(new_block)
        return new_block

    def is_chain_valid(self) -> bool:
        """Validate hash integrity and chain links."""
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]
            if curr.hash != curr.calculate_hash():
                print(f"Invalid hash at block {i}")
                return False
            if curr.previous_hash != prev.hash:
                print(f"Broken link at block {i}")
                return False
        return True

    def get_balance(self, address: str) -> float:
        """Scan all transactions for balance (demo only - inefficient for large chains)."""
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.get("to") == address:
                    balance += float(tx.get("amount", 0))
                if tx.get("from") == address:
                    balance -= float(tx.get("amount", 0))
        return balance

    def save_to_json(self, filepath: str) -> None:
        """Persist the full chain to a JSON file."""
        data = {
            "difficulty": self.difficulty,
            "block_reward": self.block_reward,
            "target_block_time": self.target_block_time,
            "adjust_every": self.adjust_every,
            "miner_address": self.miner_address,
            "chain": []
        }
        for block in self.chain:
            data["chain"].append({
                "index": block.index,
                "timestamp": block.timestamp,
                "transactions": block.transactions,
                "previous_hash": block.previous_hash,
                "nonce": block.nonce,
                "difficulty": block.difficulty,
                "hash": block.hash
            })
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Chain saved to {filepath} ({len(self.chain)} blocks)")

    def load_from_json(self, filepath: str) -> bool:
        """Load chain from JSON file and validate. Returns True on success."""
        try:
            with open(filepath, "r") as f:
                data = json.load(f)

            self.difficulty = data.get("difficulty", 4)
            self.block_reward = data.get("block_reward", 50.0)
            self.target_block_time = data.get("target_block_time", 60.0)
            self.adjust_every = data.get("adjust_every", 5)
            self.miner_address = data.get("miner_address", "QLoadedMiner")

            self.chain = []
            for bdata in data.get("chain", []):
                block = Block(
                    index=bdata["index"],
                    timestamp=bdata["timestamp"],
                    transactions=bdata["transactions"],
                    previous_hash=bdata["previous_hash"],
                    nonce=bdata["nonce"],
                    difficulty=bdata.get("difficulty", self.difficulty)
                )
                # Restore the stored hash (do not recalculate during load)
                block.hash = bdata["hash"]
                self.chain.append(block)

            if not self.is_chain_valid():
                print("Warning: Loaded chain failed validation!")
                return False

            print(f"Chain loaded from {filepath} ({len(self.chain)} blocks, valid)")
            return True
        except Exception as e:
            print(f"Failed to load chain: {e}")
            return False


 def main():
    parser = argparse.ArgumentParser(
        description="QCoin Enhanced PoW Miner v0.2 - Nexus Project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""Examples:
  python qcoin_miner.py --difficulty 4 --blocks 5
  python qcoin_miner.py --difficulty 3 --blocks 8 --simulate-txs --persist chain.json
  python qcoin_miner.py --load chain.json --blocks 4 --miner-address Node42
"""
    )
    parser.add_argument("--difficulty", type=int, default=4, help="Initial PoW difficulty (leading zeros)")
    parser.add_argument("--blocks", type=int, default=5, help="Number of blocks to mine after genesis")
    parser.add_argument("--reward", type=float, default=50.0, help="Block reward in QCoin")
    parser.add_argument("--miner-address", type=str, default="QDemoMiner", help="Address receiving block rewards")
    parser.add_argument("--simulate-txs", action="store_true", help="Include demo transactions between blocks")
    parser.add_argument("--persist", type=str, metavar="FILE", help="Save final chain to JSON file")
    parser.add_argument("--load", type=str, metavar="FILE", help="Load existing chain from JSON and continue mining")
    parser.add_argument("--target-block-time", type=float, default=60.0, help="Target seconds per block for difficulty adjustment")
    parser.add_argument("--adjust-every", type=int, default=5, help="Adjust difficulty every N blocks")

    args = parser.parse_args()

    print("=" * 70)
    print("QCOIN MINING PROTOTYPE v0.2  |  NEXUS PROJECT")
    print("Mesh + AI + Hardware incentive layer  |  From Hannover with Esslinger & Co.")
    print("=" * 70)

    blockchain = QCoinBlockchain(
        difficulty=args.difficulty,
        block_reward=args.reward,
        target_block_time=args.target_block_time,
        adjust_every=args.adjust_every
    )
    blockchain.miner_address = args.miner_address

    actual_block_times: List[float] = []

    if args.load:
        if not blockchain.load_from_json(args.load):
            print("Starting fresh chain instead.")
            blockchain.create_genesis_block()
    else:
        blockchain.create_genesis_block()

    print(f"Starting miner: {args.miner_address}")
    print(f"Initial difficulty: {blockchain.difficulty} | Target block time: {blockchain.target_block_time}s")
    print(f"Genesis balance: {blockchain.get_balance(args.miner_address):.2f} QC\n")

    demo_txs = [
        {"from": args.miner_address, "to": "QRecipientMesh", "amount": 12.5, "note": "Mesh contribution reward"},
        {"from": args.miner_address, "to": "QAIswarm", "amount": 7.5, "note": "AI task payout"}
    ]

    start_mining = time.time()

    for i in range(args.blocks):
        txs = demo_txs if args.simulate_txs else []
        print(f"--- Mining block {len(blockchain.chain)} ---")

        block_start = time.time()
        new_block = blockchain.add_block(txs)
        block_end = time.time()
        actual_block_times.append(block_end - block_start)

        # Adjust difficulty periodically
        if len(actual_block_times) >= blockchain.adjust_every and len(blockchain.chain) % blockchain.adjust_every == 0:
            new_diff = blockchain.adjust_difficulty(actual_block_times[-blockchain.adjust_every:])
            blockchain.difficulty = new_diff

        print(f"  Balance now: {blockchain.get_balance(args.miner_address):.2f} QC | Chain length: {len(blockchain.chain)}\n")

    total_time = time.time() - start_mining
    avg_hashrate = blockchain.total_hashes / total_time if total_time > 0 else 0

    print("=" * 70)
    print("MINING SESSION COMPLETE")
    print(f"Blocks mined this session: {args.blocks}")
    print(f"Final chain length: {len(blockchain.chain)} blocks")
    print(f"Final balance ({args.miner_address}): {blockchain.get_balance(args.miner_address):.2f} QC")
    print(f"Average hashrate: {avg_hashrate:,.0f} H/s | Total time: {total_time:.1f}s")
    print(f"Chain valid: {blockchain.is_chain_valid()}")
    print("=" * 70)

    if args.persist:
        blockchain.save_to_json(args.persist)

    print("\nNext steps: Integrate with Yggdrasil mesh, add real tx signing, or run multiple instances.")
    print("Use --load to continue from a saved chain across sessions or devices.")


if __name__ == "__main__":
    main()
