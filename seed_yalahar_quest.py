#!/usr/bin/env python3

import os
import sys
import django
from django.db import transaction

# Add the project directory to the Python path
sys.path.append('/home/tylermartin713/workspace/TibiaGGapi')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TibiaGGproject.settings')
django.setup()

from TibiaGGapi.models import Quest, QuestMission, QuestReward, QuestQuestReward, QuestDanger

def seed_yalahar_quest():
    with transaction.atomic():
        # Create the main quest
        quest = Quest.objects.create(
            name="In Service of Yalahar Quest",
            description="The new found island of Yalahar needs to be investigated thoroughly. A comprehensive quest involving exploration, moral choices between Palimuth (good) and Azerus (evil), and culminating in an epic final battle. Features access to city quarters, unique rewards, and the Yalaharian Outfit.",
            location="Edron, Liberty Bay, Yalahar",
            min_level=80,
            rec_level=120,
            is_premium=True,
            quest_type="main",
            difficulty_rating=5,
            estimated_duration="Several hours to complete all missions",
            prerequisites="Explorer Society membership (Novice rank or higher), various items and access requirements for different missions",
            npc_start="Wyrdin"
        )

        # Create all missions
        missions_data = [
            {
                "mission_order": 1,
                "name": "The Way to Yalahar",
                "description": "Get passage to Yalahar from Captain Max in Liberty Bay (or Captain Bluebear for free accounts with password). Find Timothy north of depot in Yalahar to get his research notes. Report back to Wyrdin in Edron for 500 gold reward.",
                "objective": "Retrieve Timothy's research notes from Yalahar and return them to Wyrdin",
                "steps": "Visit Wyrdin in Ivory Towers, Edron → Talk to Captain Max in Liberty Bay for passage → Find Timothy in Yalahar → Return research notes to Wyrdin → Meet Palimuth near city entrance",
                "location": "Edron, Liberty Bay, Yalahar",
                "required_items": "Travel money, Explorer Society membership",
                "notes": "First mission to access Yalahar. Free account alternative available through Wyrdin's Apprentice near Kazordoon.",
                "dangers": "None"
            },
            {
                "mission_order": 2,
                "name": "Searoutes around Yalahar",
                "description": "Optional mission to unlock ship routes from Yalahar to other cities. Bring 5 special items from different cities to Captain Karith to prove their worth for trade routes.",
                "objective": "Establish ship routes by providing 5 special items from different cities to Captain Karith",
                "steps": "Collect items from 5 cities: Piece of Royal Satin (Thais), Sample of Venorean Spice (Venore), Bottle of Bug Milk (Ab'Dendriel), Bowl of Evergreen Flowers (Carlin), Rum Flask (Liberty Bay), Tusk (Port Hope), Sample of Sand Wasp Honey (Darashia), Jug of Embalming Fluid (Ankrahmun)",
                "location": "Yalahar and various cities",
                "required_items": "5 special items from different cities (total cost ~1400gp)",
                "notes": "Optional but highly recommended for easier travel. Only need 5 of the 8 possible items.",
                "dangers": "Travel dangers between cities"
            },
            {
                "mission_order": 3,
                "name": "Something Rotten", 
                "description": "Fix 4 sewer problems in Yalahar using a crowbar or Whacking Driller of Fate. Locations are marked on your map. Clean the pipes and loosen rusty controls.",
                "objective": "Fix 4 sewer problems in Yalahar's underground system",
                "steps": "Get crowbar → Go to 4 marked sewer locations → Use crowbar on sewer problems → Clean pipes and fix controls → Report back to Palimuth → Gain access to Alchemist Quarter mechanism",
                "location": "Yalahar sewers",
                "required_items": "Crowbar or Whacking Driller of Fate",
                "notes": "Unlocks access to Alchemist Quarter mechanism. Most locations accessible from sewer grate east of depot.",
                "dangers": "Basic sewer creatures"
            },
            {
                "mission_order": 4,
                "name": "Watching the Watchmen",
                "description": "Visit all 7 guards at the gates between quarters to collect their reports. Good mission to explore all quarters of Yalahar safely on main roads.",
                "objective": "Collect reports from all 7 guards stationed at quarter gates", 
                "steps": "Visit guards in order: Foreign-Arena, Arena-Alchemist, Alchemist-Cemetery, Cemetery-Magician, Magician-Sunken, Sunken-Factory, Factory-Trade → Ask each for their report → Return to Palimuth → Gain access to Trade Quarter mechanism",
                "location": "All Yalahar quarters",
                "required_items": "None",
                "notes": "Unlocks access to Trade Quarter mechanism. Stay on main roads for safety.",
                "dangers": "Quarter creatures if straying from main roads"
            },
            {
                "mission_order": 5,
                "name": "Death to the Deathbringer",
                "description": "Choose between Palimuth (good) and Azerus (evil). Kill 3 plague bearers in Alchemist Quarter and decide fate of The Alchemists' Formulas - burn them (good) or give to Azerus (evil).",
                "objective": "Eliminate plague bearers and decide fate of dangerous alchemical research",
                "steps": "Talk to both Palimuth and Azerus → Read their notes → Enter Alchemist Quarter → Kill Diseased Dan, Diseased Bill, Diseased Fred → Get Alchemists' Formulas → Burn in oven (good) OR give to Azerus (evil)",
                "location": "Alchemist Quarter",
                "required_items": "None (protection spell provided)",
                "notes": "First major moral choice. HP of bosses reduced since Summer Update 2012. Shortcut to Diseased Fred added.",
                "dangers": "Diseased Dan, Diseased Bill, Diseased Fred, Death Blobs, Mutated creatures, Acid Blobs, Slimes, Bog Raiders, Mutated Tigers"
            },
            {
                "mission_order": 6,
                "name": "Good to be Kingpin",
                "description": "Deal with Mr. West in Trade Quarter. Good path: sneak through sewers to negotiate peacefully. Evil path: fight through his men and force submission.",
                "objective": "Negotiate with or subdue Mr. West to gain control of Trade Quarter",
                "steps": "Good: Use sewers to reach Mr. West without killing his men → Negotiate peaceful agreement. Evil: Fight through Trade Quarter killing Gang Members, Gladiators, Mad Scientists → Force Mr. West into submission",
                "location": "Trade Quarter and sewers",
                "required_items": "None",
                "notes": "Choice affects relationship with Mr. West and future quarter access.",
                "dangers": "Gang Members, Gladiators, Mad Scientists (if taking evil path), Tarantulas, Slimes, Centipedes (in sewers)"
            },
            {
                "mission_order": 7,
                "name": "Food or Fight",
                "description": "Convince druid Tamerin in Arena Quarter to breed either cattle (good) or warbeasts (evil). Must complete 2 favors: bring Animal Cure from Nibelor and kill Morik the Gladiator.",
                "objective": "Gain Tamerin's assistance by completing favors and choosing breeding focus",
                "steps": "Find Tamerin in Arena Quarter → Get Animal Cure from Siflind in Nibelor (requires Ice Islands Quest access) → Kill Morik the Gladiator for his helmet → Choose cattle (good) or warbeasts (evil)",
                "location": "Arena Quarter, Nibelor",
                "required_items": "Animal Cure from Nibelor, Morik's helmet",
                "notes": "Requires Ice Islands Quest access for Nibelor. Unlocks Arena Quarter mechanism.",
                "dangers": "Arena creatures, gladiators, Morik the Gladiator"
            },
            {
                "mission_order": 8,
                "name": "Frightening Fuel",
                "description": "Use Ghost Charm in Cemetery Quarter to capture souls from Tormented Ghosts. Good path: give charm to Palimuth to free souls. Evil path: give to Azerus for energy source.",
                "objective": "Charge Ghost Charm with tormented souls for different purposes",
                "steps": "Get Ghost Charm from Azerus → Use on Strange Carving in Cemetery Quarter → Kill 3 Tormented Ghosts and use Ghost Residue on charm → Give Charged Ghost Charm to Palimuth (good) or Azerus (evil)",
                "location": "Cemetery Quarter",
                "required_items": "Ghost Charm (provided by Azerus)",
                "notes": "Unlocks Cemetery Quarter mechanism. Choice affects soul fate and trust with factions.",
                "dangers": "Tormented Ghosts, various undead creatures"
            },
            {
                "mission_order": 9,
                "name": "A Fishy Mission", 
                "description": "Deal with Quara threat in Sunken Quarter. Good path: find cause (toxic sewage) and stop it. Evil path: kill Quara leaders Inky, Splasher, and Sharptooth. Requires Helmet of the Deep.",
                "objective": "Resolve Quara conflict through diplomacy or violence",
                "steps": "Get Helmet of the Deep → Enter Sunken Quarter with Tarak → Good: Talk to Maritima to learn about sewage problem → Report to Palimuth. Evil: Kill Quara bosses Inky, Splasher, Sharptooth → Report to Azerus",
                "location": "Sunken Quarter",
                "required_items": "Helmet of the Deep",
                "notes": "Unlocks Sunken Quarter mechanism. Good path addresses root cause, evil path uses force.",
                "dangers": "Quara Constrictors, Mantassins, Hydromancers, Pinchers, Predators, Inky, Splasher, Sharptooth"
            },
            {
                "mission_order": 10,
                "name": "Dangerous Machinations",
                "description": "Retrieve matrix crystal from Factory Quarter. Good path: get Food Matrix Crystal to supply food. Evil path: get Weapon Matrix Crystal to supply weapons. Use on Mysterious Machine.",
                "objective": "Activate factory production for either humanitarian or military purposes",
                "steps": "Enter Factory Quarter → Good: Get Food Matrix Crystal from food production area → Evil: Get Weapon Matrix Crystal from weapon area → Use crystal on Mysterious Machine (both paths) → Face Worker Golems",
                "location": "Factory Quarter",
                "required_items": "None",
                "notes": "Unlocks Factory Quarter mechanism. Can run past golems in full defense if unprepared for combat.",
                "dangers": "Damaged Worker Golems, Worker Golems (slow but tough)"
            },
            {
                "mission_order": 11,
                "name": "Decision", 
                "description": "Final choice between supporting Palimuth (good side) or Azerus (evil side). This decision determines your achievement and final battle approach. Cannot be changed after this point.",
                "objective": "Make final commitment to either good or evil faction",
                "steps": "Talk to Palimuth OR Azerus → Make final commitment to good or evil side → Previous mission choices influence available achievements: Follower of Palimuth, Follower of Azerus, or Turncoat",
                "location": "Yalahar center",
                "required_items": "None",
                "notes": "Final faction choice. Achievement depends on consistency of previous choices.",
                "dangers": "None"
            },
            {
                "mission_order": 12,
                "name": "The Final Battle",
                "description": "Face Azerus in an epic team battle requiring 10+ players level 100+. Battle phases: Rift Worms → Rift Broods → Rift Scythes → War Golems → Azerus becomes vulnerable. 12-minute time limit.",
                "objective": "Defeat Azerus and his interdimensional army in phases",
                "steps": "Gather team of 10+ players level 100+ → Enter inner sanctum → Phase 1: Kill Rift Worms (ignore Azerus) → Phase 2: Kill Rift Broods with Stone Shower → Phase 3: Kill Rift Scythes with Great Fireball → Phase 4: Kill War Golems, now Azerus is vulnerable → Kill Azerus within time limit → Enter Magic Forcefield to complete",
                "location": "Inner sanctum",
                "required_items": "Team coordination, Avalanche, Thunderstorm, Great Fireball, Stone Shower runes",
                "notes": "Requires large team and specific strategies per phase. 12-minute time limit. Rewards Yalaharian Outfit and choice of equipment.",
                "dangers": "Azerus, Rift Worms, Rift Broods, Rift Scythes, War Golems"
            }
        ]

        created_missions = []
        for mission_data in missions_data:
            mission = QuestMission.objects.create(
                quest=quest,
                **mission_data
            )
            created_missions.append(mission)

        # Create rewards
        rewards_data = [
            {
                "name": "5 Platinum Coins",
                "description": "Monetary reward for completing 'The Way to Yalahar' mission",
                "reward_type": "money",
                "value": "5 Platinum Coins"
            },
            {
                "name": "Additional Boat Routes",
                "description": "Unlocked ship routes to and from Yalahar to Ab'Dendriel, Ankrahmun, Carlin, Darashia, Liberty Bay, Port Hope, Thais, and Venore",
                "reward_type": "access",
                "value": "Ship routes to 8 cities"
            },
            {
                "name": "Quarter Access",
                "description": "Progressive access to all Yalahar quarter mechanisms: Alchemist, Trade, Arena, Cemetery, Sunken, and Factory quarters",
                "reward_type": "access",
                "value": "All quarter mechanisms"
            },
            {
                "name": "Yalaharian Outfit",
                "description": "Unique outfit obtained after completing Mission 10: The Final Battle. Base outfit for both male and female characters.",
                "reward_type": "item",
                "value": "Yalaharian Male/Female Outfit"
            },
            {
                "name": "Yalahari Equipment Choice",
                "description": "Choose one item from reward room: Yalahari Armor (Knights), Yalahari Leg Piece (Paladins), Yalahari Mask (Sorcerers/Druids), or Yalahari Footwraps (Monks)",
                "reward_type": "item",
                "value": "Choice of 4 vocation-specific items"
            },
            {
                "name": "Achievement",
                "description": "One of three achievements based on choices: Follower of Azerus (all evil choices), Follower of Palimuth (all good choices), or Turncoat (mixed choices)",
                "reward_type": "other",
                "value": "Achievement based on moral choices"
            }
        ]

        created_rewards = []
        for reward_data in rewards_data:
            reward = QuestReward.objects.create(**reward_data)
            created_rewards.append(reward)

        # Associate rewards with quest
        for reward in created_rewards:
            QuestQuestReward.objects.create(quest=quest, reward=reward)

        # Create dangers
        dangers_data = [
            {
                "creature_name": "Azerus",
                "location": "Inner sanctum",
                "notes": "Extremely powerful boss in final battle, requires team of 10+ players level 100+. Has multiple phases and 12-minute time limit."
            },
            {
                "creature_name": "Rift Creatures",
                "location": "Inner sanctum", 
                "notes": "Rift Worms, Rift Broods, Rift Scythes, and War Golems summoned during final battle. Each requires different strategy."
            },
            {
                "creature_name": "Plague Bearers",
                "location": "Alchemist Quarter",
                "notes": "Diseased Dan, Diseased Bill, and Diseased Fred in Alchemist Quarter. Reduced HP since Summer Update 2012 but still dangerous."
            },
            {
                "creature_name": "Quara Leaders",
                "location": "Sunken Quarter",
                "notes": "Inky, Splasher, and Sharptooth in Sunken Quarter. Powerful aquatic bosses that can deal significant damage."
            },
            {
                "creature_name": "Mutated Creatures",
                "location": "Alchemist Quarter",
                "notes": "Death Blobs, Mutated Humans, Mutated Rats, Acid Blobs, Slimes, Mutated Tigers in Alchemist Quarter"
            },
            {
                "creature_name": "Worker Golems",
                "location": "Factory Quarter",
                "notes": "Damaged Worker Golems and Worker Golems in Factory Quarter. Slow but tough, can be avoided by running in full defense"
            },
            {
                "creature_name": "Criminal Organization",
                "location": "Trade Quarter",
                "notes": "Mad Scientists, Gladiators, Gang Members in Trade Quarter when taking evil path against Mr. West"
            },
            {
                "creature_name": "Arena Creatures",
                "location": "Arena Quarter",
                "notes": "Various beasts and gladiators in Arena Quarter, including Morik the Gladiator who must be defeated"
            },
            {
                "creature_name": "Undead Forces",
                "location": "Cemetery Quarter",
                "notes": "Tormented Ghosts in Cemetery Quarter that must be killed to charge the Ghost Charm"
            },
            {
                "creature_name": "Aquatic Dangers",
                "location": "Sunken Quarter",
                "notes": "Quara Constrictors, Mantassins, Hydromancers, Pinchers, and Predators in Sunken Quarter. Requires Helmet of the Deep."
            },
            {
                "creature_name": "Bog Raiders",
                "location": "Alchemist Quarter",
                "notes": "Up to 6 Bog Raiders and 2 Mutated Tigers must be faced when retrieving Alchemists' Formulas"
            },
            {
                "creature_name": "Sewer Creatures",
                "location": "Yalahar sewers",
                "notes": "Tarantulas, Slimes, and Centipedes in sewers when taking good path to Mr. West"
            }
        ]

        created_dangers = []
        for danger_data in dangers_data:
            danger = QuestDanger.objects.create(
                quest=quest,
                **danger_data
            )
            created_dangers.append(danger)

        print(f"Successfully created In Service of Yalahar Quest!")
        print(f"Created quest: {quest.name}")
        print(f"Created {len(created_missions)} missions")
        print(f"Created {len(created_rewards)} rewards") 
        print(f"Created {len(created_dangers)} dangers")
        
        return quest

if __name__ == "__main__":
    try:
        quest = seed_yalahar_quest()
        print("✅ In Service of Yalahar Quest seeded successfully!")
    except Exception as e:
        print(f"❌ Error seeding quest: {e}")
        raise
