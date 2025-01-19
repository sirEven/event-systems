import re
from typing import Any, Dict


def dummy_handler(data: Dict[str, Any]) -> None:
    dummy_data = data.get("dummy_data")
    print(f"{dummy_data}")


def dummy_handler_two(data: Dict[str, Any]) -> None:
    dummy_data = data.get("dummy_data")
    print(f"{dummy_data}")


async def async_dummy_handler(data: Dict[str, Any]) -> None:
    dummy_data = data.get("dummy_data")
    print(f"{dummy_data}")


def call_counting_dummy_handler(data: Dict[str, Any]) -> None:
    count_statement = data.get("dummy_data")
    if match := re.search(r"\d+", count_statement):
        # Extract the number and convert it to an integer
        number = int(match.group())
        # Increment the number
        incremented_number = number + 1
        # Replace the number in the string with the incremented number
        incremented_string = re.sub(r"\d+", str(incremented_number), count_statement)
        print(incremented_string)
