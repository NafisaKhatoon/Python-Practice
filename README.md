*This project has been created as part of the 42 curriculum by nakhatoo.*

# Call Me Maybe

## Description

Call Me Maybe is a Python project that introduces function calling
in Large Language Models (LLMs) using constrained decoding.

The goal of this project is to translate natural language requests
into structured function calls in JSON format using the
Qwen/Qwen3-0.6B language model.

Instead of answering a question directly, the program identifies
the appropriate function and extracts the required arguments
according to the provided function definitions.

For example, given the following request:

"What is the sum of 2 and 3?"

The program generates a structured function call containing
the function name and its parameters instead of calculating
the result.

The project demonstrates how constrained decoding can improve
the reliability of structured outputs from a small language model.

## Instructions

### Requirements

- Python 3.10 or later
- uv package manager
- NumPy
- Pydantic
- Provided LLM SDK
- Qwen/Qwen3-0.6B language model
- Flake8 and mypy for code quality checks


### Installation

From the root directory of the project, install the dependencies:

```bash
uv sync
```

Alternatively:

```bash
make install
```

### Execution

Run the program using:

```bash
uv run python -m src
```

Alternatively:

```bash
make run
```

By default, the program reads the following input files:

- `data/input/functions_definition.json`
- `data/input/function_calling_tests.json`

The generated results are saved in:

`data/output/function_calling_results.json`

The output directory is automatically created if it does not exist.

### Command-line arguments

The program supports custom input and output paths:

```bash
uv run python -m src \
    --functions_definition data/input/functions_definition.json \
    --input data/input/function_calling_tests.json \
    --output data/output/function_calling_results.json
```

| Argument | Description |
| --- | --- |
| `--functions_definition` | Path to the function definitions |
| `--input` | Path to the natural language prompts |
| `--output` | Path to the generated JSON results |

### Makefile commands

| Command | Description |
| --- | --- |
| `make install` | Install project dependencies |
| `make run` | Execute the program |
| `make debug` | Execute using Python's debugger |
| `make clean` | Remove temporary files and caches |
| `make lint` | Run Flake8 and mypy |
| `make lint-strict` | Run strict type checking |

## Project Structure

```text
call_me_maybe/
├── src/
│   ├── __init__.py
│   ├── __main__.py
│   ├── decoder.py
│   ├── models.py
│   └── vocab.py
├── llm_sdk/
├── data/
│   └── input/
│       ├── functions_definition.json
│       └── function_calling_tests.json
├── .flake8
├── .gitignore
├── mypy.ini
├── Makefile
├── pyproject.toml
├── uv.lock
└── README.md
```

The `data/output/` directory is generated during execution
and is not included in the repository.

### File responsibilities

- `__main__.py`: Handles command-line arguments, input validation,
  model initialization, prompt processing and output generation.
- `decoder.py`: Implements constrained decoding, function
  selection and parameter generation.
- `models.py`: Defines Pydantic models for input and output data.
- `vocab.py`: Loads the vocabulary and converts token
  representations into readable text.
- `llm_sdk/`: Contains the provided SDK for interacting
  with the language model.

## Algorithm Explanation

### What is constrained decoding?

A language model generates text by predicting the next token
based on the previous tokens.

For each generation step, the model produces logits representing
the scores of possible next tokens.

Without constraints, the model may generate invalid JSON,
incorrect parameter types or unexpected function names.

Constrained decoding restricts the available tokens according
to the expected structure before selecting the next token.

### Generation pipeline

The implementation follows these steps:

1. Load and validate the function definitions and input prompts.
2. Initialize the language model and vocabulary.
3. Build a prompt containing the available functions, their
   descriptions, parameter types and the user request.
4. Encode the prompt into token IDs using the LLM SDK.
5. Retrieve logits from the language model.
6. Restrict token selection according to the current
   decoding constraints.
7. Select the highest-scoring valid token.
8. Update the token history.
9. Repeat the process until the function name and its
   required parameters have been generated.
10. Construct the final function call and serialize it
    into JSON.

