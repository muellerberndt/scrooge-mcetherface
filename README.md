# Scrooge McEtherface

[![Discord](https://img.shields.io/discord/481002907366588416.svg)](https://discord.gg/E3YrVtG)

An Ethereum auto-looter based on [Mythril Classic](https://github.com/ConsenSys/mythril-classic/). Use at your own risk.

## Installation

```bash
$ git clone https://github.com/b-mueller/scrooge-mcetherface
$ cd scrooge-mcetherface
$ pip install -r requirements.txt
$ cp config.ini.example config.ini
```

St up your RPC URL and Ethereum address in `config.ini`. Note that you'll need to run a node to send transactions, it won't work over INFURA. You can also try it with [Ganache](https://truffleframework.com/ganache).

Python 3.5 or higher is required.

## Usage

```
$ ./scrooge <address>
```

<p align="center">
	<img src="/static/screenshot.png">
</p>
