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

    def ingest(
        self,
        data: int | float | list[int | float]
    ) -> None:
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

    def ingest(
        self,
        data: dict[str, str] | list[dict[str, str]]
    ) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        if isinstance(data, list):
            for item in data:
                text = (
                    item["log_level"]
                    + ": "
                    + item["log_message"]
                )
                self.data.append((self.rank, text))
                self.rank += 1
        else:
            text = (
                data["log_level"]
                + ": "
                + data["log_message"]
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
            print("No processor found, no data")
            return

        for processor in self.processors:
            total = self.stats[processor]
            remaining = len(processor.data)

            print(
                f"{type(processor).__name__}: "
                f"total {total} items processed, "
                f"remaining {remaining} on processor"
            )
