import importlib


def check_package(name: str, message: str) -> bool:
    """Check if a package is installed."""
    try:
        package = importlib.import_module(name)
        version = getattr(package, "__version__", "unknown")
        print(f"[OK] {name} ({version}) - {message}")
        return True
    except ImportError:
        print(f"[MISSING] {name}")
        print(f"Install it with: pip install {name}")
        return False


def main() -> None:
    print("LOADING STATUS: Loading programs...\n")

    print("Checking dependencies:")

    pandas_ok = check_package(
        "pandas",
        "Data manipulation ready"
    )

    numpy_ok = check_package(
        "numpy",
        "Numerical computation ready"
    )

    check_package(
        "requests",
        "Network access ready"
    )

    matplotlib_ok = check_package(
        "matplotlib",
        "Visualization ready"
    )

    if not pandas_ok or not numpy_ok or not matplotlib_ok:
        print("\nSome required dependencies are missing.")
        print("Install them with:")
        print("pip install -r requirements.txt")
        print("or:")
        print("poetry install")
        return

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    print("\nAnalyzing Matrix data...")

    data = np.random.randint(1, 100, 1000)

    dataframe = pd.DataFrame({"matrix_data": data})

    print(f"Processing {len(dataframe)} data points...")

    print("Generating visualization...")

    plt.plot(dataframe["matrix_data"])
    plt.title("Matrix Data")
    plt.xlabel("Data Point")
    plt.ylabel("Value")
    plt.savefig("matrix_analysis.png")
    plt.close()

    print("\nAnalysis complete!")
    print("Results saved to: matrix_analysis.png")


if __name__ == "__main__":
    main()
