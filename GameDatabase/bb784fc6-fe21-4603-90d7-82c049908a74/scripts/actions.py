#------------------------------------------------------------------------------
# Constant and Variables Values
#------------------------------------------------------------------------------
import re
import itertools
import time

shields = []
playerside = None
sideflip = None
diesides = 20
shieldMarker = ('Shield', 'a4ba770e-3a38-4494-b729-ef5c89f561b7')

# Start of Automation code

cardScripts = {
		# ON PLAY EFFECTS
				'Alshia, Spirit of Novas': { 'onPlay': { 'search': ['me.piles["Graveyard"]', '1', '"Spell"'] }},
				'Akashic Second, Electro-Spirit': { 'onPlay': { 'draw': ['me.Deck', 'True'] }},
				'Aures, Spirit Knight': { 'onPlay': { 'mana': ['me.Deck'] }},
				'Aqua Bouncer': { 'onPlay': { 'bounce': [] }},
				'Aqua Deformer': { 'onPlay': { 'fromMana': ['2', '"ALL"', '"ALL"', '"ALL"', 'True', 'False', 'True'] }},
				'Aqua Hulcus': { 'onPlay': { 'draw': ['me.Deck', 'True'] }},
				'Aqua Hulk': { 'onPlay': { 'draw': ['me.Deck', 'True'] }},
				'Aqua Sniper': { 'onPlay': { 'bounce': ['2'] }},
				'Aqua Surfer': { 'onPlay': { 'bounce': [] }},
				'Armored Decimator Valkaizer': { 'onPlay': {  'kill': ['4000'] }},
				'Artisan Picora': { 'onPlay': { 'fromMana': ['1','"ALL"','"ALL"','"ALL"','False','True'] }}, 
				'Astral Warper': { 'onPlay': { 'draw': ['me.Deck', 'True', '3'] }},
				'Baban Ban Ban, Earth\'s Blessing': { 'onPlay': { 'massMana': ['me.Deck', 'True'] }},
				'Ballom, Master of Death': { 'onPlay': { 'destroyAll': ['table', 'True', '"ALL"', '"Darkness"', 'True'] }},
				'Bega, Vizier of Shadow': { 'onPlay': { 'shields': ['me.Deck'] , 'targetDiscard': ['True'] }},
				'Belix, the Explorer': { 'onPlay': { 'fromMana': ['1','"Spell"'] }},
				'Bronze-Arm Tribe': { 'onPlay': { 'mana': ['me.Deck'] }},
				'Bronze Chain Sickle': { 'onPlay': { 'mana': ['me.Deck'] }},
				'Buinbe, Airspace Guardian': { 'onPlay': { 'draw': ['me.Deck', 'True'] }},
				'Chaos Worm': { 'onPlay': {  'kill': [] }},
				'Chief De Baula, Machine King of Mystic Light': { 'onPlay': { 'search': ['me.piles["Graveyard"]', '1', '"Spell"'] }},
				'Cobalt Hulcus, Aqua Savage': { 'onPlay': { 'draw': ['me.Deck', 'True'] }},
				'Craze Valkyrie, the Drastic': { 'onPlay': { 'tapCreature': ['2'] }},
				'Crimson Maru, the Untamed Flame': { 'onPlay': {  'kill': ['4000'] }},
				'Cyber N World': { 'onPlay': {  'semiReset': [] }},
				'Dacity Dragoon, Explosive Beast': { 'onPlay': {  'kill': ['3000'] }},
				'Dandy Eggplant': { 'onPlay': { 'fromDeck': [] }},
				'Dark Hydra, Evil Planet Lord': { 'onPlay': { 'fromGrave': [] }},
				'Death Mendosa, Death Dragonic Baron': { 'onPlay': { 'kill': ['"ALL"','"Untap"'] }},
				'Emperor Himiko': { 'onPlay': { 'draw': ['me.Deck', 'True'] }},
				'Emperor Marco': { 'onPlay': { 'draw': ['me.Deck', 'False', '3'] }},
				'Estol, Vizier of Aqua': { 'onPlay': { 'shields': ['me.Deck'] }},
				'Evolution Totem': { 'onPlay': {  'search': ['me.Deck', '1', '"Evolution Creature"'] }},
				'Factory Shell Q': { 'onPlay': {  'search': ['me.Deck', '1', '"ALL"', '"ALL"', '"Survivor"'] }},
				'Fighter Dual Fang': { 'onPlay': {  'mana': ['me.Deck','2'] }},
				'Fist Dragoon': { 'onPlay': { 'kill': ['2000'] }},
				'Flameburn Dragon': { 'onPlay': { 'kill': ['4000'] }},
				'Fonch, the Oracle': { 'onPlay': {  'tapCreature': [] }},
				'Forest Sword, Great Hero': { 'onPlay': { 'mana': ['me.Deck'] }},
				'Fortress Shell': { 'onPlay': {  'destroyMana': ['2'] }},
				'Forbos, Sanctum Guardian Q': { 'onPlay': {  'search': ['me.Deck', '1', '"Spell"'] }},
				'Funky Wizard': { 'onPlay': {  'draw': ['me.Deck', 'True'] }},
				'Galek, the Shadow Warrior': { 'onPlay': { 'targetDiscard': ['True'] }},
				'Gardner, the Invoked': { 'onPlay': { 'gear': ['"mana"'] }},
				'Gigargon': { 'onPlay': {  'search': ['me.piles["Graveyard"]', '2', '"Creature"'] }},
				'Gigabalza': { 'onPlay': { 'targetDiscard': ['True'] }},
				'Grave Worm Q': { 'onPlay': { 'search': ['me.piles["Graveyard"]', '1', '"ALL"', '"ALL"', '"Survivor"'] }},
				'Gunes Valkyrie, Holy Vizier': { 'onPlay': { 'tapCreature': [] }},
				'Gylus, Larval Lord': { 'onPlay': { 'targetDiscard': ['True'] }},
				'Gyulcas, Sage of the East Wind': { 'onPlay': {  'search': ['me.Deck', '1', '"Cross Gear"'] }},
				'Hawkeye Lunatron': { 'onPlay': { 'search': ['me.Deck', '1', '"ALL"', '"ALL"', '"ALL"', 'False'] }},
				'Honenbe, Skeletal Guardian':  { 'onPlay': { 'mill': ['me.Deck', '3', 'True'], 'search': ['me.piles["Graveyard"]', '1', '"Creature"'] }},
				'Hormone, Maxim Bronze': { 'onPlay': { 'mana': ['me.Deck'] }},				
				'Hot Spring Crimson Meow': { 'onPlay': { 'draw': ['me.Deck', 'True'] }},
				'Hulk Crawler': { 'onPlay': { 'draw': ['me.Deck', 'True'] }},
				'Hurlosaur': { 'onPlay': {  'kill': ['1000'] }},
				'Iron Arm Tribe': { 'onPlay': { 'mana': ['me.Deck'] }},
				'Izana Keeza': { 'onPlay': {  'kill': ['2000'] }},
				'Jasmine, Mist Faerie': { 'onPlay': { 'suicide': ['"Jasmine, Mist Faerie"', 'mana', 'me.Deck'] }},
				'Jelly, Dazzling Electro-Princess': { 'onPlay': { 'draw': ['me.Deck', 'True'] }},
				'Jenny, the Dismantling Puppet': { 'onPlay': {  'targetDiscard': [] }},
				'Jenny, the Suicide Doll': { 'onPlay': { 'suicide': ['"Jenny, the Suicide Doll"', 'targetDiscard', 'True'] }},
				'Jet R.E, Brave Vizier': { 'onPlay': { 'shields': ['me.Deck'] }},
				'King Ripped-Hide': { 'onPlay': { 'draw': ['me.Deck', 'True', '2'] }},
				'Kolon, the Oracle': { 'onPlay': { 'tapCreature': [] }},
				'Lena, Vizier of Brilliance': { 'onPlay': { 'fromMana': ['1','"Spell"'] }},
				'Lugias, The Explorer': { 'onPlay': { 'tapCreature': [] }},
				'Locomotiver': { 'onPlay': { 'targetDiscard': ['True'] }},
				'Magris, Vizier of Magnetism': { 'onPlay': { 'draw': ['me.Deck', 'True'] }},
				'Masked Horror, Shadow of Scorn': { 'onPlay': { 'targetDiscard': ['True'] }},
				'Meteosaur': { 'onPlay': { 'kill': ['2000'] }},
				'Miele, Vizier of Lightning': { 'onPlay': { 'tapCreature': [] }},
				'Moors, the Dirty Digger Puppet': { 'onPlay': {  'search': ['me.piles["Graveyard"]'] }},
				'Muramasa\'s Socket': { 'onPlay': {  'kill': ['1000'] }},
				'Murian': { 'onPlay': { 'suicide': ['"Murian"', 'draw', 'me.Deck'] }},
				'Niofa, Horned Protector': { 'onPlay': { 'search': ['me.Deck', '1', '"ALL"', '"Nature"'] }},
				'Ochappi, Pure Hearted Faerie': { 'onPlay': { 'fromGrave': [] }},
				'Pakurio': { 'onPlay': {  'targetDiscard': ['False','"shields"'] }},
				'Phal Eega, Dawn Guardian': { 'onPlay': { 'search': ['me.piles["Graveyard"]', '1', '"Spell"'] }},
				'Phal Pierro, Apocalyptic Guardian': { 'onPlay': { 'suicide': ['"Phal Pierro, Apocalyptic Guardian"', 'fromGrave', ''] }},
				'Phal Reeze, Apocalyptic Sage': { 'onPlay': { 'search': ['me.piles["Graveyard"]', '1', '"Spell"'] }},
				'Piara Heart': { 'onPlay': {  'kill': ['1000'] }},
				'Pointa, the Aqua Shadow': { 'onPlay': { 'targetDiscard': ['True'] }},
				'Prometheus, Splash Axe': { 'onPlay': { 'mana': ['me.Deck', '2', 'False', 'True'] } },
				'Qurian': { 'onPlay': { 'draw': ['me.Deck', 'True'] }},
				'Raiden, Lightfang Ninja': { 'onPlay': { 'tapCreature': [] }},
				'Rayla, Truth Enforcer': { 'onPlay': { 'search': ['me.Deck', '1', '"Spell"'] }},
				'Rom, Vizier of Tendrils': { 'onPlay': { 'tapCreature': [] }},
				'Rothus, the Traveler': { 'onPlay': { 'sacrifice': [] }},
				'Romanesk, the Dragon Wizard': { 'onPlay': {  'mana': ['me.Deck', '4'] }},
				'Rumbling Terahorn': { 'onPlay': { 'search': ['me.Deck', '1', '"Creature"'] }},
				'Ryokudou, the Principle Defender': { 'onPlay': { 'mana': ['me.Deck','2'], 'fromMana': [] }},
				'Sarvarti, Thunder Spirit Knight': { 'onPlay': { 'search': ['me.piles["Graveyard"]', '1', '"Spell"'] }},
				'Scissor Scarab': { 'onPlay': { 'search': ['1','"ALL"','"ALL"','"Giant Insect"'] }},
				'Shtra': { 'onPlay': {  'fromMana': ['1', '"ALL"', '"ALL"', '"ALL"', 'True', 'False', 'True'] }},
				'Self-Destructing Gil Poser': { 'onPlay': { 'suicide': ['"Self-Destructing Gil Poser"', 'kill', '2000'] }},
				'Sir Navaal, Thunder Mecha Knight': { 'onPlay': { 'fromMana': ['1','"Spell"'] }},
				'Sir Virginia, Mystic Light Insect': { 'onPlay': {  'search': ['me.piles["Graveyard"]', '1', '"Creature"'] }},
                'Skysword, the Savage Vizier': { 'onPlay': {  'skysword': ['me.Deck'] }},
				'Solidskin Fish': { 'onPlay': { 'fromMana': [] }},
				'Spiritual Star Dragon': { 'onPlay': { 'fromDeck': [] }},
				'Splash Zebrafish': { 'onPlay': { 'fromMana': [] }},
				'Syforce, Aurora Elemental': { 'onPlay': { 'fromMana': ['1','"Spell"'] }},
				'Terradragon Zalberg': { 'onPlay': {  'destroyMana': ['2'] }},
				'Thorny Mandra': { 'onPlay': {  'fromGrave': [] }},
				'Thrash Crawler': { 'onPlay': {  'fromMana': [] }},
				'Titan Giant': {'onPlay': { 'mana' : ['me.Deck', '2', 'True'] }},
				'Torpedo Cluster': { 'onPlay': {  'fromMana': [] }},
				'Triple Mouth, Decaying Savage': { 'onPlay': { 'mana': ['me.Deck'], 'targetDiscard': ['True'] }},
				'Unicorn Fish': { 'onPlay': { 'bounce': [] }},
				'Velyrika Dragon': { 'onPlay': { 'search': ['me.Deck', '1', '"ALL"', '"ALL"', '"Armored Dragon"'] }},
				'Viblo Blade, Hulcus Range': { 'onPlay': { 'draw': ['me.Deck', 'True'] }},				
				'Walmiel, Electro-Sage': { 'onPlay': { 'tapCreature': [] }},
				'Whispering Totem': { 'onPlay': { 'fromDeck': [] }},
				'Wind Axe, the Warrior Savage': { 'onPlay': {  'mana': ['me.Deck'] }},
				'Zardia, Spirit of Bloody Winds': { 'onPlay': {  'shields': ['me.Deck'] }},
				'Zemechis, the Explorer': { 'onPlay': {  'gear': ['"kill"'] }},
		# ON CAST EFFECTS
				'Abduction Charger': { 'onPlay': {  'bounce': ['2'] }},
				'Apocalypse Day': { 'onPlay': {  'destroyAll': ['table', 'len([card for card in table if isCreature(card)])>5'] }},			
				'Big Beast Cannon': { 'onPlay': { 'kill': ['7000'] }},
				'Blizzard of Spears': { 'onPlay': {  'destroyAll': ['table', 'True', '4000'] }},
				'Bomber Doll': { 'onPlay': { 'kill': ['2000'] }},
				'Bone Dance Charger':  { 'onPlay': { 'mill': ['me.Deck', '2'] }},
				'Boomerang Comet': { 'onPlay': { 'fromMana': [], 'toMana': ['card'] }},
				'Brain Cyclone': { 'onPlay': { 'draw': ['me.Deck', 'False', '1'] }},
				'Brain Serum': { 'onPlay': {  'draw': ['me.Deck', 'False', '2'] }},
				'Burst Shot': { 'onPlay': {  'destroyAll': ['table', 'True', '2000'] }},
				'Cannonball Sling': { 'onPlay': { 'kill': ['2000'] },
									  'onMetaMorph': { 'kill': ['6000'] }},
				'Chains of Sacrifice': { 'onPlay': { 'kill': ['"ALL"','"ALL"','"ALL"','2'], 'sacrifice': [] }},
				'Clone Factory': { 'onPlay': {  'fromMana': ['2'] }},
				'Cloned Nightmare': { 'onPlay': {  'targetDiscard': ['True'] }},
				'Corpse Charger': { 'onPlay': {  'search': ['me.piles["Graveyard"]', '1', '"Creature"'] }},
				'Crimson Hammer': { 'onPlay': { 'kill': ['2000'] }},
				'Cyber Brain': { 'onPlay': { 'draw': ['me.Deck', 'False', '3'] }},
				'Crystal Memory': { 'onPlay': { 'search': ['me.Deck', '1', '"ALL"', '"ALL"', '"ALL"', 'False'] }}, 
				'Darkflame Drive': { 'onPlay': { 'kill': ['"ALL"','"Untap"'] }},
				'Dark Reversal': { 'onPlay': { 'search': ['me.piles["Graveyard"]', '1', '"Creature"'] }},
				'Death Chaser': { 'onPlay': { 'kill': ['"ALL"','"Untap"'] }},
				'Death Gate, Gate of Hell': { 'onPlay': { 'kill': ['"ALL"','"Untap"'], 'fromGrave': [] }},
				'Death Smoke': { 'onPlay': { 'kill': ['"ALL"','"Untap"'] }},
				'Decopin Crash': { 'onPlay': { 'kill': ['4000'] }},
				'Devil Hand': { 'onPlay': { 'kill': [], 'mill':['me.Deck', '3', 'True'] }},
				'Devil Smoke': { 'onPlay': { 'kill': ['"ALL"','"Untap"'] }},
				'Dimension Gate': { 'onPlay': { 'search': ['me.Deck', '1', '"Creature"'] }},
				'Dracobarrier': { 'onPlay': { 'tapCreature': [] }},
				'Drill Bowgun': { 'onPlay': { 'gear': ['"kill"'] }},
				'Enchanted Soil': { 'onPlay': { 'fromGrave': [] }},
				'Energy Stream': { 'onPlay': { 'draw': ['me.Deck', 'False', '2'] }},
				'Eureka Charger': { 'onPlay': { 'draw': ['me.Deck'] }},
				'Eureka Program': { 'onPlay': { 'eurekaProgram': ['True'] }},
                'Faerie Crystal': { 'onPlay': { 'mana': ['me.Deck'] }},
				'Faerie Life': { 'onPlay': { 'mana': ['me.Deck'] }},
				'Faerie Miracle': { 'onPlay': { 'mana': ['me.Deck'] }},
				'Faerie Shower': { 'onPlay': { 'lookAtTopCards': ['2','"card"','"hand"','"mana"'] }},
				'Flame-Absorbing Palm': { 'onPlay': { 'kill': ['2000'] }},
				'Fire Crystal Bomb': { 'onPlay': { 'kill': ['5000'] }},
				'Flame Lance Trap': { 'onPlay': { 'kill': ['5000'] }},
				'Flood Valve': { 'onPlay': { 'fromMana': [] }},
				'Gardening Drive': { 'onPlay': { 'mana': ['me.Deck'] }},
				'Gatling Cyclone': { 'onPlay': {  'kill': ['2000'] }},
				'Ghost Clutch': { 'onPlay': { 'targetDiscard': ['True'] }},
				'Ghost Touch': { 'onPlay': { 'targetDiscard': ['True'] }},
				'Goren Cannon': { 'onPlay': { 'kill': ['3000'] }},
                'Goromaru Communication': { 'onPlay': { 'search': ['me.Deck', '1', '"Creature"'] }},
				'Hell Chariot': { 'onPlay': { 'kill': ['"ALL"','"Untap"'] }},
				'Hide and Seek': { 'onPlay': { 'bounceAndDiscard':[] }},
				'Hogan Blaster': { 'onPlay': { 'drama': ['True', '"creature or spell"', '"battlezone"', '"top"'] }},				
				'Holy Awe': { 'onPlay': { 'tapCreature': ['1','True'] }},
				'Hopeless Vortex': { 'onPlay': { 'kill': [] }},
				'Hyperspatial Storm Hole': { 'onPlay': { 'kill': ['5000'] }},
				'Hyperspatial Bolshack Hole': { 'onPlay': { 'kill': ['5000'] }},
				'Hyperspatial Kutt Hole': { 'onPlay': { 'kill': ['5000'] }},
				'Hyperspatial Guard Hole': { 'onPlay': { 'sendToShields': [] }},
				'Hyperspatial Vice Hole': { 'onPlay': {  'targetDiscard': [] }},
				'Hyperspatial Shiny Hole': { 'onPlay': { 'tapCreature': [] }},
				'Hyperspatial Energy Hole': { 'onPlay': { 'draw': ['me.Deck', 'False', '1'] }},
				'Hyperspatial Faerie Hole': { 'onPlay': { 'mana': ['me.Deck'] }},
				'Hyperspatial Revive Hole': { 'onPlay': { 'search': ['me.piles["Graveyard"]', '1', '"Creature"'] }},
				'Infernal Smash': { 'onPlay': { 'kill': [] }},
				'Intense Vacuuming Twist': { 'onPlay': { 'lookAtTopCards': ['5'] }},				
				'Invincible Abyss': { 'onPlay': { 'destroyAll': ['[card for card in table if card.owner != me]', 'True'] }},
				'Invincible Aura': { 'onPlay': { 'shields': ['me.Deck', '3', 'True'] }},
				'Invincible Technology': { 'onPlay': { 'search': ['me.Deck','len(me.Deck)'] }},
                'Lifeplan Charger': { 'onPlay': { 'lookAtTopCards': ['5', '"Creature"'] }},
				'Lightning Charger': { 'onPlay': { 'tapCreature': [] }},
				'Like a Rolling Storm':  { 'onPlay': { 'mill': ['me.Deck', '3', 'True'], 'search': ['me.piles["Graveyard"]', '1', '"Creature"'] }},
				'Lionic Phantom Dragon\'s Flame': { 'onPlay': {  'kill': ['2000'] }},
				'Living Lithograph': { 'onPlay': { 'mana': ['me.Deck'] }},
				'Logic Cube': { 'onPlay': { 'search': ['me.Deck', '1', '"Spell"'] }},
				'Logic Sphere': { 'onPlay': { 'fromMana': ['1', '"Spell"'] }},
				'Lost Soul': { 'onPlay': { 'discardAll': [] }},
				'Mana Crisis': { 'onPlay': { 'destroyMana': [] }},
				'Martial Law': { 'onPlay': { 'gear': ['"kill"'] }},
				'Magic Shot - Arcadia Egg': { 'onPlay': { 'kill': ['"ALL"','"Untap"'] }},
				'Magic Shot - Chain Spark': { 'onPlay': { 'tapCreature': [] }},
				'Magic Shot - Open Brain': { 'onPlay': { 'draw': ['me.Deck', 'False', '2'] }},
				'Magic Shot - Panda Full Life': { 'onPlay': { 'mana': ['me.Deck'] }},
				'Magic Shot - Soul Catcher': { 'onPlay': {  'search': ['me.piles["Graveyard"]', '1', '"Creature"'] }},
				'Magic Shot - Sword Launcher': { 'onPlay': {  'kill': ['3000'] }},
				'Mana Bonanza': { 'onPlay': { 'massMana': ['me.Deck', 'False'] }},
				'Miraculous Rebirth': { 'onPlay': { 'kill': ['5000'], 'fromDeck': [] }},
				'Miraculous Snare': { 'onPlay': { 'sendToShields': [] }},
				'Moonlight Flash': { 'onPlay': { 'tapCreature': ['2'] }},
				'Morbid Medicine': { 'onPlay': { 'search': ['me.piles["Graveyard"]', '2', '"Creature"'] }},
				'Mystery Cube': { 'onPlay': { 'drama': [] }},				
				'Mystic Dreamscape': { 'onPlay': { 'fromMana': ['3'] }},
				'Mystic Inscription': { 'onPlay': { 'shields': ['me.Deck'] }},
				'Natural Snare': { 'onPlay': { 'sendToMana': [] }},
				'Persistent Prison of Gaia': { 'onPlay': { 'bounceAndDiscard':[]}},
				'Phantom Dragon\'s Flame': { 'onPlay': {  'kill': ['2000'] }},
				'Phantasm Clutch': { 'onPlay': { 'kill': ['"ALL"','"Tap"'] }},
				'Pixie Cocoon': { 'onPlay': { 'fromMana': ['1', '"Creature"'], 'toMana': ['card'] }},
				'Pixie Life': { 'onPlay': { 'mana': ['me.Deck'] }},
				'Primal Scream':  { 'onPlay': { 'mill': ['me.Deck', '4', 'True'], 'search': ['me.piles["Graveyard"]', '1', '"Creature"'] }},				
				'Punish Hold': { 'onPlay': { 'tapCreature': ['2'] }},
				'Purgatory Force': { 'onPlay': { 'search': ['me.piles["Graveyard"]', '2', '"Creature"'] }},
				'Reap and Sow': { 'onPlay': { 'mana': ['me.Deck'], 'destroyMana': [] }},		
				'Reaper Hand': { 'onPlay': { 'kill': [] }},		
				'Reflecting Ray': { 'onPlay': { 'tapCreature': [] }},
				'Reverse Cyclone': { 'onPlay': { 'tapCreature': [] }},
				'Riptide Charger': { 'onPlay': {  'bounce': [] }},
				'Skeleton Vice': { 'onPlay': { 'targetDiscard': ['True'], 'targetDiscard': ['True'] }},
				'Samurai Decapitation Sword': { 'onPlay': {  'kill': ['5000'] }},
				'Screw Rocket': { 'onPlay': { 'gear': ['"kill"'] }},
				'Searing Wave': { 'onPlay': { 'destroyShield': ['False'] }},
				'Seventh Tower': { 'onPlay': { 'mana': ['me.Deck'] },
									'onMetamorph': { 'mana': ['me.Deck','3'] }},
				'Solar Grace': { 'onPlay': { 'tapCreature': [] }},
				'Solar Ray': { 'onPlay': { 'tapCreature': [] }},
				'Solar Trap': { 'onPlay': { 'tapCreature': [] }},
				'Spastic Missile': { 'onPlay': {  'kill': ['3000'] }},
				'Spiral Drive': { 'onPlay': { 'bounce': [] }},
				'Spiral Gate': { 'onPlay': { 'bounce': [] }},
				'Spiral Lance': { 'onPlay': { 'gear': ['"bounce"'] }},
				'Stronghold of Lightning and Flame': { 'onPlay': { 'kill': ['3000'], 'tapCreature': [] }},
				'Super Burst Shot': { 'onPlay': {  'destroyAll': ['[card for card in table if card.owner != me]', 'True', '2000'] }},
				'Super Infernal Gate Smash': { 'onPlay': { 'kill': [] }},
				'Super Spark': { 'onPlay': { 'tapCreature': ['1','True'] }},
				'Teleportation': { 'onPlay': { 'bounce': ['2'] }},
				'Ten-Ton Crunch': { 'onPlay': { 'kill': ['3000'] }},
				'Terror Pit': { 'onPlay': { 'kill': [] }},
				'The Strong Spiral': { 'onPlay': { 'bounce': [] }},
				'The Strong Breath': { 'onPlay': { 'kill': ['"ALL"','"Untap"'] }},
				'Timeless Garden': { 'onPlay': { 'mana': ['me.Deck'] }},
				'Tornado Flame': { 'onPlay': {  'kill': ['4000'] }},
				'Transmogrify': { 'onPlay': { 'killAndSearch': ['True'] }},
				'Triple Brain': { 'onPlay': { 'draw': ['me.Deck', 'False', '3'] }},
				'Ultimate Force': { 'onPlay': {  'mana': ['me.Deck', '2'] }},
				'Vacuum Ray': { 'onPlay': { 'tapCreature': [] }},
				'Valiant Spark': { 'onPlay': {  'tapCreature': [] },
									'onMetamorph': { 'tapCreature': ['1','True'] }},
				'Volcano Charger': { 'onPlay': { 'kill': ['2000'] }},
				'Wave Rifle': { 'onPlay': { 'gear': ["bounce"] }},
				'White Knight Spark': { 'onPlay': { 'tapCreature': ['1','True'] }},
				'Wizard Resurrection': { 'onPlay': { 'mana': ['me.Deck'], 'fromMana': ['1','"Spell"'] }},
				'XENOM, the Reaper Fortress': { 'onPlay': {  'targetDiscard': ['True'] }},
				'Zombie Carnival': { 'onPlay': { 'fromGrave': [] }},
				'Zombie Cyclone': { 'onPlay': {  'search': ['me.piles["Graveyard"]', '1', '"Creature"'] }},
		# ON BANISH EFFECTS
				'Akashic First, Electro-Dragon': { 'onDestroy': { 'toHand': ['card'] }},
				'Akashic Second, Electro-Spirit': { 'onPlay': { 'draw': ['me.Deck', 'True'] }, 'onDestroy': { 'toMana': ['card'] }},
				'Aqua Agent': { 'onDestroy': { 'toHand': ['card'] }},
				'Aqua Knight': { 'onDestroy': { 'toHand': ['card'] }},
				'Aqua Ranger': { 'onDestroy': { 'toHand': ['card'] }},
				'Aqua Skydiver': { 'onDestroy': {  'toHand': ['card'] }},
				'Aqua Soldier': { 'onDestroy': { 'toHand': ['card'] }},
				'Aqua Warrior': { 'onDestroy': {  'draw': ['me.Deck', 'True', '2'] }},
				'Asylum, the Dragon Paladin': { 'onDestroy': {  'toShields': ['card'] }},
				'Bat Doctor, Shadow of Undeath': { 'onDestroy': {  'search': ['me.piles["Graveyard"]', '1', '"Creature"'] }},
				'Bone Piercer': { 'onDestroy': { 'fromMana': ['1', '"Creature"'] }},
				'Bruiser Dragon': { 'onDestroy': { 'destroyShield': ['False'] }},
				'Cetibols': { 'onDestroy': {  'draw': ['me.Deck', 'True'] }},
				'Chillias, the Oracle': { 'onDestroy': {  'toHand': ['card'] }},
				'Coiling Vines': { 'onDestroy': { 'toMana': ['card'] }},
				'Crasher Burn': { 'onDestroy': { 'kill': ['3000'] }},
				'Crystal Jouster': { 'onDestroy': { 'toHand': ['card'] }},
				'Cubela, the Oracle': { 'onDestroy': { 'tapCreature': [] }},
				'Death Monarch, Lord of Demons': { 'onDestroy': { 'SummonFromGrave': ['len([card for card in me.piles["Graveyard"] if not re.search("Evolution",card.type)])', '"Creature"', '"ALL"', '"Demon Command"']}},
				'Dracodance Totem': { 'onDestroy': { 'fromMana': ['1','"ALL"','"ALL"','"Dragon"'], 'toMana': ['card'] }},
				'Fly Lab, Crafty Demonic Tree': { 'onDestroy': { 'targetDiscard': ['True'] }},
				'Glider Man': { 'onDestroy': { 'targetDiscard': [] }},
				'Hammerhead Cluster': { 'onDestroy': { 'bounce': [] }},
				'Jil Warka, Time Guardian': { 'onDestroy': {  'tapCreature': ['2'] }},
				'Mighty Shouter': { 'onDestroy': { 'toMana': ['card'] }},
				'Ouks, Vizier of Restoration': { 'onDestroy': {  'toShields': ['card'] }},
				'Peace Lupia': { 'onDestroy': { 'tapCreature': [] }},
				'Peru Pere, Viral Guardian': { 'onDestroy': { 'toHand': ['card'] }},
				'Pharzi, the Oracle': { 'onDestroy': { 'search': ['me.piles["Graveyard"]', '1', '"Spell"'] }},
				'Propeller Mutant': { 'onDestroy': { 'targetDiscard': ['True'] }},
				'Proxion, the Oracle': { 'onDestroy': { 'toHand': ['card'] }},
				'Shaman Broccoli': { 'onDestroy': { 'toMana': ['card'] }},
				'Shout Corn': { 'onDestroy': { 'toMana': ['card'] }},
				'Solid Horn': { 'onDestroy': { 'toMana': ['card'] }},
				'Stubborn Jasper': { 'onDestroy': { 'toHand': ['card'] }},
				'Red-Eye Scorpion': { 'onDestroy': { 'toMana': ['card'] }},
				'Worm Gowarski, Masked Insect': { 'onDestroy': { 'targetDiscard': ['True'] }},
	}
