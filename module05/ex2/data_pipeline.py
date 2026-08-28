from abc import ABC, abstractmethod
from typing import Any, Protocol


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


class ExportPlugin(Protocol):

    def process_output(
        self,
        data: list[tuple[int, str]]
    ) -> None:
        ...


class CSVPlugin:

    def process_output(
        self,
        data: list[tuple[int, str]]
    ) -> None:
        values: list[str] = []

        for rank, value in data:
            values.append(value)

        print("CSV Output:")
        print(",".join(values))


class JSONPlugin:

    def process_output(
        self,
        data: list[tuple[int, str]]
    ) -> None:
        items: list[str] = []

        for rank, value in data:
            items.append(f'"item_{rank}": "{value}"')

        print("JSON Output:")
        print("{" + ", ".join(items) + "}")


class DataStream:

    def __init__(self) -> None:
        self.processors: list[DataProcessor] = []
        self.stats: dict[DataProcessor, int] = {}

    def register_processor(
        self,
        proc: DataProcessor
    ) -> None:
        self.processors.append(proc)
        self.stats[proc] = 0

    def process_stream(
        self,
        stream: list[Any]
    ) -> None:
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

    def output_pipeline(
        self,
        nb: int,
        plugin: ExportPlugin
    ) -> None:
        for processor in self.processors:
            output_data: list[tuple[int, str]] = []

            for i in range(nb):
                rank, value = processor.output()

                if rank == -1:
                    break

                output_data.append((rank, value))

            if output_data:
                plugin.process_output(output_data)


def main() -> None:
    print("=== Code Nexus - Data Pipeline ===")

    print("Initialize Data Stream...")

    stream = DataStream()

    stream.print_processors_stats()

    print("Registering Processors")

    numeric = NumericProcessor()
    text = TextProcessor()
    log = LogProcessor()

    stream.register_processor(numeric)
    stream.register_processor(text)
    stream.register_processor(log)

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
                "log_message": "User is connected"
            }
        ],
        42,
        ["Hi", "five"]
    ]

    print("Send first batch of data on stream:", data)

    stream.process_stream(data)

    stream.print_processors_stats()

    print("Send 3 processed data from each processor "
          "to a CSV plugin:")

    csv_plugin = CSVPlugin()

    stream.output_pipeline(3, csv_plugin)

    stream.print_processors_stats()

    print("Send another batch of data:")

    second_data = [
        21,
        ["I love AI", "LLMs are wonderful", "Stay healthy"],
        [
            {
                "log_level": "ERROR",
                "log_message": "500 server crash"
            },
            {
                "log_level": "NOTICE",
                "log_message": "Certificate expires in 10 days"
            }
        ],
        [32, 42, 64, 84, 128, 168],
        "World hello"
    ]

    stream.process_stream(second_data)

    stream.print_processors_stats()

    print("Send 5 processed data from each processor "
          "to a JSON plugin:")

    json_plugin = JSONPlugin()

    stream.output_pipeline(5, json_plugin)

    stream.print_processors_stats()


if __name__ == "__main__":
    main()
