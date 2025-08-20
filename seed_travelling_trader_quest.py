#!/usr/bin/env python3

import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "TibiaGGproject.settings")

# Setup Django
django.setup()

from TibiaGGapi.models import (
    Quest,
    QuestMission,
    QuestReward,
    QuestQuestReward,
    QuestDanger,
)
from django.db import transaction


def create_travelling_trader_quest():
    try:
        with transaction.atomic():
            # Create the main quest
            quest = Quest.objects.create(
                name="The Travelling Trader Quest",
                description="Rashid is searching for experienced traders to buy their goods. You must pass a test to prove yourself a worthy trader, completing one new task each day for a whole week. This quest unlocks the ability to trade with the famous travelling merchant Rashid.",
                min_level=0,
                rec_level=50,
                estimated_duration="7 days (one mission per day)",
                difficulty_rating=2,
                prerequisites="Premium account required. Quest must be started on Monday after server save. Need 1500 gp + travel money.",
            )
            print(f"Created quest: {quest.name}")

            # Create missions (7 days)
            missions_data = [
                {
                    "name": "First Mission - Monday (Deer Trophy)",
                    "objective": "Bring Rashid a Deer Trophy while he is in Svargrond at Dankwart's tavern.",
                    "location": "Svargrond (Dankwart's tavern)",
                    "required_items": "1 Deer Trophy",
                    "steps": "1. Find Rashid in Svargrond at Dankwart's tavern. 2. Say 'hi' then 'mission' to start the quest. 3. Rashid will ask for a Deer Trophy. 4. Hunt Smugglers or other creatures to obtain a Deer Trophy. 5. Return to Rashid with the trophy and say 'mission' then 'yes' to complete.",
                    "notes": "This is the starting mission. You must wait until the next day to proceed.",
                    "dangers": "Smugglers when hunting for Deer Trophy",
                },
                {
                    "name": "Second Mission - Tuesday (Heavy Package)",
                    "objective": "Get a package from Willard on Edron and deliver it to Rashid in Liberty Bay.",
                    "location": "Liberty Bay (Lyonel's tavern), Edron, Outlaw Camp",
                    "required_items": "600 oz of free capacity, travel money",
                    "steps": "1. Find Rashid in Liberty Bay at Lyonel's tavern. 2. Say 'mission' to get the task. 3. Travel to Edron and find Willard. 4. Ask Willard about 'package for rashid'. 5. Willard will direct you to Snake Eye in Outlaw Camp. 6. Travel to Outlaw Camp and find Snake Eye. 7. Ask Snake Eye about 'package for rashid'. 8. Get the Heavy Package from the box. 9. Return to Rashid in Liberty Bay.",
                    "notes": "You need 600 oz of free capacity to carry the Heavy Package.",
                    "dangers": "Smugglers, Wild Warriors, Bandits, possibly lured Minotaurs in Outlaw Camp",
                },
                {
                    "name": "Third Mission - Wednesday (Scarab Cheese)",
                    "objective": "Buy Scarab Cheese from Miraia in Darashia and deliver it to Rashid in Port Hope without using boats.",
                    "location": "Port Hope (Clyde's tavern), Darashia",
                    "required_items": "100 gp for cheese, travel money",
                    "steps": "1. Find Rashid in Port Hope at Clyde's tavern. 2. Say 'mission' to get the task. 3. Travel to Darashia and find Miraia at the Enlightened Oasis. 4. Buy Scarab Cheese for 100 gp. 5. Travel on foot from Ankrahmun to Port Hope (no boats allowed). 6. Deliver the cheese to Rashid before it becomes moldy.",
                    "notes": "Cannot use boats, Temple Teleport Scroll, or parcels. Must travel on foot. Cheese will become moldy if you take too long. Don't buy the cheese before talking to Rashid first.",
                    "dangers": "Nomads and Tiquanda creatures on the path from Ankrahmun to Port Hope",
                },
                {
                    "name": "Fourth Mission - Thursday (Fine Vase)",
                    "objective": "Buy a Fine Vase from Briasol in Ab'Dendriel and deliver it to Rashid in Ankrahmun without touching it.",
                    "location": "Ankrahmun (Arito's tavern), Ab'Dendriel",
                    "required_items": "1000 gp for the vase",
                    "steps": "1. Find Rashid in Ankrahmun at Arito's tavern (above post office). 2. Say 'mission' to get the task. 3. Travel to Ab'Dendriel and find Briasol. 4. Say 'hi' or 'ashari' then ask about 'fine vase'. 5. Buy the vase for 1000 gp. 6. Do NOT move the vase in your backpack or it will break. 7. Return to Rashid in Ankrahmun.",
                    "notes": "The vase is extremely fragile - do not touch it or move it in your backpack or it will break. If it breaks, you can buy another one.",
                    "dangers": "No specific creatures, but be careful not to die as the vase might break",
                },
                {
                    "name": "Fifth Mission - Friday (Crimson Sword Trading)",
                    "objective": "Use trading skills to get a Crimson Sword from Uzgod in Kazordoon for 400 gp or less with good quality.",
                    "location": "Darashia (Miraia's tavern), Kazordoon",
                    "required_items": "3 Iron Ores, 250 gp (for the successful negotiation)",
                    "steps": "1. Find Rashid in Darashia at Miraia's tavern. 2. Say 'mission' to get the task about haggling. 3. Travel to Kazordoon and find Uzgod the weapon dealer. 4. Ask about 'crimson sword' - he'll say he doesn't sell them. 5. Ask him to 'forge' one. 6. Say 'no' when he offers 1000 gp (too expensive). 7. Say 'no' when he offers cheap sword for 300 gp (poor quality). 8. Say 'yes' when he offers good quality for 3 Iron Ores + 250 gp. 9. Return to Rashid with the sword.",
                    "notes": "This is a test of haggling skills. You must negotiate to get good quality for 400 gp or less. If you make a mistake, you can reset by buying any Crimson Sword and offering it to Rashid.",
                    "dangers": "Dwarves and/or Geo-Elementals when mining Iron Ores if you don't have them",
                },
                {
                    "name": "Sixth Mission - Saturday (Goldfish Bowl)",
                    "objective": "Get a Goldfish Bowl with a fish inside and bring it to Rashid in Edron.",
                    "location": "Edron (Mirabell's tavern), Calassa or Sunken Quarter in Yalahar",
                    "required_items": "Empty Goldfish Bowl (buy from furniture shopkeeper)",
                    "steps": "1. Find Rashid in Edron at Mirabell's tavern (above post office and bank). 2. Say 'mission' to get the task. 3. If you don't have one, buy an empty Goldfish Bowl from any furniture shopkeeper. 4. Travel to Calassa or Sunken Quarter in Yalahar. 5. Use the empty bowl on water with fish to catch one. 6. Return to Rashid with the Goldfish Bowl (with fish).",
                    "notes": "You can prepare this before talking to Rashid. You can also buy from another player or ask a friend to get it for you in Yalahar if you don't have access.",
                    "dangers": "Quaras in Calassa or Sunken Quarter when trying to catch fish",
                },
                {
                    "name": "Final Mission - Sunday (Recognition)",
                    "objective": "Receive recognition as a trader from Rashid and unlock trading abilities.",
                    "location": "Carlin depot (one floor above)",
                    "required_items": "None (completion of all previous missions)",
                    "steps": "1. Find Rashid in Carlin depot on the upper floor. 2. Say 'hi' then 'mission'. 3. Rashid will declare you a recognized trader. 4. You can now trade with Rashid anytime and anywhere he appears.",
                    "notes": "This is the final step. You must have completed all previous missions during the week.",
                    "dangers": "None",
                },
            ]

            for i, mission_data in enumerate(missions_data, 1):
                mission = QuestMission.objects.create(
                    quest=quest,
                    name=mission_data["name"],
                    objective=mission_data["objective"],
                    location=mission_data["location"],
                    required_items=mission_data["required_items"],
                    steps=mission_data["steps"],
                    notes=mission_data["notes"],
                    dangers=mission_data["dangers"],
                    mission_order=i,
                )
                print(f"Created mission: {mission.name}")

            # Create quest rewards
            rewards_data = [
                {
                    "name": "Trading Access",
                    "description": "Ability to trade with Rashid, the travelling merchant, at any location",
                    "reward_type": "access",
                    "is_final_reward": True,
                },
                {
                    "name": "Recognised Trader Achievement",
                    "description": "Achievement awarded for completing the quest",
                    "reward_type": "other",
                    "is_final_reward": True,
                },
                {
                    "name": "Just in Time Achievement",
                    "description": "Additional achievement if you previously completed Ice Delivery mission of The Explorer Society Quest",
                    "reward_type": "other",
                    "is_final_reward": True,
                },
            ]

            for reward_data in rewards_data:
                reward = QuestReward.objects.create(
                    name=reward_data["name"],
                    description=reward_data["description"],
                    reward_type=reward_data["reward_type"],
                )

                # Link reward to quest
                QuestQuestReward.objects.create(
                    quest=quest,
                    reward=reward,
                    is_final_reward=reward_data["is_final_reward"],
                )
                print(f"Created reward: {reward.name}")

            # Create quest dangers
            dangers_data = [
                {
                    "creature_name": "Smuggler",
                    "location": "Various locations when hunting for Deer Trophy and in Outlaw Camp",
                    "notes": "Encountered during multiple missions",
                },
                {
                    "creature_name": "Wild Warrior",
                    "location": "Outlaw Camp area",
                    "notes": "Dangerous when retrieving the Heavy Package",
                },
                {
                    "creature_name": "Bandit",
                    "location": "Outlaw Camp area",
                    "notes": "Can be encountered during Tuesday's mission",
                },
                {
                    "creature_name": "Minotaur",
                    "location": "Outlaw Camp (if lured)",
                    "notes": "Potentially dangerous if lured to the area",
                },
                {
                    "creature_name": "Nomad",
                    "location": "Path from Ankrahmun to Port Hope",
                    "notes": "Encountered during Wednesday's cheese delivery mission",
                },
                {
                    "creature_name": "Tiquanda Creatures",
                    "location": "Jungle areas on route to Port Hope",
                    "notes": "Various jungle creatures including Elephants, Earth Elementals, Hyaenas",
                },
                {
                    "creature_name": "Dwarf/Geo-Elemental",
                    "location": "Kazordoon area",
                    "notes": "If you need to mine Iron Ores for Friday's mission",
                },
                {
                    "creature_name": "Quara",
                    "location": "Calassa and Sunken Quarter in Yalahar",
                    "notes": "Dangerous when trying to catch fish for Saturday's mission",
                },
                {
                    "creature_name": "Hydra",
                    "location": "Various locations (if lured)",
                    "notes": "Potentially dangerous if lured during travels",
                },
            ]

            for danger_data in dangers_data:
                danger = QuestDanger.objects.create(
                    quest=quest,
                    creature_name=danger_data["creature_name"],
                    location=danger_data["location"],
                    notes=danger_data["notes"],
                )
                print(f"Created danger: {danger.creature_name}")

            print(f"\nSuccessfully created The Travelling Trader Quest with:")
            print(f"- {len(missions_data)} missions")
            print(f"- {len(rewards_data)} rewards")
            print(f"- {len(dangers_data)} dangers")

    except Exception as e:
        print(f"Error creating quest: {e}")
        return False

    return True


if __name__ == "__main__":
    success = create_travelling_trader_quest()
    if success:
        print(
            "\n✅ The Travelling Trader Quest has been successfully added to the database!"
        )
    else:
        print("\n❌ Failed to create The Travelling Trader Quest.")
