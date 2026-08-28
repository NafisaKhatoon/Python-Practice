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
                text = (
                    item["log_level"] + ": " + item["log_message"]
                )
                self.data.append((self.rank, text))
                self.rank += 1
        else:
            text = (
                data["log_level"] + ": " + data["log_message"]
            )
            self.data.append((self.rank, text))
            self.rank += 1


class DataStream:

    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []
        self.stats: dict[DataProcessor, int] = {}

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)
        self.stats[proc] = 0

    def process_stream(self, stream: list[Any]) -> None:
        for item in stream:
            found = False

            for processor in self.processors:
                if processor.validate(item):
                    before = len(processor.data)

                    processor.ingest(item)

                    after = len(processor.data)
                    self.stats[processor] += after - before

                    found = True
                    break

            if not found:
                print(
                    "DataStream error - Can't process "
                    f"element in stream: {item}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")

        if not self.processors:
            print("No processor found, no data\n")
            return

        for processor in self.processors:
            total = self.stats[processor]
            remaining = len(processor.data)

            print(
                f"{type(processor).__name__}: "
                f"total {total} items processed, "
                f"remaining {remaining} on processor"
            )


def main() -> None:
    print("=== Code Nexus - Data Stream ===\n")

    print("Initialize Data Stream...")
    stream = DataStream()

    stream.print_processors_stats()

    print("Registering Numeric Processor\n")
    numeric = NumericProcessor()
    stream.register_processor(numeric)

    data = [
        "Hello world",
        [3.14, -1, 2.71],
        [
            {
                "log_level": "WARNING",
                "log_message": "Telnet access! Use ssh instead"
            },
            {
                "log_level": "INFO",
                "log_message": "User wil is connected"
            }
        ],
        42,
        ["Hi", "five"]
    ]

    print("Send first batch of data on stream:", data)
    stream.process_stream(data)

    stream.print_processors_stats()

    print("\nRegistering other data processors")

    text = TextProcessor()
    log = LogProcessor()

    stream.register_processor(text)
    stream.register_processor(log)

    print("Send the same batch again")
    stream.process_stream(data)

    stream.print_processors_stats()

    print(
        "\nConsume some elements from the data processors: "
        "Numeric 3, Text 2, Log 1"
    )

    for i in range(3):
        numeric.output()

    for i in range(2):
        text.output()

    for i in range(1):
        log.output()

    stream.print_processors_stats()


if __name__ == "__main__":
    main()
