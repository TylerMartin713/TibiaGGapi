#!/usr/bin/env python3

import os
import sys
import django

# Add the project directory to Python path
sys.path.append("/home/tylermartin713/workspace/TibiaGGapi")

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TibiaGGproject.settings")
django.setup()

from TibiaGGapi.models import (
    Quest,
    QuestMission,
    QuestReward,
    QuestQuestReward,
    QuestDanger,
)


def seed_djinn_war_quest():
    # Create the main quest
    quest, created = Quest.objects.get_or_create(
        name="The Djinn War - Efreet Faction",
        defaults={
            "description": "Ally with the mighty Efreets, a powerful race nearly forgotten by the sands of time, to obtain victory in the everlasting djinn wars against their counterparts, the fearsome Marids. There are two warring Djinn factions, the Blue Djinns (Marids) and the Green Djinns (Efreets). As part of their war, they are interested in buying and selling strong equipment for good prices, but they will only deal with people that they trust.",
            "min_level": 40,
            "rec_level": 50,
            "quest_type": "main",
            "difficulty_rating": 3,
            "estimated_duration": "2-3 hours",
            "prerequisites": "Premium account required. Note: There's a short quest that can only be completed before the Djinn War: To Appease the Mighty Quest, which rewards 20 Platinum Coins. If you want to finish this quest, do it before starting the Djinn War.",
            "location": "Mal'ouquah (Green Djinn Fortress)",
            "npc_start": "Melchior (for word of greeting), then Ubaid",
            "is_premium": True,
        },
    )

    if created:
        print(f"Created quest: {quest.name}")
    else:
        print(f"Quest already exists: {quest.name}")
        return

    # Create missions
    missions_data = [
        {
            "name": "Mission 1: The Supply Thief",
            "description": "Find the supply thief who stole from the Efreets",
            "objective": "Find the supply thief in Thais and report back to Baa'leal",
            "mission_order": 1,
            "steps": """1. Talk to Melchior in Ankrahmun and ask about 'word of greeting' - he will tell you 'DJANNI'HAH'
2. Go to the Green Djinn Fortress (Mal'ouquah) - west of the oasis, follow path west to Level 30 Doors of Expertise
3. Talk to Ubaid using 'DJANNI'HAH' (not 'hi') and ask for 'passage'
4. When he tells you to leave, say 'no' and then 'yes' when asked if you want to help fight the Marid
5. Go to Baa'leal and ask for a 'mission' - he will tell you about a supply thief
6. Go to Thais prison (downstairs) and find the prisoner Partos in a cell underground
7. Talk to Partos about 'Ankrahmun' and ask about the 'supplies' - remember his name (Partos)
8. Return to Baa'leal and tell him you completed the 'mission', then tell him the prisoner's name 'Partos'
9. He will give you 600 gp and tell you to speak with Alesar about another mission""",
            "location": "Ankrahmun, Mal'ouquah, Thais",
            "required_items": "None",
            "notes": "Warning: Remember to use 'DJANNI'HAH' or Baa'leal will use soulfire on you dealing 1500 damage over 12.5 minutes. After first mission, you can use 'hi' normally.",
            "dangers": "Soulfire damage if you don't use the greeting word properly",
        },
        {
            "name": "Mission 2: The Tear of Daraman",
            "description": "Steal the Tear of Daraman from the Blue Djinn fortress",
            "objective": "Infiltrate the Blue Djinn fortress and steal the Tear of Daraman gemstone for Alesar",
            "mission_order": 2,
            "steps": """1. Talk to Alesar and ask for a 'mission' - he wants the Tear of Daraman from the Blue Djinns
2. Go to the secret entrance to Blue Djinn fortress - take ramp between Ankrahmun and Darashia
3. Instead of going north to Darashia, follow passage west and take hidden ramp south
4. Face Stone Golems and continue south to secret entrance to Blue Djinn Fortress
5. Go up stairs to 4th floor (one floor above Fire Elementals)
6. Look for two fountains on east side of room - you'll face many Blue Djinns, Marids, Fire Elementals, and Scarabs
7. Warning: On 3rd floor you may face up to 5 Blue Djinns, 1 Marid, 4 Fire Elementals and 2 Scarabs
8. When you find the two fountains, 'use' the one to the north
9. There will be ripples in water and a Tear of Daraman will appear on floor beneath you
10. Return to Alesar and tell him you completed the mission, give him the Tear of Daraman
11. He will tell you to speak with Malor for another mission""",
            "location": "Blue Djinn Fortress (Ashta'daramai)",
            "required_items": "None (you'll obtain the Tear of Daraman)",
            "notes": "Bring Dwarven Rings and good team support. This is very dangerous with many strong creatures.",
            "dangers": "Blue Djinns, Marids, Fire Elementals, Scarabs - up to 5 Blue Djinns and 1 Marid on 3rd floor alone",
        },
        {
            "name": "Mission 3: Orc Fortress",
            "description": "Retrieve Fa'hradin's lamp and place it in Gabel's chambers",
            "objective": "Get the lamp from the Orc King and sneak it into Gabel's personal bedchamber in the Blue Djinn fortress",
            "mission_order": 3,
            "steps": """1. Talk to Malor upstairs and ask for a 'mission' - he wants Fa'hradin's lamp to defeat Gabel
2. Go to Ulderek's Rock (Orc Fortress) and find the Orc King
3. Warning: When you say 'hi' to Orc King, he spawns many different Orcs - be ready with poison bomb
4. Ask him for the 'lamp' and tell him it's for 'Malor' - he will give you Fa'hradin's Gemmed Lamp
5. Return to Blue Djinn fortress secret entrance and go all the way to the top floor
6. You'll face MANY Blue Djinns, Marids, Scarabs and Fire Elementals - bring at least one Dwarven Ring
7. Need a good team: 80+ knight or high level paladin/mage for bedchamber (3 Marids and spawns)
8. Find Gabel's bedchamber and 'use' the gemmed lamp on his counter while carrying Fa'hradin's Gemmed Lamp
9. Return to Malor and tell him you completed the 'mission'
10. You can now trade with Yaman and Alesar, hunt Marids and Blue Djinns, and start blue djinn hunting task""",
            "location": "Ulderek's Rock, Blue Djinn Fortress (Gabel's bedchamber)",
            "required_items": "Fa'hradin's Gemmed Lamp (obtained from Orc King)",
            "notes": "Most dangerous mission. Level 70+ knight can clear to top floor but will struggle with bedchamber. Need strong team for final part.",
            "dangers": "Orc King and many Orcs, Blue Djinns, Marids, Fire Elementals, Scarabs. 3 Marids in bedchamber are especially dangerous.",
        },
    ]

    for mission_data in missions_data:
        mission, created = QuestMission.objects.get_or_create(
            quest=quest, name=mission_data["name"], defaults=mission_data
        )
        if created:
            print(f"Created mission: {mission.name}")

    # Create rewards
    rewards_data = [
        {
            "name": "600 Gold Coins",
            "reward_type": "money",
            "value": "600",
            "description": "Gold coins reward for completing Mission 1",
        },
        {
            "name": "Gemmed Lamp",
            "reward_type": "item",
            "value": "1",
            "description": "A special lamp obtained during the quest",
        },
        {
            "name": "Green Djinn Trading Access",
            "reward_type": "access",
            "value": "Trading",
            "description": "Permission to trade with Yaman and Alesar (Green Djinn merchants)",
        },
        {
            "name": "Blue Djinn Hunting Access",
            "reward_type": "access",
            "value": "Hunting",
            "description": "Ability to hunt Marids and Blue Djinns in Ankrahmun and Yalahar",
        },
        {
            "name": "Blue Djinn Hunting Task",
            "reward_type": "service",
            "value": "Task",
            "description": "Possibility to start a blue djinn hunting task",
        },
    ]

    for i, reward_data in enumerate(rewards_data):
        reward, created = QuestReward.objects.get_or_create(
            name=reward_data["name"],
            defaults={
                "description": reward_data["description"],
                "reward_type": reward_data["reward_type"],
                "value": reward_data["value"],
            },
        )

        if created:
            print(f"Created reward: {reward.name}")

        # Link reward to quest
        quest_reward, created = QuestQuestReward.objects.get_or_create(
            quest=quest,
            reward=reward,
            defaults={
                "reward_order": i + 1,
                "is_final_reward": i
                >= 2,  # Trading access and beyond are final rewards
            },
        )

    # Create dangers
    dangers_data = [
        {
            "creature_name": "Blue Djinns",
            "location": "Blue Djinn Fortress",
            "notes": "Found throughout the fortress, especially dangerous in groups",
        },
        {
            "creature_name": "Marids",
            "location": "Blue Djinn Fortress",
            "notes": "Very powerful, 3 found in Gabel's bedchamber",
        },
        {
            "creature_name": "Fire Elementals",
            "location": "Blue Djinn Fortress",
            "notes": "Found on various floors of the fortress",
        },
        {
            "creature_name": "Scarabs",
            "location": "Blue Djinn Fortress",
            "notes": "Additional creatures found in the fortress",
        },
        {
            "creature_name": "Stone Golems",
            "location": "Secret entrance path",
            "notes": "Found near the secret entrance to Blue Djinn fortress",
        },
        {
            "creature_name": "Orc King",
            "location": "Ulderek's Rock",
            "notes": "Spawns many Orcs when greeted, use poison bomb strategy",
        },
        {
            "creature_name": "Various Orcs",
            "location": "Ulderek's Rock",
            "notes": "Orc Warlords, Leaders, Berserkers, Warriors spawned by Orc King",
        },
    ]

    for danger_data in dangers_data:
        danger, created = QuestDanger.objects.get_or_create(
            quest=quest,
            creature_name=danger_data["creature_name"],
            defaults={
                "location": danger_data["location"],
                "notes": danger_data["notes"],
            },
        )
        if created:
            print(f"Created danger: {danger.creature_name}")

    print(f"\nQuest '{quest.name}' has been seeded successfully!")
    print(f"- {quest.missions.count()} missions")
    print(f"- {quest.quest_rewards.count()} rewards")
    print(f"- {quest.dangers.count()} dangers")


if __name__ == "__main__":
    seed_djinn_war_quest()
