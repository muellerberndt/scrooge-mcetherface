# Scrooge McEtherface

<p align="center">
	<img src="/static/scrooge.png" height="320px"/>
</p>

[![Discord](https://img.shields.io/discord/481002907366588416.svg)](https://discord.gg/E3YrVtG)

An Ethereum auto-looter based on [Mythril Classic](https://github.com/ConsenSys/mythril-classic/). Use at your own risk.

## Installation

```bash
$ git clone https://github.com/b-mueller/scrooge-mcetherface
$ cd scrooge-mcetherface
$ pip install -r requirements.txt
$ cp config.ini.example config.ini
```

Don't forget to set up your RPC and sender address in `config.ini`. Python 3.5 or higher is required.

## Usage

```
$ ./scrooge <address>
```
