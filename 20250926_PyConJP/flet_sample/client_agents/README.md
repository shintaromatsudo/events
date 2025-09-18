# Hello Agent - Flet Version

A simple demo showing how to create AI agents using OpenAI API in Flet, inspired by the [wasm-agents-blueprint](https://github.com/mozilla-ai/wasm-agents-blueprint) project.

## Features

- 🤖 Chat with OpenAI GPT models
- 🎭 Customizable agent behavior with instructions
- 🚀 Easy-to-use Flet UI
- 💡 Example prompts and instructions
- 🔐 Secure API key management

## Setup

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Configure OpenAI API Key:**

   Copy the `.env` file and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your-actual-openai-api-key-here
   ```

   You can get your API key from: https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key

3. **Run the app:**
   ```bash
   uv run flet run src/main.py
   ```

## How to Use

1. **Configure**: Set your OpenAI API key in the `.env` file
2. **Initialize**: Click "Initialize OpenAI Client" to set up the connection
3. **Customize**: Choose from example prompts and instructions, or create your own
4. **Run**: Click "Run Agent" to send your prompt and see the AI response

## Example Use Cases

- **Haiku Bot**: Get responses in traditional Japanese haiku format
- **Code Helper**: Get programming assistance with code examples
- **Pirate Assistant**: Have fun conversations with a pirate-themed AI
- **Philosopher**: Get deep, metaphorical responses to your questions

## Technical Details

This Flet application provides a native desktop/mobile interface for interacting with OpenAI's GPT models, offering similar functionality to the browser-based wasm-agents-blueprint demo but with the benefits of a native app experience.

## Requirements

- Python 3.9+
- OpenAI API key
- Internet connection for API callsClientAgents app

## Run the app

### uv

Run as a desktop app:

```
uv run flet run
```

Run as a web app:

```
uv run flet run --web
```

### Poetry

Install dependencies from `pyproject.toml`:

```
poetry install
```

Run as a desktop app:

```
poetry run flet run
```

Run as a web app:

```
poetry run flet run --web
```

For more details on running the app, refer to the [Getting Started Guide](https://flet.dev/docs/getting-started/).

## Build the app

### Android

```
flet build apk -v
```

For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://flet.dev/docs/publish/android/).

### iOS

```
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://flet.dev/docs/publish/ios/).

### macOS

```
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://flet.dev/docs/publish/macos/).

### Linux

```
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://flet.dev/docs/publish/linux/).

### Windows

```
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://flet.dev/docs/publish/windows/).
