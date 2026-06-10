# QCoin Mining: Starter Guide and Implementation

**Part of Nexus Project** - Foundational hub for xMesh/NovaNet/QNET mesh networking, XCoin/QCoin blockchain, AI agent swarms, and hardware prototypes.

Initiated by Sven Normen Esslinger / Esslinger & Co. (Hannover).

## Vision and Context

QCoin (alongside XCoin) forms the **economic and incentive layer** of the Nexus ecosystem. It enables:
- Trustless value transfer and coordination across the decentralized mesh.
- Governance and tokenized participation (e.g., voting on network upgrades, rune protocols like Wizard Q).
- Incentives for contributing resources: mesh bandwidth/routing (via xMesh/QNET), AI swarm compute/tasks, hardware uptime (Soilnova, Vista Nova prototypes), and node operation.
- Arbitrage mechanisms, immutable audit trails, and self-sovereign economy.

**Mining** in this context refers to the process of securing the blockchain through computational work (initially Proof-of-Work for fair, permissionless entry) while aligning incentives with the physical and digital layers of Nexus:
- Early miners bootstrap the network and earn genesis rewards.
- Future evolution: Hybrid or alternative consensus (PoS, Proof-of-Mesh-Contribution, Proof-of-AI-Utility) for energy efficiency and better integration with low-power mesh devices (Yggdrasil, Tenda Nova, Dockerized nodes).

This starter provides a **minimal viable prototype** for local testing and learning. It is **not production-ready** but serves as the foundation to build upon in the `src/blockchain-layer/` directory. The prototype now includes dynamic difficulty adjustment and chain persistence for more realistic testing.

## Why Start with PoW?

- **Advantages**: Simple to implement and understand; fair launch/distribution without pre-mine centralization risks; proven in Bitcoin; good for initial bootstrapping and hype in decentralized communities.
- **Nuances & Trade-offs**:
  - Energy consumption: Mitigate later with efficient algorithms (e.g., RandomX for CPU, or tie difficulty to useful work like mesh proofs).
  - Suitability for mesh: Traditional PoW may be too heavy for embedded/IoT nodes in xMesh. Consider lightweight variants or offloading to more powerful hardware prototypes.
  - Security in small networks: Early stages vulnerable to 51% attacks; use checkpoints or community governance initially.
  - Examples from similar projects: Bitcoin (global PoW), Monero (privacy-focused CPU mining), Helium (Proof of Coverage for physical hotspots - analogous to mesh contribution).

**Implications**: PoW mining kickstarts participation and QCoin distribution. As the mesh and AI swarms grow, shift incentives to reward real utility (e.g., uptime proofs submitted via mesh, AI task completion verified on-chain).

## Quick Start: Run the Enhanced Miner

### Prerequisites
- Python 3.8+
- No external packages required (uses only standard library: hashlib, json, time, argparse, datetime, typing)

### Steps
1. Ensure you are on the latest main branch:
   ```bash
   git pull origin main
   cd nexus-project
   ```

2. Run the miner with enhanced options:
   ```bash
   python src/blockchain-layer/qcoin_miner.py --help
   ```

3. Example runs:
   ```bash
   # Basic demo (difficulty 4, mine 5 blocks)
   python src/blockchain-layer/qcoin_miner.py --difficulty 4 --blocks 5 --miner-address SvenQMiner

   # With simulated transactions and persistence
   python src/blockchain-layer/qcoin_miner.py --difficulty 3 --blocks 10 --miner-address QMeshNode01 --simulate-txs --persist qcoin_chain.json

   # Load a previously saved chain and continue mining
   python src/blockchain-layer/qcoin_miner.py --load qcoin_chain.json --blocks 3 --miner-address QMeshNode01
   ```

The script now supports:
- Dynamic difficulty adjustment (every 5 blocks by default, targeting ~60s per block for demo purposes)
- JSON chain persistence (save/load full chain state)
- Hasrate estimation and better progress/stats
- Coinbase rewards + optional demo transactions
- Chain validation on load/save

## Architecture Outline for QCoin Layer (Updated)

### Core Components (expanding in `src/blockchain-layer/`)
- **qcoin_miner.py**: Standalone enhanced miner with CLI, PoW, dynamic difficulty, persistence (current focus).
- **qcoin_core.py** (planned next): Refactored core classes (Block, Transaction, Blockchain) for import/reuse in nodes/wallets.
- **qcoin_node.py** (future): Full node with P2P (Yggdrasil/libp2p integration), mempool, block propagation.
- **qcoin_wallet.py** (future): ECDSA keypairs, tx signing, balance queries, rune support.
- **consensus.py** (future): Full difficulty adjustment algorithm, hybrid consensus hooks (PoW + PoS/PoC).
- **incentives.py** (future): Emission schedule, halving, staking, mesh/AI contribution oracles.
- **mesh_integration.py** (future): Proof-of-Contribution hooks, bandwidth/uptime proofs from xMesh/QNET, AI swarm verification.

### Block Structure
- `index`, `timestamp`, `transactions` (list of dicts), `previous_hash`, `nonce`, `hash`
- Mining: Find nonce so that `hash` has required leading zeros (difficulty).
- Coinbase transaction automatically added for block reward.