######### Events ##################

def endTurn(args):
	mute()
	nextPlayer = args.player
	if nextPlayer == None:
		#normally passed without green button
		currentPlayers = getPlayers()
		if len(currentPlayers)==2:
			nextPlayer = currentPlayers[1]
		else:
			whisper("Please use the green arrows to pass the turn!")
			return
	
	if turnNumber() == 0 or getActivePlayer() == me:
		if nextPlayer == me:
			if turnNumber() != 0:
				whisper("You can't pass the turn to yourself!")
				return
			else:
				nextTurn(me, True)
		notify("{} ends their turn.".format(me))
		remoteCall(nextPlayer, 'untapAll', table)
		nextTurn(nextPlayer, True)
	
def resetGame():
	mute()
	me.setGlobalVariable("shieldCount", "0")
#########intermediate automation functions#########

def askCard2(list, title="Select a card", buttonText="Select", numberToTake=1):  #askCard function was changed. So using the same name but with the new functionality
	dlg = cardDlg(list)
	dlg.title= title
	
	if numberToTake == 0:
		dlg.min, dlg.max = 0,0
		dlg.text = "Card Order(drag to rearrange):"
		dlg.show()
		return dlg.list
	result = dlg.show()
	
	if result is None:		
		return None
	return result[0]

def askYN(text="Proceed?", c1="Yes", c2= "No"):
	choiceList = [c1, c2]
	colorsList = ['#FF0000', '#FF0000']
	choice = askChoice(text, choiceList, colorsList)
	return choice
	

