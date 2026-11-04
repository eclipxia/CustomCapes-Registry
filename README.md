# CustomCapes Registry

Public registry of capes for the [CustomCapes](https://github.com/eclipxia/CustomCapes) RusherHack plugin.
Players using the plugin download `capes.json` and show the cape listed for each player's UUID.
Nothing about the players around you is ever sent to this repo, the plugin only reads these files.

## Add your cape

1. Run `*cape uuid` in game (or look your UUID up with any UUID lookup site). Use the lowercase form with dashes.
2. Make a cape png: **64x32** (or 128x64, 256x128 ... up to 1024x512), max 256 KB.
   Vanilla cape layout, elytras use the same texture.
3. Fork this repo and add the file as `capes/<your-uuid>.png`.
4. Add a line to `capes.json`:
   ```json
   "<your-uuid>": "capes/<your-uuid>.png"
   ```
5. Open a pull request. CI (`scripts/validate.py`) checks the file and the entry.

Only add a cape for **your own** account. To change or remove it, open another pull request.

## Rules

- No offensive, hateful or illegal content.
- One cape per UUID.
