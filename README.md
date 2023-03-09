# Regression Games - Capture the Flag - Getting Started - Python

**PLEASE NOTE THAT PYTHON SUPPORT IS EXTREMELY EXPERIMENTAL. We recommend using our TypeScript or JavaScript templates.**

PLEASE OPEN THE "TUTORIAL" TOOL IN THE REPLIT TOOLS PANE. Also, see the final code in `final_code.py`

This template demonstrates the basics of using the [rg-bot](https://www.npmjs.com/package/rg-bot) and [rg-ctf-utils](https://www.npmjs.com/package/rg-ctf-utils) packages to create
a simple bot for the Regression Games: Capture the Flag challenge. At the end of
this tutorial, you will have a bot that can capture the flag and collect items.

**Please open this project in Replit, or see the Markdown files in `.tutorial/` for the tutorial.**

# About the Alpha Cup - $1500+ in prizes!
_Sign up at https://play.regression.gg/events_

[![Regression Games Alpha Cup Video](https://img.youtube.com/vi/RgUIYXuewzU/0.jpg)](http://www.youtube.com/watch?v=RgUIYXuewzU "Regression Games Alpha Cup Video")

The Alpha Cup, sponsored by [Steamship](https://steamship.com), is a 3v3 Capture the Flag tournament in Minecraft.
Players program bots in TypeScript, JavaScript, and Python to score points by capturing
flags and killing the opposing team. The first team to 10 flag captures wins! Learn more
about our tournament on [our blog](https://medium.com/@RGAaron/regression-games-announces-the-alpha-cup-cd1815e7ef9c) and from our [Game Specification](https://www.notion.so/regressiongg/Capture-the-Flag-Game-Specification-bc72be0f38df427287ec428006d1d299?pvs=4).


## Known Limitations

Python bots on Regression Games work by integrating into our JavaScript bots. This means that the Python calls to the bot are complete via calls to a Node/JavaScript backend. There are some known limitations to the current setup.

* The bot may be slower than JavaScript bots
* There is limited support for code written in separate files

_Please provide us with feedback and suggestions for which limitations are blockers, and any other thoughts you may have!_