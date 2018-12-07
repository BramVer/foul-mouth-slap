# foul-mouth-slap
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FBramVer%2Ffoul-mouth-slap.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2FBramVer%2Ffoul-mouth-slap?ref=badge_shield)  

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
Different words and patterns (= basic regex) can be added to specific file extension identifiers, to overwrite the eventual result.  
`foul` sections will be appended to the list of violations, while `acceptable` sections will remove them from the list.

**Note:** The regex patterns are provided as literal strings; no need to escape them.

#### Example: Given the following structure:
```toml
[all]
  [all.foul]
    words = [
      "dink",
      "poop",
    ]
    patterns = [
      '([a-zA-Z])\\1{3,}'
    ]
[css]
  [css.foul]
    words = ["test"]
  [css.acceptable]
    words = ["poop"]
    patterns = ['#[a-zA-Z0-9]*']

```
The resulting foul_words for `.css` files will be `dink, test`, all other files will have `dink, poop` as foul_words.  

For patterns it's a bit trickier: the first (= foul) pattern makes sure we don't repeat the same textcharacter more than 3 times.  
The second one allows character repetitions when they are preceded by a `#` character in a `.css` file.  
This results in a situation where `.py` files cannot contain the following text: `# aaaaAAAaa` but `.css` files can,
because the violation is overruled by the acceptable pattern.

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


## License
[![FOSSA Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2FBramVer%2Ffoul-mouth-slap.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2FBramVer%2Ffoul-mouth-slap?ref=badge_large)
