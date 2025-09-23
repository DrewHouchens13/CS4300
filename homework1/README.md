# CS4300 Homework Repository

This repository contains Python source code and corresponding **pytest unit tests** for the CS4300 homework assignments.  

Each task demonstrates core Python concepts such as data types, control structures, file I/O, duck typing, package usage, and testing methodology.  

The project is organized to separate **source files (`src/`)** from **test files (`test/`)**, ensuring a clean and professional workflow.

---

## 📂 Project Structure
```
CS4300/
├── homework1/
│   ├── src/
│   │   ├── task1.py
│   │   ├── task2.py
│   │   ├── task3.py
│   │   ├── task4.py
│   │   ├── task5.py
│   │   ├── task6_read_me.txt
│   │   ├── task6.py
│   │   └── task7.py
│   ├── test/
│   │   ├── __pycache__/
│   │   ├── test_task1.py
│   │   ├── test_task2.py
│   │   ├── test_task3.py
│   │   ├── test_task4.py
│   │   ├── test_task5.py
│   │   ├── test_task6.py
│   │   └── test_task7.py
│   └── pyproject.toml
├── README.md
├── homework2/
└── hw1_env/
```

## ▶️ Running the Code & Tests

### 1. Activate the Virtual Environment

The repository uses a Python virtual environment (`hw1_env`) for dependency management.  
Activate it before running any code:

```bash
# On Windows (PowerShell)
.\hw1_env\Scripts\activate

# On Mac/Linux
source hw1_env/bin/activate
```

### 2. Navigate to the Homework Directory
Move into the `homework1` folder where the source and test files are stored:

```bash
cd homework1
```

### 3. Run the Test Cases with Pytest
Execute the test suite to validate your code:

```bash
pytest
```

-Running pytest without arguments will discover all tests inside the test/ directory.
-To run a specific test file (e.g., only for Task 3):
```bash
pytest test/test_task3.py
```

-To increase verbosity (see more detail on each test):
```bash
pytest -v
```

## ✅ Notes
- Ensure your virtual environment is **activated** before running tests.
- All test files follow the naming convention `test_taskX.py`, which maps directly to the corresponding `taskX.py` in the `src/` folder.
- The project uses **pytest** for testing; make sure it is installed inside the virtual environment.
