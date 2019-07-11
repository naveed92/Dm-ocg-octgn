This is the Duel Masters OCG Definition for OCTGN, and images.

You don't need to how to program/script to contribute. Just need to know a bit about how git works.
You can use GitHub desktop, it's very user friendly.

For updates/corrections to card text for already exising/work-in-progress sets:
- Fork the repo
- Find the set folder inside GameDatabase/bb784fc6-fe21-4603-90d7-82c049908a74/Sets/
- You can edit the set xml file directly on GitHub
- Propose file change, it'll automatically create a pull request(or you may do that manually)
- Someone with write permissions will approve your change, and it'll show in the main fork.

If you want to help out in adding new sets/images:
- Fork the repo
- Add the set folder inside GameDatabase/bb784fc6-fe21-4603-90d7-82c049908a74/Sets/
- Make a set.xml file inside
- Fill up the data inside in the same format as other set.xml files
- Each set, booster pack and card needs its own GUID. You can generate GUIDs on websites like this: https://www.guidgenerator.com/
- Inside image database, the folders should contain images named to their card IDs.
- If you have netBeans/java, you can use the extraction programs to quickly get card data and images in a compatible format, but it will require cleaning up later as the program sometimes can't deal with uniques cases on wikia set/card pages.

Note: All images must be 560 px or less in height, and must be in jpg format.


All automations are based on python. OCTGN plugin dev refernce:
https://github.com/octgn/OCTGN/wiki
https://github.com/octgn/OCTGN/wiki/OCTGN-Python-3.1.0.2-API-Reference


OCTGNGames page:
https://octgngames.com/dmocg/

Discord server:
https://discord.gg/Zr23NH2

Forums:
https://dmoctgn.proboards.com
