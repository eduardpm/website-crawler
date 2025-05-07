# website-crawler

Built with python 3.11.2 in Debian 12.

# Install env (system-wide, not in a venv)

`pip install -r requirements.txt`

# How to run the crawler

Just run `python main.py` and select the options you want.

# How it works

Each website has it's own folder. Currently, the only supported ones are Coolblue.be and Emag.ro  
Each folder will contain a file called `page_structure.py`, which will contain the html elements being selected to extract relevant info.  
Each folder will contain a file called `urls.py`, which will contain the urls of the products that should be crawled for.

Both these files should be extended as needed.

# TODO

Beautify printed data.  
Integrate with a Telegram bot.