---
name: blockchain
description: Smart contracts, DeFi, audit, Solidity
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Blockchain
## Solidity Smart Contract
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
contract MyToken is ERC20, Ownable {
    constructor() ERC20("MyToken", "MTK") Ownable(msg.sender) {
        _mint(msg.sender, 1000000 * 10 ** decimals());
    }
    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }
}
```
## Security Checklist
- [ ] Reentrancy protection (ReentrancyGuard)
- [ ] Integer overflow (Solidity 0.8+ checked math)
- [ ] Access control (Ownable, AccessControl)
- [ ] Front-running protection
- [ ] Flash loan attack vectors
- [ ] Oracle manipulation
- [ ] Gas optimization
- [ ] Formal verification si montants importants
## Audit Workflow
```
1. Lire la spec et les invariants attendus
2. Analyser le code manuellement
3. Outils automatises (Slither, Mythril, Echidna)
4. Tests de fuzz
5. Rapport avec severite (Critical/High/Medium/Low/Info)
```
