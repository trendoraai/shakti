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