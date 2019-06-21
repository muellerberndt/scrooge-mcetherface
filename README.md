# Scrooge McEtherface

[![Discord](https://img.shields.io/discord/481002907366588416.svg)](https://discord.gg/E3YrVtG)

Scrooge McEtherface is an Ethereum auto-looter based on [Mythril](https://github.com/ConsenSys/mythril/). It exploits instances of [Ether theft](https://smartcontractsecurity.github.io/SWC-registry/docs/SWC-105) and [self-destruction](https://smartcontractsecurity.github.io/SWC-registry/docs/SWC-106) caused by various issues including [integer arithmetic bugs](https://smartcontractsecurity.github.io/SWC-registry/docs/SWC-101), [exposed initialization functions](https://smartcontractsecurity.github.io/SWC-registry/docs/SWC-118) and others. Use at your own peril.

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

Python 3.5 or higher is required. Set up your RPC URL and Ethereum address in `config.ini`. Note that you'll need to run a node to send transactions, it won't work over INFURA. The easiest way to test is using [Ganache](https://truffleframework.com/ganache).

The `symbolic_tx_count` parameter sets a bound on the number of transactions being explored. See also this [Medium article](https://medium.com/@muellerberndt/automating-smart-contract-exploitation-and-looting-d43e9740b41c).

## Usage

```
$ ./scrooge <address>
```

## Support

**No support for this tool exists whatsoever.**

## Important Notes

- This is a weekend project that hasn't been extensively tested. Don't use it on mainnet.
- Act responsibly and don't accidentally kill anyone else's contract.
- **Use only on testnet and at your own risk**.
