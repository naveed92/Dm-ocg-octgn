This is what will appear to be an extremely convoluted collection of programs- because they were never really meant to be used by people other than me.
Extremely user-unfriendly.


Caution: 
This is a netBeans project, so I'll advise installing it instead of simply running the programs with pure Java. 
It should be possible, but I've never tried.

Just run MainClass.java
Optionally you can edit the line that invokes the extractSet method and put set URL there. Otherwise the program will ask you for the URL.
I've accounted for most wikia set page structures up till Episode 2, but pages after that MIGHT have a new structure that cannot be processed,
or gives wonky results. It's just a bunch of strict decision-based text processing.

There are already 3 versions of the extractor class:

SinnanSetExtractor - General version. Usually works for everything, except-
SinnanSetExtractorDMD - Use this for extracting DMD sets
SinnanSetExtractorV2 - Use this if you want only the "New Cards" section mentioned specifically. For example on the page https://duelmasters.fandom.com/wiki/DMX-12_Black_Box_Pack

It's 90% possible that some conditional error will pop during usage in which case you'll have to dive deep into the code to fix it.
I've commented a lot wherever possible but the code is still messy as hell. Good luck with it.

-------------------------------------------------------------------------------------------------------------------
For doubts you can contact me. At the time of writing this document, 
the best way to do that would be to join the discord channel mentioned in the chat page of http://dmoctgn.proboards.com/
Seek me out there.

-Nitrox.



