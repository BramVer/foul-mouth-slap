# foul-mouth-slap
Script to check the diff content of files in output of git status for foul words, variants of those words and repeated chars.  
Will not work on Windhose.

## Install

1. Update assets/word_list.toml to your specific needs
2. Create pre-commit hook somewhere you can easily access

```bash
touch ~/.git-templates/hooks/pre-commit
```
4. Call the script
```bash
#!/bin/sh

# Add other pre-commit hooks 
python /PATH/TO/slapper.py
```
5. Make hook executable
```bash
sudo chmod u+x ~/.git-templates/hooks/pre-commit
```
6. Set global rule in git to call this on commit in every repository
```bash
git config --global core.hooksPath ~/.git-templates/hooks/
```

### Adding custom rules
The rules for __all__ will be used as baseline.  
Different patterns/words can be added to specific file extension identifiers, to overwrite the eventual result.  
`foul` sections will be appended, while `acceptable` sections will omit existing checks.

#### Example: Given the following structure:
```toml
[all]
  [all.foul]
    words = [
      "dink",
      "kak",
    ]

[css]
  [css.foul]
    words = ["test"]
  [css.acceptable]
    words = ["kak"]
```
The resulting foul_words will be `dink, test`.