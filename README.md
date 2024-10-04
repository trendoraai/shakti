


How to run shakti from your command line

```bash
VENV_PATH=$(poetry env info --path)
export PATH="$VENV_PATH/bin:$PATH"
source ~/.bashrc   # For Bash
source ~/.zshrc    # For Zsh
which shakti
```

### Pre-commit hooks

How to install pre-commit hooks

```bash
pre-commit install
```

How to manually run pre-commit hooks

```bash
pre-commit run --all-files
```