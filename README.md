# meme police
the discord bot that polices your bad memes (and also my very first python project!)

## to-do

#### reaction features
- [x] basic delete functionality + phrases
    - [ ] bot command to change delete emoji
- [ ] basic reward functionality + phrases
    - [ ] bot command to change reward emoji
- [ ] bot command to change number of reacts required for action
- [ ] restrict these commands to certain permission groups

#### logistics
- [x] bot command to restrict functionality to a specific channel (`!restrict`)
- [ ] display usage message if channel has not been set
    - [ ] give option to not set a channel restriction
- [ ] channel check function that enforces restriction if set, or displays usage
- [ ] cache deleted messages in a separate channel
    - [ ] make it so this channel can be configured during setup
- [ ] help command

#### other fun stuff
- [ ] ticketing system and leaderboard
    - [ ] give leaders funny roles