################ Functions used in the Automation dictionaries.####################

def SummonFromGrave(count=1, TypeFilter = "ALL", CivFilter = "ALL", RaceFilter = "ALL", noEvo = True): #Temporary Fix for not allowing Evolutions
	mute()
	for i in range(0,count):
		if TypeFilter != "ALL" and noEvo:
			cardsInGroup_Type_Filtered = [card for card in me.piles["Graveyard"] if re.search(TypeFilter,card.Type) and not re.search("Evolution",card.type)]
		else:
			cardsInGroup_Type_Filtered = [card for card in me.piles["Graveyard"]]
		if CivFilter != "ALL":
			cardsInGroup_CivandType_Filtered = [card for card in cardsInGroup_Type_Filtered if re.search(CivFilter,card.properties['Civilization'])]
		else:
			cardsInGroup_CivandType_Filtered = [card for card in cardsInGroup_Type_Filtered]
		if RaceFilter != "ALL":
			cardsInGroup_CivTypeandRace_Filtered = [card for card in cardsInGroup_CivandType_Filtered if re.search(RaceFilter,card.properties['Race'])]
		else:
			cardsInGroup_CivTypeandRace_Filtered = [card for card in cardsInGroup_CivandType_Filtered]
		if len(cardsInGroup_CivTypeandRace_Filtered) == 0: return
		choice = askCard2(cardsInGroup_CivTypeandRace_Filtered, 'Choose a Card  to Summon from the Graveyard','Graveyard')
		if type(choice) is not Card: break
		toPlay(choice)

