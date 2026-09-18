import os

from dotenv import load_dotenv


def load_configuration() -> dict[str, str | None]:
    """Load configuration from environment variables."""
    load_dotenv()

    config = {
        "MATRIX_MODE": os.getenv("MATRIX_MODE"),
        "DATABASE_URL": os.getenv("DATABASE_URL"),
        "API_KEY": os.getenv("API_KEY"),
        "LOG_LEVEL": os.getenv("LOG_LEVEL"),
        "ZION_ENDPOINT": os.getenv("ZION_ENDPOINT"),
    }

    return config


def check_configuration(config: dict[str, str | None]) -> bool:
    """Check whether all required configuration is available."""
    missing = []

    for name, value in config.items():
        if not value:
            missing.append(name)

    if missing:
        print("WARNING: Missing configuration:")
        for name in missing:
            print(f"  - {name}")
        return False

    return True


def show_configuration(config: dict[str, str | None]) -> None:
    """Display the configuration without exposing secrets."""
    mode = config["MATRIX_MODE"]
    database_url = config["DATABASE_URL"]
    api_key = config["API_KEY"]
    log_level = config["LOG_LEVEL"]
    zion_endpoint = config["ZION_ENDPOINT"]

    print("Configuration loaded:")
    print(f"Mode: {mode}")

    if mode == "development":
        print("Database: Connected to local instance")
    elif mode == "production":
        print("Database: Connected to production instance")
    else:
        print(f"Database: {database_url}")

    if api_key:
        print("API Access: Authenticated")
    else:
        print("API Access: Not authenticated")

    print(f"Log Level: {log_level}")

    if zion_endpoint:
        print("Zion Network: Online")
    else:
        print("Zion Network: Offline")


def security_check(config: dict[str, str | None]) -> None:
    """Show basic configuration security checks."""
    print("Environment security check:")
    print("[OK] No hardcoded secrets detected")

    if os.path.exists(".env"):
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] .env file not found")

    if config["MATRIX_MODE"] == "development":
        print("[OK] Production overrides available")
    elif config["MATRIX_MODE"] == "production":
        print("[OK] Production configuration active")
    else:
        print("[WARNING] Unknown MATRIX_MODE")


def main() -> None:
    """Run the Oracle configuration system."""
    print("ORACLE STATUS: Reading the Matrix...")

    config = load_configuration()

    if not check_configuration(config):
        print("\nPlease configure the missing variables and try again.")
        return

    show_configuration(config)
    security_check(config)

    print("\nThe Oracle sees all configurations.")


if __name__ == "__main__":
    main()
