# foul-mouth-slap
Script to check the diff content of files in output of git status for foul words, variants of those words and repeated chars.  
Will not work on Windhose.

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

Just run `py.test` to go over everything.