def drama(shuffle = True, type = 'creature', targetZone = 'battlezone', failZone = 'mana', conditional = True):
	mute()
	if shuffle:
		me.Deck.shuffle()
		notify("{} shuffles their deck.".format(me))
	card = me.Deck.top()
	card.isFaceUp = True
	notify("Top card is {}".format(card))
	played = False #Flag for resolving after shuffle, unused rn
	if type == 'creature':
		success = re.search("Creature", card.Type)
	elif type == 'creature or spell':
		success = re.search("Creature", card.Type) or re.search("Spell", card.Type)
	if success:
		if conditional:
			choiceList = ['Yes', 'No']
			colorsList = ['#FF0000', '#FF0000']
			choice = askChoice("Put {} into {}?\n\n {}".format(card.Name, targetZone, card.Rules), choiceList, colorsList)
			#more conditions for non-bz?
			if choice == 1:
				toPlay(card)
				played = True
				return
		else:
			toPlay(card)
			played = True
			return
	if failZone == 'mana':
		toMana(card)
	elif failZone == 'hand':
		toHand(card)
	else:
		notify("{} puts {} back on top of deck".format(me, card))
		card.isFaceUp = False
	
def lookAtTopCards(num, cardType='card', targetZone='hand', remainingZone = 'bottom'):
	mute()
	notify("{} looks at the top {} cards of their deck".format(me,num))
	cardList = [card for card in me.Deck.top(num)]
	choice = askCard2(cardList, 'Choose a card to put into {}'.format(targetZone))
	if type(choice) is Card:
		if cardType == 'card' or re.search(cardType, choice.Type):
			#use switch instead, when more zones are added here
			if targetZone == 'mana':
				toMana(choice)
			else:
				#to hand is default rn
				toHand(choice, show = True)	
		else:
			notify("Please select a {}! Action cancelled.".format(cardType))
			return
	else:
		notify("Nothing selected! Action cancelled.")
		return
	cardList = [card for card in me.Deck.top(num-1)]
	#will it always be 1 card that goes into target zone? Account for more in later upgrades
	if len(cardList)>1 and remainingZone=='bottom':
		cardList = askCard2(cardList, 'Rearrange the remaining cards to put to {}'.format(remainingZone),'OK', 0)
	for card in cardList:
			if remainingZone == 'mana':
				toMana(card)
			else:
				card.moveToBottom(me.Deck)
				notify("{} moved a card to the bottom of their deck.".format(me))
	
def targetDiscard(randomDiscard = False, targetZone = 'grave'):
	mute()
	currentPlayers = getPlayers()
	playerList = []
	cardList = []
	for player in currentPlayers:
		playerList.append(player.name)
	choicePlayer = askChoice("Pick a player:", playerList)
	if choicePlayer < 1: return
	targetPlayer = currentPlayers[choicePlayer-1]
	cardList = [card for card in targetPlayer.hand]
	if randomDiscard:
		remoteCall(targetPlayer,'randomDiscard',targetPlayer.hand)
		return
	cardChoice = cardDlg(cardList)
	cardChoice.title= 'Choose a Card to discard'
	cardChoice.text="{}'s hand".format(targetPlayer)
	cardChoice  = cardChoice.show()[0]
	if type(cardChoice) is not Card: 
		notify("{} - Error".format(type(cardChoice)))
		return
	if targetZone == 'shields': 
		whisper("Setting {} as shield.".format(cardChoice))
		remoteCall(targetPlayer,'toShields',cardChoice) 
	elif targetZone == 'grave':
		remoteCall(targetPlayer,'toDiscard',cardChoice)
	
def discardAll():
	mute()
	currentPlayers = getPlayers()
	playerList = []
	cardList = []
	for player in currentPlayers:
		playerList.append(player.name)
	choicePlayer = askChoice("Pick a player:", playerList)
	if choicePlayer < 1: return
	targetPlayer = currentPlayers[choicePlayer-1]
	cardList = [card for card in targetPlayer.hand]
	for card in cardList:
		remoteCall(targetPlayer, 'toDiscard', card)
		
def fromMana(count = 1, TypeFilter = "ALL", CivFilter = "ALL", RaceFilter = "ALL", show = True, toGrave = False, ApplyToAllPlayers = False):
	mute()
	if ApplyToAllPlayers == True:
		playerList = players
	else:
		playerList = [players[0]]
	for player in playerList:
		for i in range(0,count):
			if TypeFilter != "ALL":
				cardsInGroup_Type_Filtered = [card for card in table if isMana(card) and card.owner==me and re.search(TypeFilter,card.Type)]
			else:
				cardsInGroup_Type_Filtered = [card for card in table if isMana(card) and card.owner==me]
			if CivFilter != "ALL":
				cardsInGroup_CivandType_Filtered = [card for card in cardsInGroup_Type_Filtered if re.search(CivFilter,card.properties['Civilization'])]
			else:
				cardsInGroup_CivandType_Filtered = [card for card in cardsInGroup_Type_Filtered]
			if RaceFilter != "ALL":
				cardsInGroup_CivTypeandRace_Filtered = [card for card in cardsInGroup_CivandType_Filtered if re.search(RaceFilter,card.properties['Race'])]
			else:
				cardsInGroup_CivTypeandRace_Filtered = [card for card in cardsInGroup_CivandType_Filtered]
			if len(cardsInGroup_CivTypeandRace_Filtered) == 0: return
			choice = askCard2(cardsInGroup_CivTypeandRace_Filtered, 'Choose a Card from the Mana Zone','Mana Zone')
			if type(choice) is not Card: break
			if toGrave == True: remoteCall(player,"destroy",choice)
			else: remoteCall(player,"toHand",[choice, show])