**Mining Loop**:
1. Prepare transactions + coinbase reward.
2. Mine (nonce search).
3. (Optional) Adjust difficulty based on actual vs target block time.
4. Append to chain.
5. Persist if requested.

**Tokenomics Sketch** (highly customizable — define in incentives.py later):
- Ticker: QC
- Example max supply: 21 000 000 QC (or higher for broad mesh incentives)
- Initial block reward: 50 QC, with planned halving or phase-based reduction
- Genesis: Large test allocation + small development treasury
- Distribution mechanisms: Pure mining rewards + future bonuses for mesh uptime, AI task proofs, hardware contributions
- Runes / Wizard Q: Extensible tx metadata or special transaction types for governance and utility

### Integration with Nexus Layers
- **Mesh (xMesh/NovaNet/QNET)**: Future miners will submit verifiable contributions (Yggdrasil peer stats, bandwidth, routing success) for bonus QCoin or reduced difficulty. Dockerized deployment on Tenda Nova or custom hardware.
- **AI Agent Swarms**: On-chain rewards for verified task completion or compute contribution. Agents can hold/spend QCoin.
- **Hardware Prototypes**: Soilnova/Vista Nova nodes earn for sensor data or uptime proofs submitted via mesh.
- **Privacy & Self-Sovereignty**: Run nodes over Yggdrasil + Tor/I2P. Future zk or privacy-preserving contribution proofs.

## New Enhanced Features (v0.2)

### 1. Dynamic Difficulty Adjustment
Every N blocks (default 5), the miner recalculates difficulty based on actual time taken vs target block time (default 60 seconds for demo).
- If blocks are too fast → difficulty increases.
- If blocks are too slow → difficulty decreases (floored at 1).
- This simulates real blockchain behavior and makes testing more realistic.

### 2. Chain Persistence (JSON)
- `--persist filename.json` saves the entire chain after mining.
- `--load filename.json` loads a previous chain and continues from the last block (validates on load).
- Useful for multi-session testing, simulating restarts on mesh nodes, or sharing test chains.

### 3. Improved Statistics & CLI
- Per-block hashrate estimate (hashes per second).
- Total mining time and average hashrate.
- Better progress printing during nonce search.
- Clearer final summary with balances and validation status.

### 4. Better Code Structure
- Clear separation of Block mining logic.
- Easier to extend (e.g., add real Transaction class with signing in next iteration).

## Extending the Prototype — Recommended Next Steps

### Immediate (I can push these next)
- Refactor into importable `qcoin_core.py` + `qcoin_miner.py`.
- Add simple ECDSA transaction signing stub (using cryptography or ecdsa lib — or pure Python for demo).
- Implement mempool simulation and pending tx queue.
- Add `--target-block-time` and `--adjust-every` CLI flags for full control.

### Short-term (mesh integration focus)
- Persist chain + miner state in Docker volume for your Tenda Nova / Yggdrasil nodes.
- Simple socket or Yggdrasil-based block broadcasting between multiple miner instances.
- Proof-of-mesh stub: accept extra "contribution" txs that reward uptime/bandwidth proofs.

### Medium / Long-term
- Full Rust implementation (performance + alignment with Grok Launcher).
- Substrate or custom consensus for hybrid PoW/PoS.
- On-chain governance and rune protocol.
- Economic modeling (token velocity, incentive alignment simulations).
- Production security audit path.

## Edge Cases & Important Considerations
- **Difficulty swings**: In real deployment, use exponential moving average or Bitcoin-style retargeting (every 2016 blocks) instead of simple every-5-blocks.
- **Chain validation on load**: Always re-validate hashes and links when loading — prevents corrupted state.
- **51% / small network**: For early testnets, consider temporary trusted checkpoints or low difficulty with community monitoring.
- **Resource usage on mesh devices**: Monitor CPU/RAM. Offer "light" mode or offload PoW to more powerful nodes.
- **Persistence security**: JSON files are plaintext — future versions should add encryption or use proper DB with access control.
- **Regulatory & token classification**: Continue framing QCoin as utility/governance token within the Esslinger & Co. Delaware C-Corp structure.

## Related Resources
- Bitcoin whitepaper & reference implementation
- Your existing stack: Yggdrasil, Docker, Rust prototypes, Grok Launcher
- Future docs to populate: `docs/blockchain.md`, `docs/architecture.md`, `docs/incentives.md`

## Status & Call to Action

**QCoin mining prototype is now live on `main`** and significantly enhanced. Clone/pull `main`, run the miner, experiment with persistence and difficulty adjustment, and start integrating with your mesh nodes.

This is the foundation for the economic layer of Nexus. Real work on QCoin has begun in earnest.

Pull requests, issues, and specific requests ("add transaction signing", "make a Rust version", "integrate Yggdrasil P2P", "model 21M supply emission curve") are welcome.

From Hannover with Esslinger & Co. — Building the self-sovereign mesh economy.

*QCoin mining starter v0.2 — pushed to main.*
