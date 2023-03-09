import logging
from rg_javascript import require, On

mineflayer_pathfinder = require('mineflayer-pathfinder')
mineflayer = require('mineflayer', '4.5.1')
rg_match_info = require('rg-match-info')
Vec3 = require('vec3').Vec3
RGBot = require('rg-bot', '1.10.0').RGBot
RGCTFUtils = require('rg-ctf-utils', '1.0.5').RGCTFUtils
CTFEvent = require('rg-ctf-utils', '1.0.5').CTFEvent

logging.basicConfig(level=logging.NOTSET)

# We keep track of deaths to make sure that this bot stops when it dies
deaths = 0

def configure_bot(bot: RGBot):
  """
  This strategy is the simplest example of how to get started 
  with the rg-bot and rg-ctf-utils packages. The Bot will get 
  the flag and then run back to base to score.
  
  Ways to extend this code:
  TODO: What happens when a bot is completing an action and 
        another event happens?
  TODO: How do we respond to item spawn and drop events?
  TODO: How do we target and attack enemies?
  TODO: What different states is my bot in, and how can I organize
        its behavior based on these states?
  rg-bot docs: https://github.com/Regression-Games/RegressionBot/blob/main/docs/api.md
  rg-ctf-utils docs: https://github.com/Regression-Games/rg-ctf-utils
  """

  # Since most blocks can't be broken on Arctic Algorithm Field,
  # don't allow digging while pathfinding
  bot.allowDigWhilePathing(False)

  # Instantiate our helper utilities and events for Capture the Flag
  rg_ctf_utils = RGCTFUtils(bot)

  @On(bot, 'error')
  def bot_on_error(this, error):
    bot.chat('I encountered an error: %r', error)

  # When a player types "start" in the chat, the bot will begin
  # looking for and approaching the flag
  @On(bot, 'chat')
  def bot_on_chat(this, username, message, *args):
    print(args)
    if username != bot.username():
      return
    if message== 'start':
      rg_ctf_utils.approachFlag()

  # When a player obtains the flag, this event gets called.
  # In the case where that player is this bot, the bot
  # navigates back to their scoring location.
  @On(bot, CTFEvent.FLAG_OBTAINED)
  def bot_on_flag_obtained(this, collector):
    if collector == bot.username():
      rg_ctf_utils.scoreFlag()

  # If the flag was scored, simply chat a message
  @On(bot, CTFEvent.FLAG_SCORED)
  def bot_on_flag_scored(this, team_name):
    bot.chat(f"Flag scored by ${team_name} team, waiting until it respawns")

  # Once the flag respawns on the map, look for and approach the flag.
  @On(bot, CTFEvent.FLAG_AVAILABLE)
  def bot_on_flag_available(this, flag_position: Vec3):
    bot.chat(
      f"Flag is available at ${bot.vecToString(flag_position)}, going to get it"
    )
    rg_ctf_utils.approachFlag()