def killAndSearch(play = False, singleSearch = False):
	mute()
	cardList = [card for card in table if isCreature(card) and re.search("Creature", card.Type)]
	if len(cardList)==0: return	
	choice = askCard2(cardList, 'Choose a Creature to destroy')
	if type(choice) is not Card: return
	card = choice
	remoteCall(choice.owner,'destroy',choice)
	if singleSearch:
		return
	else:
		remoteCall(choice.owner,'loopThroughDeck',[card, play])

def loopThroughDeck(card, play = False):
	group = card.owner.Deck
	if len(group) == 0: return
	newCard = group[0]
	newCard.isFaceUp = True
	notify("{} reveals {}".format(card.owner,newCard.Name))
	rnd(1,1000)
	if re.search("Creature", newCard.Type) and not re.search("Evolution Creature", newCard.Type):
		if play == True:
			remoteCall(newCard.owner,'toPlay',newCard)
			return
		else:
			remoteCall(newCard.owner,'moveTo',newCard.owner.hand)
			return
	else:
		remoteCall(newCard.owner,'toDiscard',newCard)
		remoteCall(newCard.owner,'loopThroughDeck',[card, play])


def eurekaProgram(ask = True):
	mute()
	cardList = [card for card in table if isCreature(card) and re.search("Creature", card.Type) and card.owner == me]
	cardList = [card for card in cardList if not re.search("Psychic", card.Type)]
	if len(cardList)==0: return	
	
	choice = askCard2(cardList, 'Choose a Creature to destroy')
	if type(choice) is not Card: return
	originalCost = int(choice.Cost)
	found = False
	notify("Cost is {}".format(originalCost))
	destroy(choice)
	for card in me.Deck:
		card=me.Deck[0]
		card.isFaceUp = True
		cost = int(card.Cost)
		notify("{} reveals {}".format(me,card))
		rnd(1,10)
		if (int(card.Cost) - originalCost) == 1:
			if re.search("Creature", card.Type):
				if not re.search("Evo", card.Type):
					if ask:
						yn = askYN("Put {} into {}?\n\n {}".format(card.Name, targetZone, card.Rules))
						if(yes == 1)
							found = True
							toPlay(card, ignoreEffects=True)
							choice = card
						##add card to resolve list
					break			
				else:
					if ask:
						yn = askYN("Put {} into {}?\n\n {}".format(card.Name, targetZone, card.Rules))
						if(yn == 1)
							found = True
							toPlay(card, ignoreEffects=True)	
							choice = card
							##add card to resolve list					
							card.moveToTable(0,0)
							align()
					break
		card.moveToBottom(me.Deck)
	for card in me.Deck:
		if card.isFaceUp:
			card.isFaceUp = False
	me.Deck.shuffle()
	notify("{} shuffles their deck.".format(me))
	if found:
	## Temporary fix without a proper resolve list
		toPlay(choice, notifymute = True)


""""def volgMill(askChoice = True):
	mute()
	if(askChoice)
		currentPlayers = getPlayers()
		playerList = []
		for player in currentPlayers:
			playerList.append(player.name)
		choicePlayer = askChoice("Pick a player:", playerList)
		if choicePlayer < 1: return
		targetPlayer = currentPlayers[choicePlayer-1]
	group = targetPlayer.Deck
	if len(group) == 0: return
	newCard = group[0]
	newCard.isFaceUp = True
	notify("{} reveals {}".format(card.owner,newCard.name))
	rnd(1,1000)
	if re.search("Creature", newCard.Type) and not re.search("Evolution Creature", newCard.Type):
		if play == True:
			remoteCall(newCard.owner,'toPlay',newCard)
			return
		else:
			remoteCall(newCard.owner,'moveTo',newCard.owner.hand)
			return
	else:
		remoteCall(newCard.owner,'toDiscard',newCard)
		remoteCall(newCard.owner,'loopThroughDeck',[card, play])
"""
def search(group, count = 1, TypeFilter = "ALL" , CivFilter = "ALL", RaceFilter = "ALL", show = True, x = 0, y = 0):
	mute()
	if len(group) == 0: return
	for i in range(0,count):
		cardsInGroup = [card for card in group]
		if TypeFilter != "ALL":
			cardsInGroup_Type_Filtered = [card for card in group if re.search(TypeFilter,card.Type)]
		else:
			cardsInGroup_Type_Filtered = [card for card in group]
		if CivFilter != "ALL":
			cardsInGroup_CivandType_Filtered = [card for card in cardsInGroup_Type_Filtered if re.search(CivFilter,card.properties['Civilization'])]
		else:
			cardsInGroup_CivandType_Filtered = [card for card in cardsInGroup_Type_Filtered]
		if RaceFilter != "ALL":
			cardsInGroup_CivTypeandRace_Filtered = [card for card in cardsInGroup_CivandType_Filtered if re.search(RaceFilter,card.properties['Race'])]
		else:
			cardsInGroup_CivTypeandRace_Filtered = [card for card in cardsInGroup_CivandType_Filtered]
		while (True):
			choice = askCard2(cardsInGroup, 'Search card to take to hand (1 at a time)')
			if type(choice) is not Card: 
				group.shuffle()
				notify("{} finishes searching his/her {}.".format(me, group.name))
				return
			if choice in cardsInGroup_CivTypeandRace_Filtered:
				toHand(choice, show)
				break
	group.shuffle()
	notify("{} finishes searching his/her {}.".format(me, group.name))

def kill(powerFilter = 'ALL', tapFilter='ALL', civFilter='ALL', count = 1, targetOwn = False):
	mute()
	if powerFilter == 'ALL':
		powerFilter = float('inf')
	for i in range(0, count):
		if targetOwn:
			cardList = [card for card in table if isCreature(card) and int(card.Power) <= powerFilter]
		else:
			cardList = [card for card in table if isCreature(card) and not card.owner==me and int(card.Power) <= powerFilter]
		if tapFilter != 'ALL':
			if tapFilter == 'Untap':
				cardList = [card for card in cardList if card.orientation == Rot0]
			if tapFilter == 'Tap':
				cardList = [card for card in cardList if card.orientation == Rot90]
		if civFilter != "ALL":
			cardList = [card for card in cardList if re.search(civFilter,card.Civilization)]
		if len(cardList)==0:
			return	
		choice = askCard2(cardList, 'Choose a Creature to destroy')
		if type(choice) is not Card:
			return
		if choice.owner == me:
			destroy(choice)
		else:
			remoteCall(choice.owner,"destroy",choice)

def destroyAll(group, condition = False, powerFilter = 'ALL', civFilter = "ALL", AllExceptFiltered = False):
	mute()
	if powerFilter == 'ALL':
		powerfilter = float('inf')
	if condition == False:
		return
	cardlist = []
	if civFilter == "ALL":
		cardList = [card for card in group if isCreature(card) and int(card.Power) <= powerFilter]
	else:
		if AllExceptFiltered:
			cardList = [card for card in group if isCreature(card) and int(card.Power) <= powerFilter and not re.search(civFilter,card.properties['Civilization'])]
		else:
			cardList = [card for card in group if isCreature(card) and int(card.Power) <= powerFilter and re.search(civFilter,card.properties['Civilization'])]
	if len(cardList)==0:
		return
	for card in cardList:
		cardToBeSaved = card
		possibleSavers = [card for card in table if cardToBeSaved != card and isCreature(card) and card.owner == me and re.search("Saver",card.rules) and (re.search(cardToBeSaved.properties['Race'],card.rules) or re.search("Saver: All Races",card.rules))]
		if len(possibleSavers) > 0:
			if confirm("Prevent {}'s destruction by using a Saver on your side of the field?\n\n".format(cardToBeSaved.Name)):
				choice = askCard2(possibleSavers, 'Choose Saver to destroy')
				if type(choice) is Card:
					toDiscard(choice)
					cardList.remove(choice)
					cardList = [card for card in cardList]
					notify("{} destroys {} to prevent {}'s destruction.".format(me, choice.name, cardToBeSaved.name))
					continue
		if cardToBeSaved.owner == me:	
			toDiscard(cardToBeSaved)
			
			if cardScripts.get(card.name,{}).get('onDestroy',{}):
				functionDict = cardScripts.get(card.name).get('onDestroy')
				for function in functionDict:
					argList = functionDict.get(function)
					eval(function)(*[eval(arg) for arg in argList])
		else:
			remoteCall(cardToBeSaved.owner,"destroy",cardToBeSaved)

def destroyMana(count = 1):
	mute()
	for i in range(0,count):
		cardList = [card for card in table if isMana(card) and not card.owner==me]
		if len(cardList)==0:
			return
		choice = askCard2(cardList, 'Choose a Mana Card to destroy')
		if type(choice) is not Card:
			return		
		remoteCall(choice.owner,"destroy",choice)

def destroyShield(owner = True):
	mute()
	if owner == True:
			cardList = [card for card in table if isShield(card) and not card.owner==me]
	else:
			cardList = [card for card in table if isShield(card) and card.owner==me]
	if len(cardList)==0:
			return
	choice = askCard2(cardList, 'Choose a shield to send to graveyard')
	if type(choice) is not Card:
			return		
	remoteCall(choice.owner,"destroy",[choice,True])
		
def fromDeck():
	mute()
	notify("{} looks at their Deck.".format(me))
	me.Deck.lookAt(-1)

def fromGrave():
	mute()
	notify("{} looks at their Graveyard.".format(me))
	me.piles['Graveyard'].lookAt(-1)

