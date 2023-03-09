# Understanding our algorithm

_Hint - expand this pane to make reading the code a little easier for long lines of code._

In this guide, we are given a starting algorithm for our bot. Open the [start.py](#start.py)
file, and let's dig into our algorithm!

Before reading the code, let's lay out the overall algorithm. This bot has the following rules:
* When anyone says "start" in the chat, approach the flag
* If a flag is obtained, and it was the bot that received the flag, the bot attempts to walk back to base
* If a flag is scored, the bot says something in the chat
* If the flag becomes available, the bot runs toward the flag

You'll notice that our bot is not implementing some main loop that makes a decision
every tick of the game - rather, our bot responds to `events` (if you are not familiar
with event handlers, check out this [this resource](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Building_blocks/Events)).

More precisely, let's go through each part of our code to see how this works:

### The configureBot function

Every Regression Games bot must have a `configureBot` function. This is what our systems
use to configure and setup your bot. Therefore, every Regression Games bot you see will
have this setup.

```javascript
export function configureBot(bot) {
  // here is where you define how your bot behaves
  ...
}
```

The `bot` argument that gets passed in is a bot with no default behavior, but has
a bunch of helpful utilities, functions, and properties for programming your bot.
For example, we have `bot.approachBlock()` to move towards a specific block,
`bot.username()` to get the username of the bot, etc... You can see all of the
many utilities within our [rg-bot](https://play.regression.gg/documentation/rg-bot)
documentation.

### Setting up for Capture the Flag

The very first thing we do in our bot configuration is:
1. Tell our bot to not dig blocks while moving around. While useful in some game modes,
   in Capture the Flag a bot cannot dig parts of the map, so this is useful to make sure
   you don't get stuck.
2. We create an `rgctfUtils` object, which has utilities for the Capture the Flag mode.
   Not only does this give access to useful constants and functions like `approachFlag()`
   and `FLAG_SPAWN`, but it also registers event handlers for events that happen in the game.
   You can learn more about these utilities and events [here](https://github.com/Regression-Games/rg-ctf-utils/blob/main/src/rg-ctf-utils.ts).

```javascript
export function configureBot(bot) {
  // Since most blocks can't be broken on Arctic Algorithm Field,
  // don't allow digging while pathfinding
  bot.allowDigWhilePathing(false);

  // Instantiate our helper utilities and events for Capture the Flag
  const rgctfUtils = new RGCTFUtils(bot);

  ...
}
```

### Listening for chat events

Now, we register event handlers for a few different actions that might happen during the game.
First, we register an event handler to listen for chat messages. This code below listens
for players who say "start", and as long as it's not the bot that said it, it then calls
`rgctfUtils.approachFlag()`, which cause the bot to begin moving toward the flag!

```javascript
// When a player types "start" in the chat, the bot will begin
// looking for and approaching the flag
bot.on('chat', async (username, message) => {
  if (username === bot.username()) return;
  if (message === 'start') {
    bot.chat("Going to start capturing the flag!")
    await rgctfUtils.approachFlag()
  }
})
```

**Note on Asynchronous Operations / Await**: You'll see that our code here, and our code
in other places, uses `async/await` syntax. This means when this event handler is called,
the code will wait until the player reaches the flag to go onto the next line in the code.
You can learn more about asynchronous operations using 
[this resource](https://javascript.info/async-await).

### Scoring the flag if the bot gets the flag

One useful event that the game provides is a [`FLAG_OBTAINED` event](https://github.com/Regression-Games/rg-ctf-utils/blob/main/src/rg-ctf-utils.ts#L15-L31)
Whenever any player picks up the flag, this event is called, and we provide the username of the
player who collected the flag. In this particular code, we implement the logic of "if this specific
bot picked up the flag, have it walk back towards its base to score the flag".

_Pro-tip: Hover over the `CTFEvent.FLAG_OBTAINED` code to see an example of how to use this event._

```javascript
// When a player obtains the flag, this event gets called.
// In the case where that player is this bot, the bot
// navigates back to their scoring location.
bot.on(CTFEvent.FLAG_OBTAINED, async (collector) => {
  if (collector == bot.username()) {
    await rgctfUtils.scoreFlag()
  }
});
```

### Send a message when someone scores the flag

In this event, we do something quite simple - if the flag is scored by anyone, we say
something in the chat. Later one we will implement more logic here!

```javascript
// If the flag was scored, simply chat a message
bot.on(CTFEvent.FLAG_SCORED, async (teamName) => {
  bot.chat(`Flag scored by ${teamName} team, waiting until it respawns`)
})
```

### Go after the flag again if the flag appears

After scoring the flag, the flag does not immediately respawn. After 10 seconds, the
flag will respawn, at which point the `FLAG_AVAILABLE` event is sent. In this code
below, our bot is waiting for this event, and as soon as the flag is available, it
says something in the chat, and runs toward the flag. _Note that this event also
gets called when a player drops the flag._

```javascript
// Once the flag respawns on the map, look for and approach the flag.
bot.on(CTFEvent.FLAG_AVAILABLE, async (position) => {
  bot.chat("Flag is available, going to get it")
  await rgctfUtils.approachFlag();
})
```

### Next steps

As you can see, our bot is actually quite simple. It waits for certain things to happen in
the game, and then responds to them with specific logic. This "event-driven" approach is
only one way for bots to operates - you may choose to instead have a main loop that reads
the game state every few ticks of the game, and has the bot implement logic based on that state.
Regression Games is fairly flexible with what you can do, and has no restrictions on your logic
(other than the raw CPU you have available on our machines).

Let's move on to making our bot a little more complex and robust, as well as implement some
logic that allows our bot to use more of our utilities.