# ai-art-shield
AI Art Shield - Image Protection Tool

#### Description:
**AI Art Shield** is a command-line tool developed in Python for protecting visual artworks from predatory generative artificial intelligence systems (such as midjourney, dall-e, sora, etc...). This is based on a project I've created for CS50P (original repository: https://github.com/dtettarasar/CS50P-final-project).

The program offers two main features:

1. **Secure Image** – Takes an image as input and applies a set of invisible perturbations (e.g., subtle noise, hidden watermarking, pixel noise, steganography, etc.) to make the image harder to exploit by AIs trained to recognize or reproduce artistic styles.

2. **Test Protection** – Allows you to evaluate the effectiveness of the protection by comparing the original image with its protected version, and by analyzing and measuring the level of alteration applied to make it less usable for AI.

---

#### Improvements:

The primary goal for the future is to make these features accessible to any user through a web application (likely developed with Django).

Beyond CS50P, I plan to work on the following key improvements:

- **Code Refactoring**: CS50P's final project requires all code to be in a single file, structured as multiple functions, to meet specific validation rules. While suitable for a learning exercise, this structure isn't ideal for a real-world application. I'll refactor the entire codebase for improved modularity, dividing it into multiple files and/or reimplementing functions within a class structure for better organization and maintainability.

- **Additional Protection Algorithms**: Currently, the project features only DCT (Discrete Cosine Transform) Protection. Future steps include integrating more diverse protection tools, such as Wavelet-based Watermarking, Fourier Transform Watermarking, and Adversarial Perturbation. These protection systems will be continuously upgraded to evolve with AI advancements, ensuring robust defense for illustrators' and photographers' work.

- **Built-in Signature System**: A crucial future feature will be the ability to add an invisible "signature" to artworks, possibly through Invisible QR Code Embedding. This system aims to certify the authenticity of an artwork or picture, verifying its human origin. Ideally, the QR code would store a token signed by the illustrator/photographer's private key.

- **Web3 / Blockchain Integration**: Exploring features related to Web3 and blockchain technologies to enhance provenance, ownership, and unforgeable rights management for digital art.

#### Technologies:
- Python 3
- Pillow (PIL) / OpenCV
- NumPy
- argparse / sys

---

#### Installation:

This project uses `uv` for dependency management, offering a fast and modern development experience.

1.  **Install `uv`** (if you don't have it already):

    If you use `pipx` (recommended for CLI tools):
    ```bash
    pipx install uv
    ```
    Alternatively, you can install it via `pip`:
    ```bash
    pip install uv
    ```
    Or, download a standalone executable from the [official uv GitHub releases](https://github.com/astral-sh/uv/releases).

2.  **Install project dependencies and create the virtual environment**:

    Navigate to the project root directory and run:
    ```bash
    uv sync
    ```
    This command will automatically create a virtual environment (named `.venv` by default) and install all required packages defined in `pyproject.toml` (or `requirements.txt` if you still use it).

3.  **Activate the virtual environment (optional, but good practice)**:

    While `uv run` allows executing scripts without explicit activation, it's good practice to activate the environment if you plan to install other packages or use Python interactively.
    ```bash
    source .venv/bin/activate  # macOS/Linux
    # or
    .venv\Scripts\activate     # Windows PowerShell
    # or
    .venv\Scripts\activate.bat # Windows Command Prompt
    ```

---

#### Usage:

1. Protect an image

```
uv run main.py secure --input image.jpg --output image_protected.jpg
```

2. Test image protection

```
uv run main.py verify -p img_protected.jpg -o img_original.jpg
```