def lookAtCards(count = 1, isTop = True):
	mute()
	if isTop == False: 
		notify("{} looks at {} cards from bottom of their deck.".format(me, count))
	notify("{} looks at {} cards from top of their deck.".format(me, count))
	me.Deck.lookAt(count, isTop)

def sacrifice(power = float('inf'), count = 1):
	mute()
	for i in range(0, count):
		cardList = [card for card in table if isCreature(card) and card.owner==me and re.search("Creature", card.Type)]
		cardList = [card for card in cardList if int(card.Power) <= power]
		if len(cardList)==0:
			return	
		choice = askCard2(cardList, 'Choose a Creature to destroy')
		if type(choice) is not Card:
			return
		destroy(choice)
	
def bounce(count = 1, opponentOnly = False):
	mute()
	for i in range(0,count):
		if opponentOnly:
			cardList = [card for card in table if isCreature(card) and re.search("Creature", card.Type) and card.owner != me]
		else:	
			cardList = [card for card in table if isCreature(card) and re.search("Creature", card.Type)]
		if len(cardList) < 1:
			return
		choice = askCard2(cardList,'Choose a Creature to return to Hand')
		if type(choice) is not Card:
			return
		if choice.owner==me:
			toHand(choice)
		else:
			remoteCall(choice.owner,"toHand",choice)
	
def bounceAndDiscard(bcount = 1, opponentOnly = True, randomDiscard=True):
	mute()
	bounce(bcount, opponentOnly)
	targetDiscard(randomDiscard)
	
def gear(str):		
	mute()
	if str == 'kill':
		cardList = [card for card in table if isGear(card)
					and not card.owner == me]
		if len(cardList) == 0:
			return
		choice = askCard2(cardList,'Choose a Cross Gear to send to Graveyard')
		if type(choice) is not Card:
			return
		remoteCall(choice.owner, 'destroy', choice)
	elif str == 'bounce':
		cardList = [card for card in table if isGear(card)]
		if len(cardList) == 0:
			return
		choice = askCard2(cardList, 'Choose a Cross Gear to send to Hand')
		if type(choice) is not Card:
			return
		if choice.owner == me:
			toHand(choice)
		else:
			remoteCall(choice.owner, 'toHand', choice)
	elif str == 'mana':
		cardList = [card for card in table if isGear(card)]
		if len(cardList) == 0:
			return
		choice = askCard2(cardList, 'Choose a Cross Gear to send to Mana')
		if type(choice) is not Card:
			return
		if choice.owner == me:
			toHand(choice)
		else:
			remoteCall(choice.owner, 'toMana', choice)

def sendToShields(count=1):
	mute()
	for i in range(0,count):
			cardList = [card for card in table if isCreature(card) and card.owner != me]
			if len(cardList)==0: return
			choice = askCard2(cardList,'Choose a Creature to send to shields')
			if type(choice) is not Card: return
			remoteCall(choice.owner,"toShields",choice)

def sendToMana(count=1):
	mute()
	for i in range(0,count):
			cardList = [card for card in table if isCreature(card) and card.owner != me]
			if len(cardList)==0: return
			choice = askCard2(cardList,'Choose a Creature to send to mana')
			if type(choice) is not Card: return
			remoteCall(choice.owner,"toMana",choice)

def tapCreature(count = 1, targetALL = False, includeOwn = False):
	mute()
	if targetALL:
		if includeOwn == True: 
			cardList = [card for card in table if isCreature(card) and card.orientation == Rot0 and re.search("Creature", card.Type)]
		else:
			cardList = [card for card in table if isCreature(card) and card.orientation == Rot0 and not card.owner==me and re.search("Creature", card.Type)]
		if len(cardList)==0:
			return
		for card in cardList:
			remoteCall(card.owner,"tap",card)
	else:
		for i in range(0,count):
			if includeOwn == True: 
				cardList = [card for card in table if isCreature(card) and card.orientation == Rot0 and re.search("Creature", card.Type)]
			else:
				cardList = [card for card in table if isCreature(card) and card.orientation == Rot0 and not card.owner==me and re.search("Creature", card.Type)]
			if len(cardList)==0:
				return
			choice = askCard2(cardList, 'Choose a Creature to tap')
			if type(choice) is not Card:
				return
			remoteCall(choice.owner,"tap",choice)
		
def semiReset():
	mute()
	if confirm("Are you sure you want to continue?"):
		currentPlayers = getPlayers()	
		for player in currentPlayers:
			cardsInHand = [c for c in player.hand] 
			cardsInGrave = [c for c in player.piles['Graveyard']]
			if cardsInHand or cardsInGrave:
				for card in cardsInHand: 
					remoteCall(player, 'toDeckTop', card) 
				for card in cardsInGrave: 
					remoteCall(player, 'toDeckTop', card)
			remoteCall(player,'shuffle', player.deck)
			remoteCall(player,'draw', [player.deck, False, 5])

def suicide(name, action, arg):
	mute()
	choiceList = ['Yes', 'No']
	colorsList = ['#FF0000', '#FF0000']
	choice = askChoice("Destroy the card to activate effect?", choiceList, colorsList)
	if choice == 0 or choice == 2:
		return
	cardList = [card for card in table if isCreature(card) and card.owner==me and re.search("Creature", card.type)]
	cardList = [card for card in cardList if card.name==name]
	toDiscard(cardList[-1])
	action(arg)

#End of Automation Code

def awaken(card, x = 0, y = 0):
	mute()
	if (re.search("Psychic", card.Type)):
		altName = card.alternateProperty('awakening', 'name')
		if card.alternate is '':
			card.alternate = 'awakening'
			notify("{}'s' {} awakens to {}.".format(me, altName, card))
			align()
			return
		else:
			card.alternate = ''
			notify("{}'s {} reverts to {}.".format(me, altName, card))
			align()
			return

def toHyperspatial(card, x = 0, y = 0, notifymute = False):
	mute()
	if card.alternate is not '' and re.search("{RELEASE}", card.Rules):
		awaken(card)
		return
	else:
		card.moveTo(me.Hyperspatial)
		align()
		if notifymute == False:
			notify("{}'s {} returns to the Hyperspatial Zone.".format(me, card))

def moveCards(args):
	## This trigger updates the evolution dictionary in the event one of the cards involved in an evolution leaves the battlezone.
	mute()
	player = args.player
	card = args.cards[0]
	fromGroup = args.fromGroups[0]
	## Old vars are: player, card, fromGroup, toGroup, oldIndex, index, oldX, oldY, x, y, highlights, markers, faceup
	
	if player is not me: ##Ignore for cards you don't control
		return
	if table not in args.fromGroups: ## we only want cases where a card is being moved from table to another group
		notify("Ignored")
		return
	evolveDict = eval(me.getGlobalVariable("evolution"))
	for evo in evolveDict.keys():
		if Card(evo) not in table:
			del evolveDict[evo]
		else:
			evolvedList = evolveDict[evo]
			for evolvedCard in evolvedList:
				if Card(evolvedCard) not in table:
					evolvedList.remove(evolvedCard)
			if len(evolvedList) == 0:
				del evolveDict[evo]
			else:
				evolveDict[evo] = evolvedList
	if evolveDict != eval(me.getGlobalVariable("evolution")):
		me.setGlobalVariable("evolution", str(evolveDict))

def isCreature(card):
	mute()
	if card in table and card.isFaceUp and not card.orientation == Rot180 and not card.orientation == Rot270 and re.search("Creature", card.Type):
		return True
	else:
		return False

def isGod(card):
	mute()
	if card in table and card.isFaceUp and not card.orientation == Rot180 and not card.orientation == Rot270 and re.search("Creature", card.Type) and re.search("God", card.Race):
		return True
	else:
		return False

def isGear(card):
	mute()
	if card in table and card.isFaceUp and not card.orientation == Rot180 and not card.orientation == Rot270 and re.search("Cross Gear", card.Type):
		return True
	else:
		return False

def isFortress(card):
	mute()
	if card in table and card.isFaceUp and not card.orientation == Rot180 and not card.orientation == Rot270 and re.search("Fortress", card.Type):
		return True
	else:
		return False

def isMana(card):
	mute()
	if card in table and card.isFaceUp and not card.orientation == Rot90 and not card.orientation == Rot0:
		return True
	else:
		return False

def isShield(card):
	mute()
	if card in table and not card.isFaceUp:
		return True
	else:
		return False

def isPsychic(card):
	mute()
	if re.search("Psychic", card.Type):
		return True
	else:
		return False

def metamorph():
	mute()
	cardList = [card for card in table if isMana(card) and card.owner== me]
	if len(cardList) < 7:
		return False
	else:
		return True


