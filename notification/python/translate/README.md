# Python Azure Functions to provide image processing capabilities in the WellLine EEP

## Setting up environment to debug the EventGridTrigger function locally (macos)
- change to the *eep-image-azfpy* folder
- pull the latest code from the repo
- make sure you have pyenv installed (brew install pyenv)
- add these two lines to the end of your .zshrc file (repalce user with your user directory name)

    export PATH=“/Users/ *user* /.pyenv:$PATH”
    eval “$(pyenv init -)”


- restart your command line / terminal so these changes take effect
- make sure there is a .python-version file in the root of the repo directory that contains the text "3.6.9"
- run:   pyenv install 3.6.9
- run:   python --version   and make sure it says 3.6.9
- run:   python -m venv ~/envs/azf
- run:   source ~/envs/azf/bin/activate
- run:   pip install requests

- obtain an auth token and export it as the TIMELINE_AUTH_TOKEN environment variable

- run the azure function host using the command:   *func host start*

- use the *sendEventGridEvent* utility to send events to the function