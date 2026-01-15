# Contributing to Keymap

Thank you for your interest in contributing to Keymap! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue with:
- A clear, descriptive title
- Steps to reproduce the bug
- Expected behavior vs actual behavior
- Your macOS version and Python version
- Relevant logs or error messages

### Suggesting Features

Feature requests are welcome! Please open an issue with:
- A clear description of the feature
- Why this feature would be useful
- Any potential implementation ideas

### Pull Requests

1. **Fork the repository** and create a new branch for your feature or bug fix
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**:
   - Follow the existing code style
   - Add comments where necessary
   - Update documentation if needed

3. **Test your changes**:
   - Ensure the application still runs: `./run.sh`
   - Test both backend and frontend functionality
   - Check that your changes work across different macOS versions if possible

4. **Commit your changes**:
   ```bash
   git commit -m "Add feature: brief description"
   ```

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request** with:
   - A clear title and description
   - Reference to any related issues
   - Screenshots or demos if applicable

## Development Setup

### Prerequisites
- macOS 10.13 or later
- Python 3.11+
- Node.js 18+

### Setting Up Development Environment

1. Clone your fork:
   ```bash
   git clone https://github.com/YOUR_USERNAME/keymap.git
   cd keymap
   ```

2. Install backend dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

4. Run in development mode:

   **Backend** (in one terminal):
   ```bash
   source venv/bin/activate
   python backend/main.py
   ```

   **Frontend** (in another terminal):
   ```bash
   cd frontend
   npm run dev
   ```

   Visit http://localhost:3000 for the Vite dev server with hot reload.

## Code Style Guidelines

### Python (Backend)
- Follow PEP 8 style guide
- Use descriptive variable names
- Add docstrings to functions and classes
- Keep functions focused and single-purpose

### JavaScript/React (Frontend)
- Use functional components with hooks
- Keep components small and reusable
- Use meaningful component and variable names
- Add comments for complex logic

### Git Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Be concise but descriptive
- Reference issues when applicable (e.g., "Fix #123")

## Project Structure

```
keymap/
├── backend/           # Python Flask backend
│   ├── main.py        # Flask server & API
│   ├── event_tap.py   # Event capture
│   ├── remapper.py    # Remapping logic
│   └── ...
├── frontend/          # React frontend
│   └── src/
│       ├── App.jsx
│       └── components/
└── config/            # Configuration files
```

## Testing

While we don't currently have automated tests, please manually test:
- Button detection functionality
- Remapping for different action types (click, keystroke, ignore)
- Per-app context switching
- Configuration save/load
- UI responsiveness

## Questions?

Feel free to open an issue with the "question" label if you have any questions about contributing!

## Code of Conduct

Be respectful and constructive in all interactions. We're all here to make Keymap better!

---

Thank you for contributing! 🎉