def align():
	mute()
	global playerside  ##Stores the Y-axis multiplier to determine which side of the table to align to
	global sideflip  ##Stores the X-axis multiplier to determine if cards align on the left or right half
	if sideflip == 0:  ##the 'disabled' state for alignment so the alignment positioning doesn't have to process each time
		return "BREAK"
	if Table.isTwoSided():
		if playerside == None:  ##script skips this if playerside has already been determined
			if me.isInverted:
				playerside = -1  #inverted (negative) side of the table
			else:
				playerside = 1
		if sideflip == None:  ##script skips this if sideflip has already been determined
			playersort = sorted(getPlayers(), key=lambda player: player._id)  ##makes a sorted players list so its consistent between all players
			playercount = [p for p in playersort if me.isInverted == p.isInverted]  ##counts the number of players on your side of the table
			if len(playercount) > 2:  ##since alignment only works with a maximum of two players on each side
				whisper("Cannot align: Too many players on your side of the table.")
				sideflip = 0  ##disables alignment for the rest of the play session
				return "BREAK"
			if playercount[0] == me:  ##if you're the 'first' player on this side, you go on the positive (right) side
				sideflip = 1
			else:
				sideflip = -1
	else:  ##the case where two-sided table is disabled
		whisper("Cannot align: Two-sided table is required for card alignment.")
		sideflip = 0  ##disables alignment for the rest of the play session
		return "BREAK"
	cardorder = [[],[],[]]
	evolveDict = eval(me.getGlobalVariable("evolution"))
	for card in table:
		if card.controller == me and not isFortress(card) and not card.anchor and not card._id in list(itertools.chain.from_iterable(evolveDict.values())):
			if isShield(card):
				cardorder[1].append(card)
			elif isMana(card):
				cardorder[2].append(card)
			else: ##collect all creatures
				cardorder[0].append(card)
	xpos = 80
	ypos = 5 + 10*(max([len(evolveDict[x]) for x in evolveDict]) if len(evolveDict) > 0 else 1)
	for cardtype in cardorder:
		if cardorder.index(cardtype) == 1:
			xpos = 80
			ypos += 93
		elif cardorder.index(cardtype) == 2:
			xpos = 80
			ypos += 93
		for c in cardtype:
			x = sideflip * xpos
			y = playerside * ypos + (44*playerside - 44)
			if c.position != (x,y):
				c.moveToTable(x,y)
			xpos += 79
	for evolution in evolveDict:
		count = 0
		for evolvedCard in evolveDict[evolution]:
			x, y = Card(evolution).position
			count += 1
			Card(evolvedCard).moveToTable(x, y - 10*count*playerside)
			Card(evolvedCard).sendToBack()

def clear(card, x = 0, y = 0):
	mute()
	card.target(False)

def setup(group, x = 0, y = 0):
	mute()
	
	cardsInTable = [c for c in table if c.controller == me and c.owner == me and not isPsychic(c)]
	cardsInHand = [c for c in me.hand if not isPsychic(c)]
	cardsInGrave = [c for c in me.piles['Graveyard'] if not isPsychic(c)]
	
	psychicsInTable = [c for c in table if c.controller == me and c.owner == me and isPsychic(c)]
	psychicsInHand = [c for c in me.hand if isPsychic(c)]
	psychicsInGrave = [c for c in me.piles['Graveyard'] if isPsychic(c)]
	
	if cardsInTable or cardsInHand or cardsInGrave or psychicsInTable or psychicsInGrave or psychicsInHand:
		if confirm("Are you sure you want to setup battlezone? Current setup will be lost"):
			
			for card in cardsInTable:
				card.moveTo(me.Deck)
			for card in cardsInHand:
				card.moveTo(me.Deck)
			for card in cardsInGrave:
				card.moveTo(me.Deck)

			for card in psychicsInTable:
				card.moveTo(me.Hyperspatial)
			for card in psychicsInHand:
				card.moveTo(me.Hyperspatial)
			for card in psychicsInGrave:
				card.moveTo(me.Hyperspatial)
		else:
			return
	if len(me.Deck) < 10: #We need at least 10 cards to properly setup the game
		whisper("Not enough cards in deck")
		return

	cardsInDeck = [c for c in me.Deck]
	for card in cardsInDeck:
		if isPsychic(card):
			whisper("You cannot have Psychic creatures in your main deck")
			return

	me.setGlobalVariable("shieldCount", "0")
	me.setGlobalVariable("evolution", "{}")
	me.Deck.shuffle()
	rnd(1,10)
	for card in me.Deck.top(5): toShields(card, notifymute = True)
	for card in me.Deck.top(5): card.moveTo(card.owner.hand)
	align()
	notify("{} sets up their battle zone.".format(me))
			
def rollDie(group, x = 0, y = 0):
	mute()
	global diesides
	n = rnd(1, diesides)
	notify("{} rolls {} on a {}-sided die.".format(me, n, diesides))

def untapAll(group=table, x = 0, y = 0):
	mute()
	for card in group:
		if not card.owner == me:
			continue
		if card.orientation == Rot90:
			card.orientation = Rot0
		if card.orientation == Rot270:
			card.orientation = Rot180
	notify("{} untaps all their cards.".format(me))
	
def tap(card, x = 0, y = 0):
	mute()
	card.orientation ^= Rot90
	if card.orientation & Rot90 == Rot90:
		notify('{} taps {}.'.format(me, card))
	else:
		notify('{} untaps {}.'.format(me, card))

def destroy(card, dest = False, x = 0, y = 0):
	mute()
	if isShield(card):
		if dest == True:
			toDiscard(card)
			return
		card.peek()
		rnd(1,10)
		if re.search("{SHIELD TRIGGER}", card.Rules):
			if confirm("Activate Shield Trigger for {}?\n\n{}".format(card.Name, card.Rules)):
				rnd(1,10)
				notify("{} uses {}'s Shield Trigger.".format(me, card.Name))
				card.isFaceUp = True
				toPlay(card, notifymute = True)
				return
		shieldCard = card
		cardsInHandWithStrikeBackAbility = [card for card in me.hand if re.search("Strike Back", card.rules)]
		if len(cardsInHandWithStrikeBackAbility) > 0:
			cardsInHandWithStrikeBackAbilityThatCanBeUsed = [card for card in cardsInHandWithStrikeBackAbility if re.search(card.Civilization, shieldCard.Civilization)]
			if len(cardsInHandWithStrikeBackAbilityThatCanBeUsed) > 0:
				if confirm("Activate Strike Back by sending {} to the graveyard?\n\n{}".format(shieldCard.Name, shieldCard.Rules)):
					choice = askCard2(cardsInHandWithStrikeBackAbilityThatCanBeUsed, 'Choose Strike Back to activate')
					if type(choice) is Card:
						shieldCard.isFaceUp = True
						rnd(1,100)
						toPlay(choice, notifymute = True)
						toDiscard(shieldCard)
						notify("{} destroys {} to use {}'s Strike Back.".format(me, shieldCard.name, choice.name))
						return
		notify("{}'s shield #{} is broken.".format(me, shieldCard.markers[shieldMarker]))
		shieldCard.moveTo(shieldCard.owner.hand)
	else:
		cardToBeSaved = card
		possibleSavers = [card for card in table if cardToBeSaved != card and isCreature(card) and card.owner == me and re.search("Saver",card.rules) and (re.search(cardToBeSaved.properties['Race'],card.rules) or re.search("Saver: All Races",card.rules))]
		if len(possibleSavers) > 0:
				if confirm("Prevent {}'s destruction by using a Saver on your side of the field?\n\n".format(cardToBeSaved.Name)):
						choice = askCard2(possibleSavers, 'Choose Saver to destroy')
						if type(choice) is Card:
								toDiscard(choice)
								notify("{} destroys {} to prevent {}'s destruction.".format(me, choice.name, cardToBeSaved.name))
								return
		toDiscard(cardToBeSaved)
################# ON  DESTROY BUG HERE  PLS FIX ##############
		if cardScripts.get(card.name,{}).get('onDestroy',{}):
			functionDict = cardScripts.get(card.name).get('onDestroy')
			for function in functionDict:
				argList = functionDict.get(function)
				eval(function)(*[eval(arg) for arg in argList])


def shuffle(group, x = 0, y = 0):
	mute()
	if len(group)==0:return
	for card in group:
		if card.isFaceUp:
			card.isFaceUp = False
	group.shuffle()
	notify("{} shuffled their {}".format(me, group.name))

def draw(group, conditional = False, count = 1, x = 0, y = 0):
	mute()
	for i in range(0,count):
		if len(group) == 0:
			return
		if conditional == True:
			choiceList = ['Yes', 'No']
			colorsList = ['#FF0000', '#FF0000']
			choice = askChoice("Draw a card?", choiceList, colorsList)
			if choice == 0 or choice == 2:
				return 
		card = group[0]
		card.moveTo(card.owner.hand)
		notify("{} draws a card.".format(me))

def drawX(group, x = 0, y = 0):
	if len(group) == 0: return
	mute()
	count = askInteger("Draw how many cards?", 7)
	if count == None: return
	for card in group.top(count): card.moveTo(card.owner.hand)
	notify("{} draws {} cards.".format(me, count))
	
def mill(group, count=1, conditional = False, x = 0, y = 0):
	mute()
	if len(group) == 0:
		notify("No cards left in Deck!")
		return
	if conditional:	
		choiceList = ['Yes', 'No']
		colorsList = ['#FF0000', '#FF0000']
		choice = askChoice("Discard top {} cards?".format(count), choiceList, colorsList)
		if choice == 0 or choice == 2:
			return 
	if len(group) < count: count = len(group)
	for card in group.top(count):
		toDiscard(card, notifymute = True)
		notify("{} discards {} from top of Deck.".format(me, card))
	
def millX(group, x = 0, y = 0):
	mute()
	if len(group) == 0: return
	count = askInteger("Discard how many cards?", 1)
	if count == None: return
	for card in group.top(count): toDiscard(card, notifymute = True)
	notify("{} discards top {} cards of Deck.".format(me, count))

def randomDiscard(group, x = 0, y = 0):
	mute()
	if len(group) == 0: return
	card = group.random()
	toDiscard(card, notifymute = True)
	rnd(1,10)
	notify("{} randomly discards {}.".format(me, card))

def mana(group, count = 1, conditional = False, tapped = False):
	mute()
	if conditional:
		choiceList = ['Yes', 'No']
		colorsList = ['#FF0000', '#FF0000']
		choice = askChoice("Charge top {} cards as mana?".format(count), choiceList, colorsList)
		if choice == 0 or choice == 2:
			return 
	for i in range(0,count):
		if len(group) == 0: return
		card = group[0]
		toMana(card, notifymute = True)
		if tapped and card.orientation & Rot90 != Rot90:
					card.orientation ^= Rot90
		notify("{} charges {} from top of {} as mana.".format(me, card.name, group.name))
		
def skysword(group, count = 1, x = 0, y = 0):
	mute()
	for i in range(0,count):
		if len(group) == 0: return
		card = group[0]
		toMana(card, notifymute = True)
		notify("{} charges top card of {} as mana.".format(me, group.name))
	for i in range(0,count):
		card = group[0]
		toShields(card, notifymute = True)
		notify("{} places top card of {} as shield.".format(me, group.name))

