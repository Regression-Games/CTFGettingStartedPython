# Gather items and automatic start

Our bot is quite simple right now - it waits for us to say "start", and then
repeatedly gets the flag. Let's make this ready for a real multiplayer match,
by adding logic to:

1. Automatically start our logic when the match begins (vs a chat message)
2. Collect nearby items when waiting for the flag to respawn
3. Add robustness for respawning

**Note that you can find the final code within the [`final_code.js`](#final_code.js) file as well.**

## 1. Start our algorithm when the match starts

There are many different ways to determine when a bot joins the match, and when the match
starts. In this example, we are going to simply start our bot's logic when they connect.

```javascript
// ~~ Insert this right above our existing chat event handler
// ~~ ALSO: Delete the chat event handler after pasting this in
bot.on('spawn', async () => {
  await rgctfUtils.approachFlag();
});
```

Because our bots are only frozen in place before a match starts, this bot will try
to move towards the flag, but will be stuck until the match starts, at which point
it will move successfully. In some cases, you may need to wait until all bots are
connected and the match actually starts to run your code. You can find many examples
on how to do this in our [FAQ and Tutorial Page](https://www.notion.so/regressiongg/Waiting-for-the-Match-To-Start-ebcd15b4ba5943f3a3e2453d22070acc?pvs=4).

## 2. Collect nearby items

We will now update our code to collect nearby items until the flag is available again.
The `RGBot` class has a useful function, [`bot.findAndCollectItemsOnGround()`](https://staging.regression.gg/documentation/rg-bot#rgbotfindandcollectitemsongroundoptions--promisearrayitem),
which can do this for us automatically.

The tricky part here is that we need to **maintain some state that makes sure our bot
only does one operation at a time**. In other words, since we have event handlers, if
we are collecting an item, and the flag spawns, we don't want our event handler for
`FLAG_AVAILABLE` to cause our bot to approach the flag, as it may still be collecting
an item. It's important to keep track of state and respond to actions in a way that does
not result in your bot getting confused!

Update the `FLAG_SCORED` and `FLAG_AVAILABLE` event handlers to look like this:

```javascript
let isCollectingItems = false;

// If the flag was scored, collect items until the flag is available
bot.on(CTFEvent.FLAG_SCORED, async (teamName) => {
  bot.chat(`Flag scored by ${teamName} team, collecting items until new flag is here`)
  isCollectingItems = true;
  while(rgctfUtils.getFlagLocation() === null) {
    await bot.findAndCollectItemsOnGround();
    await bot.waitForMilliseconds(500);
  }
  isCollectingItems = false;
  await rgctfUtils.approachFlag();
})

// Once the flag respawns on the map, look for and approach the flag, only if
// we are not busy collecting items
bot.on(CTFEvent.FLAG_AVAILABLE, async (position) => {
  if (!isCollectingItems) {
    bot.chat("Flag is available, going to get it")
    await rgctfUtils.approachFlag();
  }
})
```

After scoring, the bot now continuously looks for items until the flag location 
is not null (i.e. the flag exists on the map), at which point it approaches the
flag. The bot also keeps track if it is collecting items, so that it won't try
to approach the flag if the flag spawns while items are being collected.

## 3. Add robustness for respawning

When a bot dies on Regression Games (i.e. respawns) your code is still
running, but events like `spawn` are called again. If you are not careful,
you could end up calling your "bot starting code" again, resulting in
interleaving logic (in our case, the bot having multiple event handlers
for the same events and multiple calls to `approachFlag()`).

In order to circumvent this, you can keep track of how many deaths your
bot has experienced, and stop running your logic if you detect a change
in the number of deaths. This tutorial here goes into more detail on how
to do this in a "main loop" format versus an event driven format as well.
**Note that restarting your bot (via code updates, for example) DOES result
in a hard refresh of your code, meaning that these issues won't happen in
those cases**

We will implement the following logic:

1. Add a new variable called `deaths` that tracks the death counter for this bot
2. Add an event handler for death events to increase that counter and terminate
   any ongoing pathfinding
3. Only run event handler logic if the death counter has not changed

Right before your `spawn` event handler, put the following code:

```javascript
// track how many times we've died
let deaths = 0

bot.on('death', () => {
  console.log("I have died...")
  ++deaths;
  try {
    // stop any current pathfinding goal
    // @ts-ignore
    bot.mineflayer().pathfinder.setGoal(null)
    // @ts-ignore
    bot.mineflayer().pathfinder.stop()
  } catch (ex) {

  }
})
```

Then, update your `FLAG_SCORED` logic to the following. Note that we are only
checking for death changes in this event handler because it is the only
event handler where we have multiple `await`ed pieces of navigation logic, meaning
that our death will cancel the currently running navigation logic, but still
move onto the next logic. Our code added here allows us to skip the following
navigationa if this event handler is no longer valid.

```javascript
// If the flag was scored, collect items until the flag is available
bot.on(CTFEvent.FLAG_SCORED, async (teamName) => {
  let previousDeaths = deaths
  const codeStillRunning = () => {return previousDeaths === deaths}
  bot.chat(`Flag scored by ${teamName} team, collecting items until new flag is here`)
  isCollectingItems = true;
  while(rgctfUtils.getFlagLocation() === null && codeStillRunning()) {
    await bot.findAndCollectItemsOnGround();
    await bot.waitForMilliseconds(500);
  }
  isCollectingItems = false;
  if (codeStillRunning()) await rgctfUtils.approachFlag();
})
```

If this part confused you... do not worry! We have more resources in 
[this tutorial](https://www.notion.so/regressiongg/Event-Driven-vs-Main-Loop-Bots-9a22780f930a4c05a2e2605267d55a6b?pvs=4), and we plan on having an update soon
where we will handle this automatically. If you continue to have problems with this
code, let us know in [Discord](https://discord.gg/925SYVse2H)!

Try commiting and pushing this new code to your bot - your bot will automatically
reload, and you should see it collect items in between flag spawns. At this point,
you can create a disconnect from this practice match, disband your lobby, and
create a new Battle match! Select your bot for all 3 slots of your team, queue
into a match, and see how it compares to other bots!