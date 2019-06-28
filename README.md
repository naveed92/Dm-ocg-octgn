This is the Duel Masters OCG Definition for OCTGN, and images.

I have updated the repo folder structure to be exactly like OCTGN's, so one can put the repository directly inside the OCTGN folder and see the changes reflected in OCTGN quickly.
The respective gitignore cases have been added.

If you want to help out in adding sets/images:
- Add the set folder inside GameDatabase/bb784fc6-fe21-4603-90d7-82c049908a74/Sets/
- Make a set.xml file inside
- Fill up the data inside in the same format as other set.xml files
- Each set, booster pack and card needs its own GUID. You can generate GUIDs on websites like this: https://www.guidgenerator.com/
- Inside image database, the folders should contain images named to their card IDs.
- If you have netBeans/java, you can use the extraction programs to quickly get card data and images in a compatible format, but it will require cleaning up later as the program sometimes can't deal with uniques cases on wikia set/card pages.

Note: All images must be 560 px or less in height, and must be in jpg format.

http://octgngames.com/dmocg/
