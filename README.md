
Shakti is a bunch of command line scripts that I personally use to code faster.

It includes things like:
1. Automatically run black/prettier before doing git add
2. Get git commit messages from AI
3. Select a command from curated list and execute (with option to edit)
4. List all the commands in the curated list
And more...

## Git related commands
### How to Automatically run black/prettier before doing git add

```bash
s git add -u
s git add .
```

### How to get git commit messages from AI

```bash
s git message
```

### How to get git diff only for relevant files

Whenever coding, I change a lot of files. When I want to see the diff, I want to see it for the relevant files.
Therefore, I created a .gitdiffignore file which contains the list of files that I want to ignore when doing git diff.
If you use `s git diff`, it will use .gitdiffignore to show the diff only for the relevant files (ignoring files within .gitdiffignore).

```bash
s git diff
```

### How to get git diff only for relevant files

This one also ignores the files within .gitdiffignore
```bash
s git difftool
```

## Curated command line related commands
### How to select and run a command from a curated list

```bash
s cmd list-eval
```

### How to list all the commands in the curated list

```bash
s cmd list
```

## How to run shakti from your command line

```bash
poetry add pyinstall --group dev
```


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

### How to generate git commit messages

```bash
{ echo "Give commit message for the following changes, follow Conventional Commit guidelines. \n\nHere are examples of couple of commit messages for your reference: \nExample one and two:\n" ; git --no-pager log -2 --pretty=format:"%B"; echo "\n\nAnd now here are the diffs: "; git --no-pager diff --staged } | aichat
```

### Set git difftool to use cursor

Set git difftool to use cursor
```bash
git config --global diff.tool cursor
git config --global difftool.cursor.cmd 'cursor --wait --diff $LOCAL $REMOTE'
```

Verify if cursor is set as difftool
```bash
git config --global --get diff.tool
# Should output: cursor

git config --global --get difftool.cursor.cmd
# Should output: cursor --wait --diff $LOCAL $REMOTE
```

## Feature Backlog
- Add support for AI to choose the directory to create a file in.
    - Based on file name
    - Based on the current directory structure
    - Based on file description
- Add support for AI to choose to re-organize the directory structure


```bash
poetry update shakti
```