from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):

    def __init__(self) -> None:
        self.data: list[tuple[int, str]] = []
        self.rank: int = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self.data:
            return (-1, "")

        return self.data.pop(0)


class NumericProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)):
            return True

        if isinstance(data, list):
            for item in data:
                if not isinstance(item, (int, float)):
                    return False
            return True

        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        if isinstance(data, list):
            for item in data:
                self.data.append((self.rank, str(item)))
                self.rank += 1
        else:
            self.data.append((self.rank, str(data)))
            self.rank += 1


class TextProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True

        if isinstance(data, list):
            for item in data:
                if not isinstance(item, str):
                    return False
            return True

        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")

        if isinstance(data, list):
            for item in data:
                self.data.append((self.rank, item))
                self.rank += 1
        else:
            self.data.append((self.rank, data))
            self.rank += 1


class LogProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return (
                isinstance(data.get("log_level"), str)
                and isinstance(data.get("log_message"), str)
            )

        if isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    return False

                if not isinstance(item.get("log_level"), str):
                    return False

                if not isinstance(item.get("log_message"), str):
                    return False

            return True

        return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        if isinstance(data, list):
            for item in data:
                text = item["log_level"] + ": " + item["log_message"]
                self.data.append((self.rank, text))
                self.rank += 1
        else:
            text = data["log_level"] + ": " + data["log_message"]
            self.data.append((self.rank, text))
            self.rank += 1


def main() -> None:
    print("=== Code Nexus - Data Processor ===\n")

    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()

    print("Testing Numeric Processor...")
    print(f"Trying to validate input '42': {numeric.validate(42)}")
    print(f"Trying to validate input 'Hello': {numeric.validate("Hello")}")

    # print("Test invalid ingestion of string 'foo' without prior validation:")
    # try:
    #     numeric.ingest("foo")
    # except ValueError as error:
    #     print(f"Got exception: {error}")
    print("Processing data: [1, 2, 3, 4, 5]")
    numeric.ingest([1, 2, 3, 4, 5])

    print("Extracting 3 values...")
    for i in range(3):
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")

    print("\nTesting Text Processor...")
    print(f"Trying to validate input '42': {text.validate(42)}")
    print("Processing data: ['Hello', 'Nexus', 'World']")
    text.ingest(["Hello", "Nexus", "World"])
    print("Extracting 1 value...")

    rank, value = text.output()
    print(f"Text value {rank}: {value}")

    print("\nTesting Log Processor...")
    print(f"Trying to validate input 'Hello': {log.validate("Hello")}")

    log_data = [
        {
            "log_level": "NOTICE",
            "log_message": "Connection to server"
        },
        {
            "log_level": "ERROR",
            "log_message": "Unauthorized access!!"
        }
    ]
    log.validate(log_data)
    print(f"Processing data: {log_data}")

    log.ingest(log_data)

    print("Extracting 2 values...")
    for i in range(2):
        rank, value = log.output()
        print(f"Log entry {rank}: {value}")


if __name__ == "__main__":
    main()