```text
Natural language request
          |
          v
Prompt construction
          |
          v
Tokenization
          |
          v
Language model
          |
          v
Next-token logits
          |
          v
Apply token constraints
          |
          v
Select valid token
          |
          v
Update token history
          |
          v
Complete function call
          |
          v
JSON output
```

### Vocabulary processing

The vocabulary is loaded using the public SDK method:

`get_path_to_vocab_file()`

The vocabulary contains mappings between token representations
and token IDs.

The Vocab class converts byte-level token representations
into readable UTF-8 text.

Two mappings are maintained:

- Token ID to token text.
- Token text to token ID.

These mappings allow the decoder to determine which tokens
are valid for a particular generation step.

Tokens that cannot be decoded independently as UTF-8
are excluded from the current vocabulary representation.

### Function selection

The `_choose()` method selects a function name token by token.

At each step, the decoder identifies tokens that correspond
to valid prefixes of the available function names.

The language model selects among these valid candidates
according to its logits.

When only one continuation is possible, the decoder can
select it without requesting another model prediction.

Function names are obtained dynamically from the input
function definitions rather than being hardcoded.

An internal `no_match` option allows the model to reject
requests that do not correspond to any available function.

### Parameter generation

After selecting a function, the decoder generates each
parameter according to its declared type.

The implementation supports:

- Strings
- Numbers
- Integers
- Booleans

#### String generation

The `_string()` method uses precomputed vocabulary masks
to distinguish normal string content from tokens that
can close a string.

Invalid candidates are excluded during token selection.

The decoder maintains the generated string and updates
the token history throughout the generation process.

JSON escape sequences are interpreted when possible,
and the final output is serialized using Python's
JSON module.

A maximum generation length prevents uncontrolled
string generation.

#### Number generation

The `_number()` method uses regular expressions to
validate numeric prefixes and completed numbers.

The numeric vocabulary is restricted to characters
that can be used to construct numeric values.

Leading whitespace is accepted at the beginning of a
number to support the tokenizer's combined tokens,
such as a space followed by a minus sign.

The generated value is converted into an integer
or floating-point number according to its declared type.

A maximum generation length prevents uncontrolled
numeric generation.

#### Boolean generation

Boolean values are generated by restricting the
available choices to `true` and `false`.

The selected value is converted into a Python boolean.

### Token masking

NumPy is used to apply masks to the model's logits.

Invalid token scores are replaced with negative infinity.

The highest-scoring valid token is then selected
using `numpy.argmax()`.

This allows the decoder to restrict the model's output
rather than relying only on prompt instructions.

### Output generation

The generated function name and parameters are stored
in a Pydantic FunctionCall model.

Each successful result contains exactly three keys:

- `prompt`
- `name`
- `parameters`

Python's JSON module serializes the results into
the required output file.

The program generates function calls but does not
execute the selected functions.

## Design Decisions

### Modular architecture

The project is divided into separate modules to keep
input handling, validation, vocabulary processing
and constrained decoding independent.

This improves readability, maintainability and
debugging.

### Pydantic validation

Pydantic BaseModel is used for the project's data
models and operational classes.

Input models validate the structure of the function
definitions and natural language prompts.

The Vocab and ConstrainedDecoder classes also use
Pydantic to validate their declared attributes during
initialization.

Custom exception classes inherit from Exception.

### Dynamic function definitions

Function names and parameter types are loaded from
the provided JSON file.

The decoder does not use a fixed list of task-specific
function names to determine the appropriate function.

This allows different function definitions to be
provided through the command line.

### Public SDK methods

The implementation interacts with the language model
through the public methods provided by the LLM SDK:

- `encode()`
- `get_logits_from_input_ids()`
- `get_path_to_vocab_file()`

No private SDK methods or attributes are accessed.

### Performance optimization

Vocabulary masks are precomputed during decoder
initialization instead of being recalculated for
every generated token.

The language model is initialized once and reused
for all input prompts.

Forced token selections avoid unnecessary model
inference calls when only one valid continuation
is available.

These decisions reduce repeated computation and
improve execution time.

### Error handling

The program handles several error conditions:

- Missing input files.
- Invalid JSON syntax.
- Incorrect input data structures.
- Missing required input fields.
- Empty function definitions.
- Model initialization failures.
- Unsupported parameter types.
- Decoding failures.
- Output file access errors.

Custom exceptions provide clear error messages.

When the model selects the internal `no_match` option,
a decoding exception is raised. The program reports
a warning, skips the unsupported request and continues
processing the remaining prompts.

## Performance Analysis

The implementation was tested using the 11 prompts
provided with the project.

### Results

| Metric | Result |
| --- | --- |
| Total supplied prompts | 11 |
| Correct function selections | 11/11 |
| Correct function calls on supplied inputs | 11/11 |
| Function selection accuracy | 100% |
| Complete call accuracy on supplied inputs | 100% |
| Valid JSON outputs | 100% |
| Measured execution time | 2 minutes 20.08 seconds |
| Required execution time | Under 5 minutes |
| Flake8 | Passed |
| Mypy | Passed |

The measured execution time is within the required
five-minute limit.

These results apply to the supplied test dataset
and the development environment.

Execution time may vary depending on hardware,
system workload, model loading and input complexity.

Additional tests revealed semantic limitations
in mixed-sign number extraction and whole-word
regular expression generation.

Structural correctness and semantic accuracy are
different: a valid JSON function call may still
contain incorrect argument values.

## Challenges Faced

### Maintaining valid token history

During development, a problem was identified in
string generation where the final character could
be duplicated in the token history.

The closing-token handling was modified to append
only the remaining string content and closing
quotation mark.

This improved consistency between the generated
value and the model context.

### Execution time

An initial attempt to validate every vocabulary
token at every string-generation step significantly
increased execution time.

The implementation was changed back to using
precomputed vocabulary masks while retaining the
string-history correction.

This allowed the program to remain within the
required execution time.

### Negative number generation

Initial tests showed that negative signs were
frequently missing from generated numbers.

Debugging the model's logits revealed that the
tokenizer could represent whitespace and a minus
sign as a combined token.

The numeric vocabulary was extended to accept
leading whitespace, and forced whitespace after
numeric parameter keys was removed.

This enabled negative number generation, although
some mixed-sign requests remain challenging
for the model.

### Regular expression generation

Some natural language requests require derived
arguments instead of directly copying values.

For example, replacing vowels requires the model
to generate an appropriate regular expression.

Prompt instructions and consistent token-history
handling helped improve the generated results.

### Unmatched requests

Initially, the decoder was forced to select one
of the available functions even when none matched
the user request.

An internal `no_match` option was introduced so
the model could reject unsupported requests.

The program reports a warning instead of producing
an unrelated function call when this option is selected.

### Pydantic integration

The operational classes were converted to inherit
from BaseModel while preserving the decoding logic.

Validation is performed during initialization
rather than inside the token-generation loop.

This keeps the additional validation overhead limited.

### Static type checking

Flake8 and mypy initially reported issues related
to the virtual environment and the provided SDK.

Configuration files were introduced to exclude
external dependencies from linting and focus the
checks on the project implementation.

The SDK imports and token return types were also
reviewed to maintain compatibility between static
type checking and runtime execution.

## Testing Strategy

The implementation was tested incrementally.

Each modification was followed by execution of
the original test dataset to detect regressions.

### Functional testing

The supplied prompts cover:

- Addition of numbers.
- Greeting generation.
- String reversal.
- Square root function selection.
- Regular expression substitution.

### Edge-case testing

Additional prompts were used to test:

- Negative numbers.
- Decimal numbers.
- Large numbers.
- Empty strings.
- Strings containing spaces.
- Special characters.
- Indirect requests.
- Unmatched requests.
- Whole-word substitution.

### Error-handling testing

The program was tested with:

- Missing prompt files.
- Missing function definition files.
- Malformed JSON.
- Incorrect JSON structures.
- Missing required fields.
- Empty function definitions.
- Unsupported natural language requests.

### Code quality testing

Flake8 and mypy are executed using:

```bash
make lint
```

### Performance testing