def massMana(group, conditional = False, x=0, y=0):
		mute()
		cardList = [card for card in table if isMana(card) and card.owner== me]
		count = len(cardList)
		if conditional == True: 
			choiceList = ['Yes', 'No'] 
			colorsList = ['#FF0000', '#FF0000']
			choice = askChoice("Charge top {} cards to mana?".format(count), choiceList, colorsList)
			if choice == 0 or choice == 2: return 
		for i in range(0,count):		 
			if len(group) == 0: return
			card = group[0]		 
			toMana(card, notifymute = True)
			if card.orientation & Rot90 != Rot90:
					card.orientation ^= Rot90
		notify("{} charges top {} cards of {} as mana.".format(me, count, group.name))
	
def shields(group, count = 1, conditional = False, x = 0, y = 0):
	mute()
	if conditional == True:
		maxCount = count
		count = askInteger("Set how many cards as shields? (Max = {})".format(maxCount), maxCount)
		if count == 0 or count > maxCount: return
	for card in group.top(count):
		if len(group) == 0: return
		card = group[0]
		toShields(card, notifymute = True)
		notify("{} sets top card of {} as shield.".format(me, group.name))

def toMana(card, x = 0, y = 0, notifymute = False):
	mute()
	evolveDict = eval(me.getGlobalVariable('evolution'))
	if card._id in list(itertools.chain.from_iterable(evolveDict.values())):
		if not confirm("WARNING: There is an evolution creature on top of this card, and can not legally be placed into your mana zone.\nWould you like to override this?"):
			return
	if isMana(card):
		whisper("This is already mana")
		return
	if isPsychic(card):
		toHyperspatial(card)
		return
	card.moveToTable(0,0)
	card.orientation = Rot180
	if re.search("/", card.Civilization):
		card.orientation = Rot270
	if card._id in evolveDict:
		evolvedCardList = evolveDict[card._id]
		for evolvedCard in evolvedCardList:
			if Card(evolvedCard) in table:
				Card(evolvedCard).orientation = Rot180
		del evolveDict[card._id]
		me.setGlobalVariable('evolution', str(evolveDict))
	align()
	if notifymute == False:
		notify("{} charges {} as mana.".format(me, card))

def toShields(card, x = 0, y = 0, notifymute = False, alignCheck = True, ignoreEvo = False):
	mute()
	if isShield(card):
		whisper("This is already a shield.")
		return
	evolveDict = eval(me.getGlobalVariable('evolution'))
	if ignoreEvo == False and card._id in list(itertools.chain.from_iterable(evolveDict.values())):
		if not confirm("WARNING: There is an evolution creature on top of this card, and can not legally be placed into your shield zone.\nWould you like to override this?"):
			return
	if isPsychic(card):
		toHyperspatial(card)
		return
	count = int(me.getGlobalVariable("shieldCount")) + 1
	me.setGlobalVariable("shieldCount", convertToString(count))
	if notifymute == False:
		if isCreature(card) or isMana(card):  ##If a visible card in play is turning into a shield, we want to record its name in the notify
			notify("{} sets {} as shield #{}.".format(me, card, count))
		else:
			notify("{} sets a card in {} as shield #{}.".format(me, card.group.name, count))

	card.moveToTable(0,0,True)
	if card.isFaceUp:
		card.isFaceUp = False
	if card.orientation != Rot0:
		card.orientation = Rot0
	card.markers[shieldMarker] = count
	if card._id in evolveDict:
		evolvedCardList = evolveDict[card._id]
		for evolvedCard in evolvedCardList:
			if Card(evolvedCard) in table:
				toShields(Card(evolvedCard), alignCheck = False, ignoreEvo = True)
		del evolveDict[card._id]
		me.setGlobalVariable('evolution', str(evolveDict))
	if alignCheck:
		align()
		
def toPlay(card, x = 0, y = 0, notifymute = False, evolveText = '', ignoreEffects = False):
	mute()
	if re.search("Evolution", card.Type):
		targets = [c for c in table
					if c.controller == me
					and c.targetedBy
					and c.targetedBy == me]
		targets = [c for c in targets
					if isCreature(c)
					or isGear(c)]
		for c in targets:
			c.target(False) #remove the targets
		if len(targets) == 0:
			whisper("Cannot play card: You must target a creature to evolve first.")
			whisper("Hint: Shift-click a card to target it.")
			return
		else:
			targetList = [c._id for c in targets]
			evolveDict = eval(me.getGlobalVariable("evolution")) ##evolveDict tracks all cards 'underneath' the evolution creature
			for evolveTarget in targets: ##check to see if the evolution targets are also evolution creatures
				if evolveTarget._id in evolveDict: ##if the card already has its own cards underneath it
					if isCreature(evolveTarget):
						targetList += evolveDict[evolveTarget._id] ##add those cards to the new evolution creature
					del evolveDict[evolveTarget._id]
			evolveDict[card._id] = targetList
			me.setGlobalVariable("evolution", str(evolveDict))
			evolveText = ", evolving {}".format(", ".join([c.name for c in targets]))
	if card.group == table:
		card.moveTo(me.hand)
	card.moveToTable(0,0)
	if shieldMarker in card.markers:
		card.markers[shieldMarker] = 0
	align()
	if notifymute == False:
		notify("{} plays {}{}.".format(me, card, evolveText))
	
	if not ignoreEffects:
		if metamorph() and cardScripts.get(card.name,{}).get('onMetamorph',{}):
				functionDict = cardScripts.get(card.name).get('onMetamorph')
				for function in functionDict:
					argList = functionDict.get(function)
					eval(function)(*[eval(arg) for arg in argList])
		elif cardScripts.get(card.name,{}).get('onPlay',{}):
			functionDict = cardScripts.get(card.name).get('onPlay')
			for function in functionDict:
				argList = functionDict.get(function)
				eval(function)(*[eval(arg) for arg in argList])
			
	if card.Type == "Spell":
		if re.search("Charger", card.name) and re.search("Charger", card.rules):
			rnd(1,100)
			toMana(card)
		else:
			rnd(1,100)
			card.moveTo(card.owner.piles['Graveyard'])
			
	####### check some stack here for other play resolving(not implemented yet) #############
	
def toDiscard(card, x = 0, y = 0, notifymute = False, alignCheck = True, ignoreEvo = False):
	mute()
	evolveDict = eval(me.getGlobalVariable('evolution'))
	if ignoreEvo == False and isCreature(card) and card._id in list(itertools.chain.from_iterable(evolveDict.values())):
		if not confirm("WARNING: There is an evolution creature on top of this card, and can not legally be destroyed.\nWould you like to override this?"):
			return
	if isPsychic(card):
		toHyperspatial(card)
		return	
	src = card.group
	card.moveTo(card.owner.piles['Graveyard'])
	if card._id in evolveDict:
		evolvedCardList = evolveDict[card._id]
		for evolvedCard in evolvedCardList:
			if Card(evolvedCard) in table:
				toDiscard(Card(evolvedCard), alignCheck = False, ignoreEvo = True)
		del evolveDict[card._id]
		me.setGlobalVariable('evolution', str(evolveDict))
	if notifymute == False:
		if src == table:
			notify("{} destroys {}.".format(me, card))
			if alignCheck:
				align()
		else:
			notify("{} discards {} from {}.".format(me, card, src.name))

def toHand(card, show = True, x = 0, y = 0, alignCheck = True, ignoreEvo = False):
	mute()
	src = card.group
	evolveDict = eval(me.getGlobalVariable('evolution'))
	if ignoreEvo == False and isCreature(card) and card._id in list(itertools.chain.from_iterable(evolveDict.values())):
		if not confirm("WARNING: There is an evolution creature on top of this card, and can not legally be destroyed.\nWould you like to override this?"):
			return
	if isPsychic(card):
		toHyperspatial(card)
		return
	card.moveTo(card.owner.hand)
	if card._id in evolveDict:
		evolvedCardList = evolveDict[card._id]
		for evolvedCard in evolvedCardList:
			if Card(evolvedCard) in table:
				toHand(Card(evolvedCard), alignCheck = False, ignoreEvo = True)
		del evolveDict[card._id]
		me.setGlobalVariable('evolution', str(evolveDict))
	if show: 
		notify("{} moved {} to hand from {}.".format(me, card, src.name))
	else:
		whisper("Moving {} to hand from {}.".format(card, src.name))
	if alignCheck:
		align()

def toDeckTop(card, x = 0, y = 0):
	mute()
	toDeck(card)

def toDeckBottom(card, x = 0, y = 0):
	mute()
	toDeck(card, bottom = True)

def toDeck(card, bottom = False):
	mute()
	evolveDict = eval(me.getGlobalVariable('evolution'))
	if isCreature(card) and card._id in list(itertools.chain.from_iterable(evolveDict.values())):
		if not confirm("WARNING: There is an evolution creature on top of this card, and can not legally be destroyed.\nWould you like to override this?"):
			return
	if isPsychic(card):
		toHyperspatial(card)
		return
	cardList = [card]
	if card._id in evolveDict:
		evolvedCardList = evolveDict[card._id]
		for evolvedCard in evolvedCardList:
			if Card(evolvedCard) in table:
				cardList.append(Card(evolvedCard))
		del evolveDict[card._id]
		me.setGlobalVariable('evolution', str(evolveDict))
	while len(cardList) > 0:
		if len(cardList) == 1:
			choice = 1
		else:
			choice = askChoice("Choose a card to place it on top of your deck.", [c.name for c in cardList])
		if choice > 0:
			c = cardList.pop(choice - 1)
			if bottom == True:
				notify("{} moves {} to bottom of Deck.".format(me, c))
				c.moveToBottom(c.owner.Deck)
			else:
				notify("{} moves {} to top of Deck.".format(me, c))
				c.moveTo(c.owner.Deck)
	align()
