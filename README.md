# foul-mouth-slap
Script to check the files in output of git status for foul words, variants of those words and repeated chars.  
Will not work on Windhose.

## Install

1. Update assets/foul-words to your specific needs
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