Execution time is measured using:

```bash
time uv run python -m src
```

The generated JSON is inspected to verify the
function names, parameter values and data types.

JSON parsing can also be checked using:

```bash
uv run python -m json.tool \
    data/output/function_calling_results.json
```

## Example Usage

### Example 1: Number addition

Input:

```json
[
    {
        "prompt": "What is the sum of 2 and 3?"
    }
]
```

Output:

```json
[
    {
        "prompt": "What is the sum of 2 and 3?",
        "name": "fn_add_numbers",
        "parameters": {
            "a": 2.0,
            "b": 3.0
        }
    }
]
```

### Example 2: String reversal

Input:

```json
[
    {
        "prompt": "Reverse the string 'hello'"
    }
]
```

Output:

```json
[
    {
        "prompt": "Reverse the string 'hello'",
        "name": "fn_reverse_string",
        "parameters": {
            "s": "hello"
        }
    }
]
```

### Example 3: Regular expression substitution

Input:

```json
[
    {
        "prompt": "Replace all vowels in 'Programming is fun' with asterisks"
    }
]
```

Output:

```json
[
    {
        "prompt": "Replace all vowels in 'Programming is fun' with asterisks",
        "name": "fn_substitute_string_with_regex",
        "parameters": {
            "source_string": "Programming is fun",
            "regex": "([aeiouAEIOU])",
            "replacement": "*"
        }
    }
]
```

### Example 4: Custom input file

```bash
uv run python -m src \
    --input /tmp/custom_tests.json \
    --output /tmp/custom_results.json
```

### Example 5: Unsupported request

Input:

```json
[
    {
        "prompt": "What is the weather today?"
    }
]
```

When the model correctly selects `no_match`, the
program reports a warning and produces an empty
JSON array if no other requests are present.

```json
[]
```

## Known Limitations

- Semantic accuracy depends on the language model.
- Mixed-sign numbers may occasionally be extracted incorrectly.
- Whole-word regular expression matching may be imprecise.
- String escape handling is not a complete JSON grammar
  implementation.
- Partial UTF-8 tokens are excluded from vocabulary processing.
- Complex nested parameters and arrays are not supported.
- Unmatched prompts may be skipped, resulting in fewer output
  entries than input prompts.
- The model may not always correctly identify unsupported requests.

## Resources

### Python and development tools

- Python documentation:
  https://docs.python.org/3/

- Python JSON documentation:
  https://docs.python.org/3/library/json.html

- Python regular expressions:
  https://docs.python.org/3/library/re.html

- Python typing:
  https://docs.python.org/3/library/typing.html

- PEP 8:
  https://peps.python.org/pep-0008/

- NumPy documentation:
  https://numpy.org/doc/

- Pydantic documentation:
  https://docs.pydantic.dev/

- uv documentation:
  https://docs.astral.sh/uv/

- Flake8 documentation:
  https://flake8.pycqa.org/

- Mypy documentation:
  https://mypy.readthedocs.io/

### Language models and constrained decoding

- Call Me Maybe project subject, version 1.5.
- Provided LLM SDK and its public methods.

- Qwen3-0.6B model:
  https://huggingface.co/Qwen/Qwen3-0.6B

- Hugging Face tokenizer documentation:
  https://huggingface.co/docs/tokenizers/

- JSON standard (RFC 8259):
  https://www.rfc-editor.org/rfc/rfc8259

### AI Usage

ChatGPT was used as a learning and development assistant
during this project.

AI assistance was used for:

- Understanding language models, tokens, logits and
  constrained decoding.
- Reviewing the project architecture and Python implementation.
- Suggesting code changes for string and number generation.
- Debugging negative-number tokenization issues.
- Improving prompt construction.
- Integrating Pydantic validation.
- Implementing unmatched-request handling.
- Understanding Flake8 and mypy errors.
- Preparing additional test cases.
- Reviewing performance and execution results.
- Preparing the README documentation.

Suggested changes were reviewed and tested incrementally
during development.

The final implementation was executed locally to verify
its behavior, accuracy, JSON output, execution time
and code quality.
