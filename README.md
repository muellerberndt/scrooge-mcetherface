# Scrooge McEtherface

[![Discord](https://img.shields.io/discord/481002907366588416.svg)](https://discord.gg/E3YrVtG)

Scrooge McEtherface is an Ethereum auto-looter based on [Mythril Classic](https://github.com/ConsenSys/mythril-classic/). It exploits instances of [Ether theft](https://smartcontractsecurity.github.io/SWC-registry/docs/SWC-105) and [selfdestruct](https://smartcontractsecurity.github.io/SWC-registry/docs/SWC-106) caused by various issues including [integer arithmetic bugs](https://smartcontractsecurity.github.io/SWC-registry/docs/SWC-101), [exposed initialization functions](https://smartcontractsecurity.github.io/SWC-registry/docs/SWC-118) and others. Use at your own peril.

Tested on Ethernaut [Fallout](https://ethernaut.zeppelin.solutions/level/0x220beee334f1c1f8078352d88bcc4e6165b792f6) and [Fallback](https://ethernaut.zeppelin.solutions/level/0x234094aac85628444a82dae0396c680974260be7) (for Fallack set `symbolic_tx_count` to 3).

<p align="center">
	<img src="/static/screenshot.png">
</p>

## Installation

```bash
$ git clone https://github.com/b-mueller/scrooge-mcetherface
$ cd scrooge-mcetherface
$ pip install -r requirements.txt
$ cp config.ini.example config.ini
```

Set up your RPC URL and Ethereum address in `config.ini`. Note that you'll need to run a node to send transactions, it won't work over INFURA. The easiest way to test is using [Ganache](https://truffleframework.com/ganache).

Use the ``symbolic_tx_count` parameter to set a bound on the number of transcations being explored (explained in [this article](https://hackernoon.com/practical-smart-contract-security-analysis-and-exploitation-part-1-6c2f2320b0c).

Python 3.5 or higher is required.

## Usage

```
$ ./scrooge <address>
```

## Important Notes

- Act responsibly and don't accidentally kill anyone else's contract.
- **Use only on testnet and at your own risk**.
