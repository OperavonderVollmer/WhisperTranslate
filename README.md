# WhisperTranslate

WhisperTranslate is a Python package designed for translating file names and metadata across multiple formats, including images, audio, and documents. It helps automate and streamline the organization of multilingual files while preserving their essential metadata.

## Features

- Translate file names into different languages
- Extract and translate metadata from various file types
- Ensure consistency across translated files
- Support for multiple file formats, including images, audio, and text-based documents
- Seamless integration with FileWhisperer for metadata handling

## Installation

### Prerequisites

- Python 3.x
- Required dependencies (install using pip):
  ```sh
  pip install pytaglib python-magic-bin pillow deep-translator
  ```
- [OperaPowerRelay](https://github.com/OperavonderVollmer/OperaPowerRelay) (Required for additional utilities)
  ```sh
  pip install git+https://github.com/OperavonderVollmer/OperaPowerRelay.git@v1.1.2
  ```
  
### Manual Installation

1. Clone or download the repository.
2. Navigate to the directory containing `setup.py`:
   ```sh
   cd /path/to/WhisperTranslate
   ```
3. Install the package in **editable mode**:
   ```sh
   pip install -e .
   ```

### Installing via pip:

```sh
pip install git+https://github.com/OperavonderVollmer/WhisperTranslate.git@latest
```

Ensure that all necessary dependencies are installed in your environment.

## Dependencies

- `deep_translator` for translation
- `FileWhisperer` for metadata extraction

## License

WhisperTranslate is licensed under the MIT License.
