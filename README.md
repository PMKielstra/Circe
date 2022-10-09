# Circe: Readable Chatbots

## Installation and Configuration
```
git clone https://github.com/PMKielstra/Circe.git
cd Circe
pip install -r requirements.txt
gunicorn main:app
```

Configuration is best done via environment variables.  See [CONFIG.md](/CONFIG.md).

## Writing Markdown Chatbots
The Mr. Chips bot, which lives in the `bots` folder, will teach you how to write Markdown chatbots.  If you don't feel like interacting with a chatbot, you can [read his source code](/bots/Mr%20Chips.md).  You get the same experience.

## Writing RiveScript Chatbots
Just put your `.rive` file in the folder where Circe looks for bots.  This functionality is powered by [https://github.com/aichaos/rivescript-js/](RiveScript-JS).