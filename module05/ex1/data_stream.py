from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):

    def __init__(self) -> None:
        self.data: list[tuple[int, str]] = []

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if len(self.data) == 0:
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

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")

        if isinstance(data, list):
            for item in data:
                self.data.append((len(self.data), str(item)))
        else:
            self.data.append((len(self.data), str(data)))


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

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")

        if isinstance(data, list):
            for item in data:
                self.data.append((len(self.data), item))
        else:
            self.data.append((len(self.data), data))


class LogProcessor(DataProcessor):

    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return True

        if isinstance(data, list):
            for item in data:
                if not isinstance(item, dict):
                    return False
            return True

        return False

    def ingest(self, data: Any) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")

        if isinstance(data, list):
            for item in data:
                text = item["log_level"] + ": " + item["log_message"]
                self.data.append((len(self.data), text))
        else:
            text = data["log_level"] + ": " + data["log_message"]
            self.data.append((len(self.data), text))


class DataStream:

    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []
        self.total: dict[DataProcessor, int] = {}

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)
        self.total[proc] = 0

    def process_stream(self, stream: list[Any]) -> None:
        for data in stream:
            processed = False

            for processor in self.processors:
                if processor.validate(data):
                    before = len(processor.data)

                    processor.ingest(data)

                    after = len(processor.data)

                    self.total[processor] += after - before

                    processed = True
                    break

            if not processed:
                print(
                    "DataStream error - Can't process "
                    f"element in stream: {data}"
                )

    def print_processors_stats(self) -> None:
        print("== DataStream statistics ==")

        if len(self.processors) == 0:
            print("No processor found, no data")
            return

        for processor in self.processors:
            name = processor.__class__.__name__

            print(
                f"{name}: total {self.total[processor]} "
                f"items processed, remaining {len(processor.data)} "
                f"on processor"
            )


def main() -> None:
    print("=== Code Nexus - Data Stream ===")

    stream = DataStream()

    print("Initialize Data Stream...")
    stream.print_processors_stats()

    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()

    print("Registering Numeric Processor")
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
                "log_message": "User will is connected"
            }
        ],
        42,
        ["Hi", "five"]
    ]

    print(f"Send first batch of data on stream: {data}")

    stream.process_stream(data)
    stream.print_processors_stats()

    print("Registering other data processors")

    stream.register_processor(text)
    stream.register_processor(log)

    print("Send the same batch again")

    stream.process_stream(data)
    stream.print_processors_stats()

    print("Consume some elements from the data processors:")

    for i in range(3):
        numeric.output()

    for i in range(2):
        text.output()

    for i in range(1):
        log.output()

    stream.print_processors_stats()


if __name__ == "__main__":
    main()
