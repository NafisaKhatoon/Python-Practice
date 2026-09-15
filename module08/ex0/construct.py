import sys
import os
import site


in_virtual_env = sys.prefix != sys.base_prefix

if in_virtual_env:
    python_path = sys.executable
    environment_path = sys.prefix
    package_path = site.getsitepackages()
    virtual_env_name = os.path.basename(environment_path)
    print("MATRIX STATUS: Welcome to the construct\n")
    print(f"Current Python: {python_path}")
    print(f"Virtual Environment: {virtual_env_name}")
    print(f"Environment Path: {environment_path}\n")
    print("SUCCESS: You're in an isolated environment!")
    print("Safe to install packages without affecting")
    print("the global system.\n")
    print(f"Package installation path: {package_path[0]}")
else:
    python_path = sys.executable
    package_path = site.getsitepackages()
    print("MATRIX STATUS: You're still plugged in\n")
    print(f"Current Python: {python_path}")
    print("Virtual Environment: None detected\n")
    print("WARNING: You're in the global environment!")
    print("The machines can see everything you install.\n")
    print(f"Global package installation path: {package_path[0]}\n")
    print("To enter the construct, run:")
    print("python -m venv matrix_env")
    print("source matrix_env/bin/activate # On Unix")
    print("matrix_env\\Scripts\\activate # On Windows\n")
    print("Then run this program again.")
