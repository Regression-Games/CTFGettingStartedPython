import logging
from rg_javascript import require, On

mineflayer_pathfinder = require('mineflayer-pathfinder')
mineflayer = require('mineflayer', '4.5.1')
rg_match_info = require('rg-match-info')
Vec3 = require('vec3').Vec3
nbt = require("prismarine-nbt")
Models = require("./lib/Models.js")
usefulItemsList = require("./lib/UsefulItems.js").usefulItemsList
RGBot = require('rg-bot', '1.10.0').RGBot
RGCTFUtils = require('rg-ctf-utils', '1.0.5').RGCTFUtils
CTFEvent = require('rg-ctf-utils', '1.0.5').CTFEvent

logging.basicConfig(level=logging.NOTSET)

# We keep track of deaths to make sure that this bot stops when it dies
deaths = 0


def configure_bot(bot):

  bot.setDebug(False)
  bot.allowParkour(True)
  bot.allowDigWhilePathing(False)

  rg_ctf_utils = RGCTFUtils(bot)
  rg_ctf_utils.setDebug(False)

  @On(bot, 'spawn')
  def bot_on_spawn(this):
    bot.chat(
      f"I have arrived... ready to capture some flags and kill some bots at: {bot.vecToString(bot.position())}"
    )

  # Record deaths by incrementing our counter every time we die
  @On(bot, 'death')
  def bot_on_death(this):
    global deaths
    deaths = deaths + 1
    logging.info(f"I have died {deaths} times...")

  @On(bot, 'kicked')
  def bot_on_kicked(this, reason):
    bot.chat('I was kicked for a reason: %r', reason)

  @On(bot, 'error')
  def bot_on_error(this, error):
    bot.chat('I encountered an error: %r', error)

  @On(bot, CTFEvent.FLAG_OBTAINED)
  def bot_on_flag_obtained(this, collector):
    # If I was the one to obtain the flag, go and score!
    if collector == bot.username():
      rg_ctf_utils.scoreFlag()

  @On(bot, CTFEvent.FLAG_SCORED)
  def bot_on_flag_scored(this, team_name):
    # After scoring, send a message to chat
    bot.chat(f"Flag scored by ${team_name} team, waiting until it respawns")

  @On(bot, CTFEvent.FLAG_AVAILABLE)
  def bot_on_flag_available(this, flag_position: Vec3):
    # If flag is available run to get it
    bot.chat(
      f"Flag is available at ${bot.vecToString(flag_position)}, going to get it"
    )
    rg_ctf_utils.approachFlag()
