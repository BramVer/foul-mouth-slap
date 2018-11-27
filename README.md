# foul-mouth-slap
Script to check the diff content of files in output of git status for foul words, variants of those words and repeated chars.  
Will not work on Windhose.

## What in the seven hells is this and why would I need it?  

Personally, I don't like to mess around with git history, so I try to keep the project history as readable and clean as I can.  
Now, I'm also someone who likes to use the same non-sensical words to test stuff or during quick implementations:  
**make it work, make it right, make it fast**.  
The problem is I don't always catch everything before committing stuff when I *make it right*.  

This is me accepting I have bad habits, and working around them.  
*So what if I write `let dink = '';`?*  
The hook will catch this and make me aware of it, giving me the option to either stop the commit or to go ahead and push it into the repository's history.  
Now I can at least be aware when commiting sinful (oh so sinful) things into the repo's history.

## Install

1. Install requirements.txt
```bash
pip install -r requirements.txt
```

2. Copy `config.toml.default` to `config.toml` and `assets/violations.toml.default` to `assets/violations.toml`.
3. Create pre-commit hook somewhere you can easily access
```bash
mkdir -p ~/.git-templates/hooks
vim ~/.git-templates/hooks/pre-commit
```

4. Call the script from inside the hook
```bash
#!/bin/sh

# Add other pre-commit hooks 
python /PATH/TO/slapper.py
```

5. Make hook executable
```bash
chmod u+x ~/.git-templates/hooks/pre-commit
```

6. Set global rule in git to call this on commit in every repository
*Reminder: You could also set this per repository*
```bash
git config --global core.hooksPath ~/.git-templates/hooks/
```

### Adding custom rules
The rules for __all__ will be used as baseline.  
Different (basic regex) patterns/words can be added to specific file extension identifiers, to overwrite the eventual result.  
`foul` sections will be appended, while `acceptable` sections will omit existing checks.

#### Example: Given the following structure:
```toml
[all]
  [all.foul]
    words = [
      "dink",
      "poop",
    ]
[css]
  [css.foul]
    words = ["test"]
  [css.acceptable]
    words = ["poop"]
```
The resulting foul_words will be `dink, test`.  
The same applies to patterns.

### Testing
Tests are located in `slapper/tests` and require the [py.test](https://docs.pytest.org/en/latest/) module.  

**Optional:** Create a virtual environment to test.
```bash
python -m virtualenv .venv
source .venv/bin/activate
```
Install pytest
```bash
pip install pytest
```
Navigate to the `slapper` directory and run the tests.
```bash
python -m pytest -v
```
Smile as you watch the tests pass.
