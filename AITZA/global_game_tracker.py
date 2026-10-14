#!/usr/bin/env python3
"""
Global Game: AFK In The Zombie Apocalypse Game — Master Stat Tracker & Character Wiki CLI
Upgraded from zombiecalc.py with:
  1. Zombie Clone & Proliferator Calculator (Lv 1–120+, 6h/12h/18h stages, novel chapter citations)
  2. Zombie Form Modification & Solidification Cost Calculator (Survival Points, Crystals, King of Gods' Points)
  3. Sacred Tree Abe Akaya Dimensional Level & Vampire Clan Boost Calculator
  4. Interactive Character Wiki & Index (150 characters sortable by Mentions, First Name, Last Name, Chapters, Debut)
  5. CSV Export & Interactive Terminal Menu + CLI Flags
"""

import argparse
import csv
import json
import math
import sys

NOVEL_VERIFIED_LEVELS = {
    1: ("Ch. 2", "Starter SSS Enhanced Super Zombie Clone (1 clone)"),
    2: ("Ch. 3", "First level-up (+2 clones = 3 total)"),
    4: ("Ch. 3", "Starter forest clearing (+4 clones = 10 total)"),
    6: ("Ch. 17", "Absorbed Tier 1 evolution crystal (21 total)"),
    7: ("Ch. 32", "Upgraded to Lv 7 (28 total)"),
    9: ("Ch. 32", "Text confirms 45 zombie clones at Lv 9"),
    10: ("Ch. 76 & 113", "Text confirms 55 clones; unlocks SSS Stage 1 Talent: Rapid Growth"),
    11: ("Ch. 113 & 115", "First +20% level-up (+11 clones = 66 base, 264 with proliferators)"),
    12: ("Ch. 115", "Upgraded to Lv 12 (+14 clones = 80 base)"),
    13: ("Ch. 115", "Upgraded to Lv 13 (+16 clones = 96 base)"),
    16: ("Ch. 239", "Reached Lv 16 & low-level Vampire Bloodline (168 base)"),
    17: ("Ch. 247 & 262", "Reached Lv 17; resurrection time = 8.6 hours (202 base)"),
    20: ("Ch. 707", "Reached Lv 20 (351 base / 1,404 with proliferators)"),
    23: ("Ch. 819", "Text confirms +102 gained = 609 base clones"),
    24: ("Ch. 830", "Text confirms +122 gained = 731 base clones"),
    27: ("Ch. 1029", "Text confirms 1,265 base clones"),
    28: ("Ch. 1064", "Text confirms 1,518 base clones"),
    30: ("Ch. 1386 & 1630", "Reached Lv 30; unlocks SSS Stage 2 Talent: Efficient Evolution (2,187 base)"),
    32: ("Ch. 1648", "Text confirms 3,150 base clones"),
    34: ("Ch. 1663", "Text confirms 4,536 base clones"),
    35: ("Ch. 1669", "Text confirms 5,444 base clones"),
    36: ("Ch. 1734", "Text confirms 6,533 base clones"),
    37: ("Ch. 1797", "Text confirms 7,840 base clones"),
    38: ("Ch. 1797", "Text confirms 9,408 base clones"),
    39: ("Ch. 1797", "Text confirms 11,290 base clones (breaks 10,000 mark!)"),
    40: ("Ch. 1813", "Text confirms +2,258 gained = 13,548 base; unlocks Life Diversion & Mutant Infection"),
    41: ("Ch. 2318", "Text confirms +2,710 gained = 16,258 base clones"),
    42: ("Ch. 2329", "Text confirms +3,252 gained = 19,510 base clones"),
    49: ("Ch. 2461", "Reached Lv 49 (69,911 base / 279,644 with proliferators)"),
    50: ("Ch. 2579", "Text confirms +13,983 gained = 83,894 base clones"),
    51: ("Ch. 2622", "Text confirms +16,779 gained = 100,673 base clones"),
    59: ("Ch. 2622", "Text confirms +72,147 gained = 432,881 base clones"),
    60: ("Ch. 3256", "Text confirms +86,577 gained = 519,458 base clones"),
    61: ("Ch. 3258", "Text confirms +103,892 gained = 623,350 base clones"),
    62: ("Ch. 3258", "Text confirms +124,670 gained = 748,020 base clones"),
    63: ("Ch. 3269", "Text confirms +149,604 gained = 897,624 base clones"),
    67: ("Ch. 3305", "Fang Heng holds level at Lv 67 (1,861,314 base / 7,445,256 total)"),
    70: ("Ch. 3305 & 3323", "Spirit/Death Crystal threshold (3,216,352 base / 12,865,408 total)"),
}

ZOMBIE_FORMS = {
    "vine_tyrant_solidify": {
        "name": "Vine Parasite + Tyrant Fusion Solidification (Ch. 177 & 379)",
        "unit_cost": {"Survival Points": 15000, "Tier 1 Evolution Crystals": 3},
        "notes": "Eliminates unstable clone mutation risk and permanently solidifies Tyrant + Vine Parasite form."
    },
    "worm_tyrant_batch": {
        "name": "Mutant Worm + Tyrant + Vine Tri-Fusion (Ch. 445)",
        "unit_cost": {"Survival Points": 2000, "Tier 1 Evolution Crystals": 1},
        "notes": "400,000 Survival Points + 200 Tier 1 Evolution Crystals per 200 clones."
    },
    "worm_late_solidify": {
        "name": "Late-Game Worm Body Solidification (Ch. 3256 & 3258)",
        "unit_cost": {"King of Gods' Points": 500},
        "notes": "Used at Lv 60–62 (e.g., 86,577 * 500 = 43,288,500 King of Gods' Points)."
    },
    "rapid_division": {
        "name": "Rapid Division Transformation (Ch. 2919)",
        "unit_cost": {"King of Gods' Points": 1500},
        "notes": "1,500 King of Gods' Points per zombie clone."
    },
    "undead_conversion": {
        "name": "Undead Form Base Conversion (Ch. 3307 & 3332)",
        "unit_cost": {"King of Gods' Points": 5000},
        "notes": "Unlocks at God-Level Undead Studies; converts zombie clone into pure Undead form."
    },
    "underworld_hunter": {
        "name": "Underworld Hunter Faith Solidification (Ch. 3332)",
        "unit_cost": {"King of Gods' Points": 105000},
        "notes": "5,000 base Undead conversion + 100,000 King of Gods' Points to solidify Underworld Hunter."
    },
    "god_of_underworld": {
        "name": "God of the Underworld Faith Solidification (Ch. 3378)",
        "unit_cost": {"King of Gods' Points": 10005000},
        "notes": "5,000 base Undead conversion + 10,000,000 King of Gods' Points per clone."
    }
}

CHARACTERS_DB = [
  {
    "rank": 1,
    "name": "Fang Heng",
    "first_name": "Heng",
    "last_name": "Fang",
    "aliases": "World Lord of District 8, Vampire King Inheritor, Great Sage Inheritor, Underworld Lord, Fang Bai",
    "tier": "Protagonist",
    "faction": "Prison 507 / Zombie Apocalypse",
    "role": "Protagonist / Sovereign of the Undead & Sacred Trees",
    "arc": "All Arcs (Ch. 1–3555)",
    "abilities": "SSS-Rank Enhanced Super Zombie Clone (Rapid Growth, Efficient Evolution, Life Diversion, Mutant Infection), Undying Body, Omniscient Eye (Alchemy/Occult), Vampire King Bloodline, Soul Symbiote Abe Akaya, Seed of Ouroboros, Super-God Necromancy & Hell Studies, God-Level Occult & Natural Science, Demigod Alchemy/Mysticism/Sealing/Sacred Study",
    "bio": "Transmigrated into the body of a former pro gamer who awakens the SSS-rank Enhanced Super Zombie Clone talent. Starting from Prison No. 507 in District 8, he builds an automated zombie empire that mines, crafts, researches, and fights 24/7. Across the novel, he fuses the Undying Body, steals and binds the Vampire Sacred Tree Angetas and the Vampire King's Coffin, bonds with the dimensional sacred tree Abe Akaya, transplants the Omniscient Eye, masters Super-God Necromancy and Hell Studies, and battles the Holy Court, OmniTech, Demonic Seeds, and the God Clan.",
    "mentions": 66802,
    "chapters": 3529,
    "first_ch": 1,
    "last_ch": 3555,
    "peak_ch": 2311
  },
  {
    "rank": 2,
    "name": "Mo Jiawei",
    "first_name": "Jiawei",
    "last_name": "Mo",
    "aliases": "Brother Wei, Old Mo, Envoy of the Underworld",
    "tier": "Core Deuteragonist / Major Ally",
    "faction": "Prison 507 / Zombie Apocalypse",
    "role": "Core Companion / Tactician & Master Manipulator",
    "arc": "District 8, Enkama Empire, Tower of Bones, World of Forests & Beyond (Ch. 144–3011)",
    "abilities": "Sealing Arts, Necromancy, Psychological Warfare, Disguise & Reconnaissance, Underworld Summoning",
    "bio": "Fang Heng's closest friend, right-hand confidant, and chief schemer. Initially meeting Fang Heng during the Meteorite Company shelter mission in District 8, he quickly recognizes Fang Heng's absurd potential and joins his core crew. Known for his shameless wit, silver tongue, and strategic brilliance, he accompanies Fang Heng across the Enkama Empire, Punoze, and the Necromancer Association.",
    "mentions": 2470,
    "chapters": 589,
    "first_ch": 144,
    "last_ch": 3011,
    "peak_ch": 291
  },
  {
    "rank": 3,
    "name": "Qiu Yaokang",
    "first_name": "Yaokang",
    "last_name": "Qiu",
    "aliases": "Dr. Qiu, Director Qiu, Chief Scientist of Prison 507",
    "tier": "Core Deuteragonist / Major Ally",
    "faction": "Prison 507 / Zombie Apocalypse",
    "role": "Chief Biologist & Virus Mutation Researcher",
    "arc": "District 8, Vampire Apocalypse, Ouroboros & Netherworld Arcs (Ch. 43–3389)",
    "abilities": "T-Virus & G-Virus Mutation Research, Mutation Fusion Talent, Sacred Tree Transplantation, Seed of Ouroboros Analysis, Gene Modification",
    "bio": "A brilliant, fanatical former Meteorite Company researcher rescued and recruited by Fang Heng into Prison No. 507. He leads all biological research in Fang Heng's shelter, engineering the Vine Parasite, Fusion Tyrant, Licker, Mutant Worm, and Ouroboros zombie clone modifications, as well as synthesizing the three S-rank talent plans into Fang Heng's SSS-rank Rapid Growth plan.",
    "mentions": 1222,
    "chapters": 273,
    "first_ch": 43,
    "last_ch": 3389,
    "peak_ch": 85
  },
  {
    "rank": 4,
    "name": "Tang Mingyue",
    "first_name": "Mingyue",
    "last_name": "Tang",
    "aliases": "Her Highness Mingyue, Princess Mingyue, Empress of Enkama",
    "tier": "Core Deuteragonist / Major Ally",
    "faction": "Enkama Empire / Royal Family",
    "role": "Imperial Princess (later Ruler) of the Enkama Empire",
    "arc": "World Lords Summit & Enkama Empire Civil War Arc (Ch. 509–1752)",
    "abilities": "Spatial Science Magic, Imperial Royal Bloodline, Strategic Command, Magic Array Control",
    "bio": "The composed, chestnut-haired princess of the Enkama Empire and representative of District 5. Seeking allies to save her fractured empire from usurpers, barbarians, and the Holy Court's infiltration, she forms a deep alliance with Fang Heng, granting him access to Imperial resources, spatial magic, and the World of Forests.",
    "mentions": 1192,
    "chapters": 216,
    "first_ch": 509,
    "last_ch": 1752,
    "peak_ch": 1008
  },
  {
    "rank": 5,
    "name": "Chen Yu",
    "first_name": "Yu",
    "last_name": "Chen",
    "aliases": "Captain Chen, Commander Chen",
    "tier": "Core Deuteragonist / Major Ally",
    "faction": "Federation",
    "role": "Captain of the 17th Elite Team / Senior Eastern Federation Liaison",
    "arc": "District 8, District 7, Vampire Wars & God Clan Arcs (Ch. 73–3495)",
    "abilities": "Tactical Firearms, Elite Squad Command, Crisis Coordination, Combat Martial Arts",
    "bio": "Originally introduced as the upright captain of the Federation's 17th Elite Team assigned to cooperate with Fang Heng at Prison No. 507. Despite being repeatedly left speechless by Fang Heng's unorthodox methods and massive zombie hordes, he becomes Fang Heng's most trusted ally inside the Federation hierarchy.",
    "mentions": 1188,
    "chapters": 196,
    "first_ch": 73,
    "last_ch": 3495,
    "peak_ch": 488
  },
  {
    "rank": 6,
    "name": "Zane",
    "first_name": "Zane",
    "last_name": "Zane",
    "aliases": "Evil God Apostle Zane",
    "tier": "Core Deuteragonist / Major Ally",
    "faction": "Netherworld / Death Realm / Evil Clan",
    "role": "Late-Game Deuteragonist / Evil God Space Survivor & Guide",
    "arc": "Netherworld, Hell & God Clan Tribunal Arcs (Ch. 3209–3555)",
    "abilities": "Shadow & Evil God Power, Netherworld Navigation, Illusion & Soul Concealment, Underworld Faith Rituals",
    "bio": "A cunning yet perpetually terrified specialist in Evil God and Netherworld powers who becomes bound to Fang Heng's operations in the final third of the novel. He serves as Fang Heng's insider guide through the Death Realm, the Ninety-Nine Layers of Hell, and the God Clan's Tribunal of Sin.",
    "mentions": 1114,
    "chapters": 211,
    "first_ch": 3209,
    "last_ch": 3555,
    "peak_ch": 3395
  },
  {
    "rank": 7,
    "name": "Sandy",
    "first_name": "Sandy",
    "last_name": "Nelen",
    "aliases": "Sandy Nelen, Curator Sandy, Saint of Alchemy Inheritor",
    "tier": "Core Deuteragonist / Major Ally",
    "faction": "Prison 507 / Zombie Apocalypse",
    "role": "Chief Alchemist of Prison 507 / Former Yin City Museum Curator",
    "arc": "Yin City, Enkama Empire, Chiporeya & Alchemy Arcs (Ch. 276–2406)",
    "abilities": "Elementary to God-Level Alchemy, Magic Array Construction, Saint of Alchemy Inheritance, Sculpture & Artifact Appraisal",
    "bio": "Originally an eccentric NPC art gallery curator in Yin City obsessed with the 'Heart of the Apocalypse' sculpture. After Fang Heng recruits him into Prison No. 507, Sandy's obsession shifts to alchemy; backed by Fang Heng's infinite resources and zombie assistants, he awakens the Saint of Alchemy's inheritance and becomes the chief magic array architect of Fang Heng's faction.",
    "mentions": 1027,
    "chapters": 222,
    "first_ch": 276,
    "last_ch": 2406,
    "peak_ch": 1177
  },
  {
    "rank": 8,
    "name": "Adam",
    "first_name": "Adam",
    "last_name": "Adam",
    "aliases": "Divine Artificer Adam",
    "tier": "Core Deuteragonist / Major Ally",
    "faction": "God Clan / Tribunal of Sin",
    "role": "God Clan Divine Magic Array Master",
    "arc": "God Clan Temple & Netherworld Fusion Arc (Ch. 3308–3380)",
    "abilities": "Divine Magic Array Reconstruction, Super-Tier Alchemy, God Clan Mental Strength, Sacred Seal Engineering",
    "bio": "A high-ranking God Clan scholar and master of divine magic arrays stationed inside the sacred temple. His intricate array reconstructions become a major focal point during Fang Heng's infiltration of the God Clan's domain, where Fang Heng uses Super-God Alchemy and the Omniscient Eye to dissect and subvert Adam's work.",
    "mentions": 1015,
    "chapters": 62,
    "first_ch": 3308,
    "last_ch": 3380,
    "peak_ch": 3312
  },
  {
    "rank": 9,
    "name": "Li Shaoqiang",
    "first_name": "Shaoqiang",
    "last_name": "Li",
    "aliases": "Old Li, Brother Qiang",
    "tier": "Core Deuteragonist / Major Ally",
    "faction": "Federation",
    "role": "Veteran Federation Necromancer & Analyst",
    "arc": "Necromancer Association, Zombie Wave, Tower of Bones & Death Realm Arcs (Ch. 526–2619)",
    "abilities": "Advanced Necromancy, Soul Absorption, Battlefield Deduction, Undead Summoning",
    "bio": "A veteran Federation player and close comrade of Tan Shuo within the Necromancer Association. Famous for making elaborate, logical-sounding deductions about Fang Heng that are either wildly off-mark or unintentionally hilarious, he becomes one of Fang Heng's most loyal necromancer lieutenants.",
    "mentions": 816,
    "chapters": 154,
    "first_ch": 526,
    "last_ch": 2619,
    "peak_ch": 648
  },
  {
    "rank": 10,
    "name": "Vannes",
    "first_name": "Vannes",
    "last_name": "Vannes",
    "aliases": "Elder Vannes",
    "tier": "Core Deuteragonist / Major Ally",
    "faction": "Tree Spirit Tribe / World of Forests",
    "role": "Elder of the Tree Spirit Race & Guardian of the Sacred Tree",
    "arc": "World of Forests & OmniTech Conflict Arc (Ch. 2131–2363)",
    "abilities": "Natural Science Magic, Sacred Tree Communion, Life Rituals, Forest Barrier Manipulation",
    "bio": "A devoted and venerable elder of the Tree Spirit Race in the World of Forests. Desperate to save the dying sacred tree and rescue captured tribe members from OmniTech Company, he allies with Fang Heng and witnesses Abe Akaya pass the progenitor sacred tree trial.",
    "mentions": 802,
    "chapters": 92,
    "first_ch": 2131,
    "last_ch": 2363,
    "peak_ch": 2293
  },
  {
    "rank": 11,
    "name": "Ji Xiaobo",
    "first_name": "Xiaobo",
    "last_name": "Ji",
    "aliases": "Young Master Ji, Necromancer Ji",
    "tier": "Core Deuteragonist / Major Ally",
    "faction": "Necromancer Association / Tower of Bones",
    "role": "Tower of Bones Necromancer & Information Conduit",
    "arc": "Tower of Bones, Punoze & Seed of Ouroboros Arcs (Ch. 1363–2802)",
    "abilities": "Necromancy Studies, Bone Magic, Academic Research, Faction Intelligence",
    "bio": "An excitable, talkative young necromancer at the Tower of Bones who initially clashes with the Holy Court's paladins during Viona's visit. He quickly befriends Fang Heng and Mo Jiawei, serving as their enthusiastic guide, logistical helper, and fellow student under Mentor Gu Luo.",
    "mentions": 801,
    "chapters": 162,
    "first_ch": 1363,
    "last_ch": 2802,
    "peak_ch": 1476
  },
  {
    "rank": 12,
    "name": "Lucia",
    "first_name": "Lucia",
    "last_name": "Lucia",
    "aliases": "Vice-Captain Lucia",
    "tier": "Core Deuteragonist / Major Ally",
    "faction": "Dark Knights / Apocalypse Merchants",
    "role": "Leader of the Meteorite Company Logistics Team / Shelter Researcher",
    "arc": "District 8 Meteorite Company & Shelter Expansion Arc (Ch. 144–531)",
    "abilities": "Pharmaceuticals, Anti-Infection Potion Development, Logistics Management, Biological Sampling",
    "bio": "A proud, capable researcher and logistics team leader from the Meteorite Company who initially doubts Fang Heng during the joint expedition into the fallen city. After witnessing his overwhelming zombie army and high honor rank, she joins his shelter research team alongside Victor and Qiu Yaokang.",
    "mentions": 792,
    "chapters": 110,
    "first_ch": 144,
    "last_ch": 531,
    "peak_ch": 161
  },
  {
    "rank": 13,
    "name": "Ed",
    "first_name": "Ed",
    "last_name": "Ed",
    "aliases": "President Ed",
    "tier": "Core Deuteragonist / Major Ally",
    "faction": "Enkama Empire / Royal Family",
    "role": "President of the Imperial Mage & Mercenary Guild",
    "arc": "Enkama Empire & Imperial Capital Arc (Ch. 1103–1486)",
    "abilities": "Elemental Magic, Guild Intelligence Network, Imperial Politics, Defensive Arrays",
    "bio": "A cautious, perpetually stressed guild president in the Enkama Empire who works closely with Princess Tang Mingyue. Though suspicious by nature, he relies heavily on Fang Heng's forces to survive the barbarian incursions, feudal rebellions, and Holy Court schemes.",
    "mentions": 782,
    "chapters": 135,
    "first_ch": 1103,
    "last_ch": 1486,
    "peak_ch": 1167
  },
  {
    "rank": 14,
    "name": "Viona",
    "first_name": "Viona",
    "last_name": "Viona",
    "aliases": "Saintess Viona",
    "tier": "Core Deuteragonist / Major Ally",
    "faction": "Holy Court / Purifiers",
    "role": "Chosen Saintess of the Holy Court",
    "arc": "Tower of Bones, Punoze & Holy Realm Arcs (Ch. 1362–2783)",
    "abilities": "Demigod-Level Holy Light, Sacred Purification, Oracle Communion, Saintess Blessing",
    "bio": "The seemingly stoic Chosen Saintess of the Holy Court escorted by Holy Paladins to the Tower of Bones. Secretly harboring her own agenda to break free from the Holy Court's control, she cooperates with Fang Heng in a staged conflict that allows him to submit her demigod-level soul imprint for his SSS-rank Level 30 talent advancement.",
    "mentions": 736,
    "chapters": 106,
    "first_ch": 1362,
    "last_ch": 2783,
    "peak_ch": 1616
  },
  {
    "rank": 15,
    "name": "Old Black",
    "first_name": "Old Black",
    "last_name": "Black",
    "aliases": "Blackie, Broker Old Black",
    "tier": "Core Deuteragonist / Major Ally",
    "faction": "Dark Knights / Apocalypse Merchants",
    "role": "Underground Information Broker & Black Market Merchant",
    "arc": "District 8, District 1 & Cross-World Trade Arcs (Ch. 48–2808)",
    "abilities": "Cross-Server Intelligence, King of Gods' Points Trading, Black Market Logistics, Stealth & Survival",
    "bio": "A veteran underground broker who first contacts Fang Heng in the survival radio forums of District 8. Initially treating Fang Heng as a promising newcomer, Old Black is repeatedly shocked by Fang Heng's astronomical supply of resources and becomes his go-to middleman for intelligence and rare blueprints.",
    "mentions": 726,
    "chapters": 147,
    "first_ch": 48,
    "last_ch": 2808,
    "peak_ch": 887
  },
  {
    "rank": 16,
    "name": "Gu Qingzhu",
    "first_name": "Qingzhu",
    "last_name": "Gu",
    "aliases": "Target Gu Qingzhu",
    "tier": "Major Recurring Character",
    "faction": "Prison 507 / Zombie Apocalypse",
    "role": "High-Level Demi-Human Combatant & Protector of Xia Xi",
    "arc": "Real World Crisis, City of Darkness & Late-Game Arcs (Ch. 1824–3502)",
    "abilities": "High-Tier Demi-Human Mutation, Extreme Close-Quarters Combat, Enhanced Regeneration & Reflexes",
    "bio": "A 26-year-old elite demi-human warrior with a massive mutation reaction who emerges during the real-world and parallel-world convergence crisis. Fiercely protective and lethal in combat, she becomes a vital guardian and recurring combat ally for Fang Heng's inner circle.",
    "mentions": 667,
    "chapters": 120,
    "first_ch": 1824,
    "last_ch": 3502,
    "peak_ch": 1875
  },
  {
    "rank": 17,
    "name": "Charlene",
    "first_name": "Charlene",
    "last_name": "Charlene",
    "aliases": "Commander Charlene",
    "tier": "Major Recurring Character",
    "faction": "Black Castle / Demon Hunters",
    "role": "Senior Leader of Black Castle",
    "arc": "Black Castle, Demi-Human & Ouroboros Arcs (Ch. 1714–2967)",
    "abilities": "Spirit Transmission, Demon Hunting Arts, Commander-Tier Combat, Shadow & Blood Suppression",
    "bio": "A calm, authoritative leader within the Black Castle faction who collaborates with Fang Heng against mutated creatures and rival organizations. Together with Fang Heng, she hunts high-tier commander creatures and navigates the shadowy politics between Black Castle and the Federation.",
    "mentions": 599,
    "chapters": 74,
    "first_ch": 1714,
    "last_ch": 2967,
    "peak_ch": 1774
  },
  {
    "rank": 18,
    "name": "Li Qingran",
    "first_name": "Qingran",
    "last_name": "Li",
    "aliases": "Junior Sister Li, Commander Li",
    "tier": "Major Recurring Character",
    "faction": "Necromancer Association / Tower of Bones",
    "role": "Disciple of Teacher Pu Shi & Leader of the Necromancer Player Coalition",
    "arc": "Necromancer Association, Punoze & Miyisca Fortress Arcs (Ch. 717–3456)",
    "abilities": "Master/Grandmaster Necromancy, Formation Command, Spirit Binding, Logistics Coordination",
    "bio": "The dedicated, level-headed star disciple of Teacher Pu Shi in the Necromancer Association. After Pu Shi entrusts the necro-faction's legacy to Fang Heng, Li Qingran becomes a core coordinator of Fang Heng's necromancer player army across multiple worlds.",
    "mentions": 588,
    "chapters": 109,
    "first_ch": 717,
    "last_ch": 3456,
    "peak_ch": 1609
  },
  {
    "rank": 19,
    "name": "Lu Yanlong",
    "first_name": "Yanlong",
    "last_name": "Lu",
    "aliases": "Commander Lu",
    "tier": "Major Recurring Character",
    "faction": "Federation",
    "role": "Outpost Commander & Veteran Frontier Officer",
    "arc": "Frontier Outpost & Dimensional Rift Arc (Ch. 1640–2365)",
    "abilities": "Heavy Weaponry, Outpost Fortification, Mutated Creature Countermeasures, Military Command",
    "bio": "A solemn, battle-hardened frontier commander introduced to Fang Heng by Hector. Tasked with defending poorly supplied outposts against mixed-type mutated creatures, he forms a steadfast military partnership with Fang Heng.",
    "mentions": 584,
    "chapters": 92,
    "first_ch": 1640,
    "last_ch": 2365,
    "peak_ch": 1645
  },
  {
    "rank": 20,
    "name": "Chu Yan",
    "first_name": "Yan",
    "last_name": "Chu",
    "aliases": "Sniper Chu Yan",
    "tier": "Major Recurring Character",
    "faction": "Federation",
    "role": "Ace Sniper & Elite Federation Operatives Leader",
    "arc": "District 7, Holy Court Invasion & Cross-Realm Arcs (Ch. 679–2079)",
    "abilities": "Master Marksmanship, Long-Range Reconnaissance, Armor-Piercing Sniping, Tactical Evasion",
    "bio": "An elite sniper who first crosses paths with Fang Heng during the District 7 conflict when Fang Heng effortlessly dodges his ambush in bat form. Impressed and humbled, Chu Yan later fights alongside Fang Heng's forces during major cross-world campaigns.",
    "mentions": 573,
    "chapters": 92,
    "first_ch": 679,
    "last_ch": 2079,
    "peak_ch": 709
  },
  {
    "rank": 21,
    "name": "Tan Shuo",
    "first_name": "Shuo",
    "last_name": "Tan",
    "aliases": "Brother Tan",
    "tier": "Major Recurring Character",
    "faction": "Federation",
    "role": "Senior Federation Necromancer & Squad Leader",
    "arc": "Necromancer Association, Tower of Bones & Death Realm Arcs (Ch. 521–2625)",
    "abilities": "Necromancy, Undead Hordes Control, Soul Sealing, Squad Leadership",
    "bio": "A pragmatic senior Federation player stationed at the Hall of the Dead who partners closely with Li Shaoqiang. From the moment Fang Heng arrives at the Necromancer Association after conquering District 8, Tan Shuo serves as a reliable bridge between Fang Heng and the necromancer player base.",
    "mentions": 563,
    "chapters": 133,
    "first_ch": 521,
    "last_ch": 2625,
    "peak_ch": 524
  },
  {
    "rank": 22,
    "name": "Victor",
    "first_name": "Victor",
    "last_name": "Victor",
    "aliases": "Engineer Victor",
    "tier": "Major Recurring Character",
    "faction": "Prison 507 / Zombie Apocalypse",
    "role": "Chief Mechanical Engineer of Prison 507 / Former Meteorite Company Engineer",
    "arc": "District 8 Shelter & Mechanical Engineering Arcs (Ch. 157–2460)",
    "abilities": "Advanced Mechanical Maintenance (Lv 50+), Space Tearing Device Engineering, Heavy Turrets & Vehicle Modification",
    "bio": "A former mechanical engineer of the Meteorite Company rescued by Fang Heng alongside his daughter. Grateful for Fang Heng's protection, Victor becomes the chief mechanical engineer of Prison No. 507, teaching Fang Heng high-level maintenance and building space-tearing devices and war machinery.",
    "mentions": 561,
    "chapters": 141,
    "first_ch": 157,
    "last_ch": 2460,
    "peak_ch": 181
  },
  {
    "rank": 23,
    "name": "Wei Tao",
    "first_name": "Tao",
    "last_name": "Wei",
    "aliases": "World Lord Wei Tao, Chief Commander Wei",
    "tier": "Major Recurring Character",
    "faction": "Federation",
    "role": "World Lord of District 1 & Chief Commander of Zombie Apocalypse (Eastern Federation)",
    "arc": "World Lords Summit, District 1 & Enkama Empire Arcs (Ch. 507–1384)",
    "abilities": "World Lord Authority, Strategic Command, High-Tier Combat Talent, Federation Military Mobilization",
    "bio": "The overburdened World Lord of District 1 and Chief Commander of the Zombie Apocalypse department for the Eastern Federation. Constantly dealing with crises caused by the Vampires, Night Owl, and Jian Muzhi's betrayal, he views Fang Heng as both his biggest headache and his greatest trump card.",
    "mentions": 548,
    "chapters": 121,
    "first_ch": 507,
    "last_ch": 1384,
    "peak_ch": 1191
  },
  {
    "rank": 24,
    "name": "Senzo",
    "first_name": "Senzo",
    "last_name": "Senzo",
    "aliases": "Elder Senzo",
    "tier": "Major Recurring Character",
    "faction": "Tree Spirit Tribe / World of Forests",
    "role": "Senior Elder of the Tree Spirit Council",
    "arc": "World of Forests & OmniTech War Arc (Ch. 2138–2362)",
    "abilities": "Ancient Tree Spirit Magic, Tribal Council Authority, Nature Warding, Niam Alloy Intelligence",
    "bio": "A senior elder of the Tree Spirit race who coordinates the multi-tribe resistance against OmniTech Company's central research institute. He works closely with Elder Vannes and Fang Heng to infiltrate OmniTech and safeguard the Sacred Tree's heritage.",
    "mentions": 527,
    "chapters": 78,
    "first_ch": 2138,
    "last_ch": 2362,
    "peak_ch": 2353
  },
  {
    "rank": 25,
    "name": "Jian Muzhi",
    "first_name": "Muzhi",
    "last_name": "Jian",
    "aliases": "Former World Lord Jian Muzhi",
    "tier": "Major Recurring Character",
    "faction": "Federation",
    "role": "Rogue Former World Lord of District 1 / Land of Origin Usurper",
    "arc": "District 1 Land of Origin Arc (Ch. 890–1002)",
    "abilities": "Land of Origin Fusion, Spatial & Origin Manipulation, Ancient Sealing Arrays",
    "bio": "A former World Lord of District 1 who spent decades plotting in secret behind the Elders Council to fuse with the Land of Origin and seize ultimate power, serving as the primary antagonist of the District 1 Origin climax.",
    "mentions": 481,
    "chapters": 61,
    "first_ch": 890,
    "last_ch": 1002,
    "peak_ch": 996
  },
  {
    "rank": 26,
    "name": "Maica",
    "first_name": "Maica",
    "last_name": "Maica",
    "aliases": "Marquis Maica",
    "tier": "Major Recurring Character",
    "faction": "Vampire Clan",
    "role": "Youngest of the Three Vampire Marquises / Loyalist of Fang Heng",
    "arc": "Vampire World, Vampire King's Coffin & Late-Game Vampire Arcs (Ch. 875–3076)",
    "abilities": "Marquis/Duke-Tier Hemomancy, Blood Flight, Crimson Barrier, Vampire Clan Administration",
    "bio": "Initially the suspicious youngest Marquis of the Vampire Clan guarding the sealed remains of the Vampire King. After Fang Heng claims the Vampire King's Coffin and proves his dominance, Maica becomes a core vampire subordinate managing Fang Heng's bloodline forces.",
    "mentions": 474,
    "chapters": 59,
    "first_ch": 875,
    "last_ch": 3076,
    "peak_ch": 979
  },
  {
    "rank": 27,
    "name": "Carl",
    "first_name": "Carl",
    "last_name": "Carl",
    "aliases": "Prince Carl",
    "tier": "Major Recurring Character",
    "faction": "Vampire Clan",
    "role": "Hibernating Prince of the Vampires / Senior Vampire Commander",
    "arc": "Vampire Awakening, World of Forests & God Clan Arcs (Ch. 787–3519)",
    "abilities": "Vampire Prince Bloodline, Scarlet Domain, Ancient Blood Spears, High-Speed Regeneration",
    "bio": "An ancient Vampire Prince originally found bound in a coffin by twenty-four golden chains of the Holy Court. Freed and recruited under Fang Heng's banner as the Vampire King's successor, Carl serves as one of Fang Heng's strongest undead/vampire vanguard generals right up to the final battles.",
    "mentions": 446,
    "chapters": 129,
    "first_ch": 787,
    "last_ch": 3519,
    "peak_ch": 791
  },
  {
    "rank": 28,
    "name": "Gu Luo",
    "first_name": "Luo",
    "last_name": "Gu",
    "aliases": "Teacher Gu Luo, Mentor Gu Luo",
    "tier": "Major Recurring Character",
    "faction": "Necromancer Association / Tower of Bones",
    "role": "Grandmaster Necromancy Mentor at the Tower of Bones",
    "arc": "Tower of Bones & Talent Advancement Arcs (Ch. 1391–2798)",
    "abilities": "Grandmaster/Demigod Necromancy, Soul Appraisal, Talent Advancement Guidance, Bone Tower Authority",
    "bio": "A revered, hunched elder on the upper floors of the Tower of Bones who serves as Fang Heng's talent advancement and Grandmaster Necromancy mentor. Continually astonished by Fang Heng's 5,600% SSS-rank mission completions, he grants Fang Heng the Level 30 and Level 40 dual SSS talent enhancements.",
    "mentions": 446,
    "chapters": 75,
    "first_ch": 1391,
    "last_ch": 2798,
    "peak_ch": 1628
  },
  {
    "rank": 29,
    "name": "Dani",
    "first_name": "Dani",
    "last_name": "Dani",
    "aliases": "Lord Dani, Feudal Lord Dani",
    "tier": "Major Recurring Character",
    "faction": "Punoze / Revolution Society",
    "role": "Feudal Lord of Punoze",
    "arc": "Punoze Feudal Conflict & Sacred Tree Arc (Ch. 1455–2702)",
    "abilities": "Shadow Manipulation, Feudal Domain Authority, Political Assassination Networks",
    "bio": "A calculating female feudal lord in Punoze who initially issues secret bounties against Fang Heng before being drawn into the deeper struggle over the Sacred Tree and Holy Court interference.",
    "mentions": 428,
    "chapters": 82,
    "first_ch": 1455,
    "last_ch": 2702,
    "peak_ch": 1621
  },
  {
    "rank": 30,
    "name": "Kotal",
    "first_name": "Kotal",
    "last_name": "Kotal",
    "aliases": "Leader Kotal",
    "tier": "Major Recurring Character",
    "faction": "Netherworld / Death Realm / Evil Clan",
    "role": "Dark Clan Commander in the Death Realm",
    "arc": "Death Realm & Netherworld Exploration Arcs (Ch. 2585–3306)",
    "abilities": "Dark Clan Combat Arts, Death Realm Survival, Underworld Temple Lore",
    "bio": "A proud warrior leader of the Dark Clan stationed in the Death Realm. Initially wary of Fang Heng as an outsider human, Kotal becomes a key local ally as Fang Heng expands the Death Realm passages and confronts the Netherworld's ancient perils.",
    "mentions": 413,
    "chapters": 69,
    "first_ch": 2585,
    "last_ch": 3306,
    "peak_ch": 2803
  },
  {
    "rank": 31,
    "name": "Pu Shi",
    "first_name": "Shi",
    "last_name": "Pu",
    "aliases": "Teacher Pu Shi",
    "tier": "Major Recurring Character",
    "faction": "Necromancer Association / Tower of Bones",
    "role": "Venerable Necromancy Mentor & Guardian of the Hall of the Dead",
    "arc": "Necromancer Association Defense Arc (Ch. 649–1609)",
    "abilities": "Master Necromancy, Soul Guiding, Undead Formation Defense",
    "bio": "Li Qingran's self-sacrificing teacher and a pillar of the Necromancer Association in the lower realm. Exhausted from defending the necromancers against the Holy Court's relentless purges, he recognizes Fang Heng as the savior of their lineage.",
    "mentions": 408,
    "chapters": 56,
    "first_ch": 649,
    "last_ch": 1609,
    "peak_ch": 718
  },
  {
    "rank": 32,
    "name": "Wangnet",
    "first_name": "Wangnet",
    "last_name": "Wangnet",
    "aliases": "Chieftain Wangnet",
    "tier": "Major Recurring Character",
    "faction": "Enkama Empire / Royal Family",
    "role": "Successor of the Barbarian Leader",
    "arc": "Enkama Empire & Land of Plague Arc (Ch. 1114–1411)",
    "abilities": "Barbarian Totem Strength, Berserker Combat, Tribe Mobilization",
    "bio": "A cautious yet formidable successor to the barbarian leadership bordering the Enkama Empire who contends with Fang Heng and the Land of Plague crisis.",
    "mentions": 402,
    "chapters": 67,
    "first_ch": 1114,
    "last_ch": 1411,
    "peak_ch": 1138
  },
  {
    "rank": 33,
    "name": "Dickey",
    "first_name": "Dickey",
    "last_name": "Dickey",
    "aliases": "Master Dickey, Dickie",
    "tier": "Major Recurring Character",
    "faction": "Necromancer Association / Tower of Bones",
    "role": "Senior Necromancer & Soul Scholar",
    "arc": "Necromancer Association & Death Realm Arcs (Ch. 517–2626)",
    "abilities": "Necromancy Lore, Sacred Tree Soul Analysis, Undead Rituals",
    "bio": "A warm, scholarly senior member of the Necromancer Association introduced to Fang Heng by Mo Yunxiao. He provides critical insights into the Vampire Sacred Tree Angetas and the mechanics of soul rebirth.",
    "mentions": 393,
    "chapters": 82,
    "first_ch": 517,
    "last_ch": 2626,
    "peak_ch": 529
  },
  {
    "rank": 34,
    "name": "Collete",
    "first_name": "Collete",
    "last_name": "Collete",
    "aliases": "Colette, Leader Collete",
    "tier": "Major Recurring Character",
    "faction": "Netherworld / Death Realm / Evil Clan",
    "role": "Hanu Clan Leader & Mutant Cocoon Researcher",
    "arc": "Death Realm & Western Federation Cocoon Arc (Ch. 2571–2958)",
    "abilities": "Hanu Clan Imprints, Gray Aura Manipulation, Biological Cocoon Research",
    "bio": "Leader of the Hanu Clan (also spelled Colette in some chapters) who participates in the Death Realm expeditions and later oversees mutant worm cocoon research alongside Vionne, Jayne, and Emery.",
    "mentions": 381,
    "chapters": 43,
    "first_ch": 2571,
    "last_ch": 2958,
    "peak_ch": 2903
  },
  {
    "rank": 35,
    "name": "Ji Haiting",
    "first_name": "Haiting",
    "last_name": "Ji",
    "aliases": "Director Ji Haiting",
    "tier": "Major Recurring Character",
    "faction": "OmniTech Company",
    "role": "Executive Director of OmniTech Company",
    "arc": "World of Forests & OmniTech Arc (Ch. 2116–2367)",
    "abilities": "Corporate Military Command, Bio-Mechanical Guards, Dimensional Tech Research",
    "bio": "The ambitious executive director of OmniTech Company in the World of Forests. He repeatedly alternates between clashing with Fang Heng over the Tree Whisperers Alliance and attempting to recruit Fang Heng into OmniTech's dimensional energy projects.",
    "mentions": 371,
    "chapters": 66,
    "first_ch": 2116,
    "last_ch": 2367,
    "peak_ch": 2168
  },
  {
    "rank": 36,
    "name": "Xia Xi",
    "first_name": "Xi",
    "last_name": "Xia",
    "aliases": "Miss Xia Xi",
    "tier": "Major Recurring Character",
    "faction": "Prison 507 / Zombie Apocalypse",
    "role": "Fang Heng's Childhood Friend & Early Real-World Benefactor",
    "arc": "Prologue, Real World & Demi-Human Convergence Arcs (Ch. 1–3457)",
    "abilities": "Support & Administration, Real-World Coordination",
    "bio": "The kind-hearted girl from the very first chapter who helped the original Fang Heng stay out of prison and submitted his resume to Phoenix Sound Gaming Company. Fang Heng consistently protects her in the real world, eventually assigning Gu Qingzhu and his elite forces to ensure her safety.",
    "mentions": 366,
    "chapters": 91,
    "first_ch": 1,
    "last_ch": 3457,
    "peak_ch": 1826
  },
  {
    "rank": 37,
    "name": "Fana",
    "first_name": "Fana",
    "last_name": "Fana",
    "aliases": "Researcher Fana",
    "tier": "Major Recurring Character",
    "faction": "Necromancer Association / Tower of Bones",
    "role": "Senior Botanical & Necromantic Researcher",
    "arc": "Tower of Bones & Demi-Human Research Arcs (Ch. 1388–2925)",
    "abilities": "Night Violet Refinement, Botanical Alchemy, Mutation Monitoring",
    "bio": "A dedicated researcher who first meets Fang Heng when he submits bulk quantities of Night Violets at the Tower of Bones. She later assists in monitoring Gu Qingzhu's demi-human mutation and supporting Fang Heng's research logistics.",
    "mentions": 365,
    "chapters": 75,
    "first_ch": 1388,
    "last_ch": 2925,
    "peak_ch": 1678
  },
  {
    "rank": 38,
    "name": "Liao Bufan",
    "first_name": "Bufan",
    "last_name": "Liao",
    "aliases": "Student Liao",
    "tier": "Major Recurring Character",
    "faction": "Prison 507 / Zombie Apocalypse",
    "role": "University Student Survivor & Early Shelter Ally",
    "arc": "Early District 8 Survival & Shelter Arc (Ch. 4–1005)",
    "abilities": "Scavenging, Basic Combat, Shelter Outpost Management",
    "bio": "A talkative university student who meets Fang Heng in Chapter 4 alongside Jimmy and Liu Lin. One of the earliest players to witness Fang Heng's rise from a starter cabin to the ruler of District 8.",
    "mentions": 365,
    "chapters": 72,
    "first_ch": 4,
    "last_ch": 1005,
    "peak_ch": 26
  },
  {
    "rank": 39,
    "name": "Aktu",
    "first_name": "Aktu",
    "last_name": "Aktu",
    "aliases": "Boss Aktu",
    "tier": "Major Recurring Character",
    "faction": "Black Castle / Demon Hunters",
    "role": "Squad Leader of the Mundt Gang in the City of Darkness",
    "arc": "City of Darkness & Mundt Gang Arc (Ch. 1836–1873)",
    "abilities": "Street Warfare, Ambush Tactics, Gang Command",
    "bio": "A key combat leader of the Mundt Gang during the City of Darkness conflict who encounters Fang Heng during the clash between underground gangs and federal teams.",
    "mentions": 362,
    "chapters": 37,
    "first_ch": 1836,
    "last_ch": 1873,
    "peak_ch": 1855
  },
  {
    "rank": 40,
    "name": "Zaka",
    "first_name": "Zaka",
    "last_name": "Zaka",
    "aliases": "Mercenary Zaka",
    "tier": "Major Recurring Character",
    "faction": "Federation",
    "role": "Western District Mercenary Leader & Zate's Brother",
    "arc": "Western District Federation Train & Recruitment Arc (Ch. 2809–2984)",
    "abilities": "Heavy Melee Combat, Mercenary Squad Leadership, Escort Operations",
    "bio": "A seasoned mercenary traveling with his brother Zate on the Western District Federation train who teams up with Fang Heng and Su Guantong during the Black Fog and recruitment center incidents.",
    "mentions": 353,
    "chapters": 73,
    "first_ch": 2809,
    "last_ch": 2984,
    "peak_ch": 2825
  },
  {
    "rank": 41,
    "name": "Bai Mu",
    "first_name": "Mu",
    "last_name": "Bai",
    "aliases": "Mr. Bai Mu",
    "tier": "Major Recurring Character",
    "faction": "Noel Clan / Occult Research",
    "role": "Mastermind of the Underground Information Website & Shadow Alliance Partner",
    "arc": "Underground Network & Shadow Alliance Arcs (Ch. 2403–3016)",
    "abilities": "Information Manipulation, Occult Intelligence, Strategic Planning",
    "bio": "A refined, coffee-loving strategist who operates the mysterious underground intelligence website from behind the scenes and introduces Fang Heng to Wu Yan and the Shadow Alliance.",
    "mentions": 342,
    "chapters": 61,
    "first_ch": 2403,
    "last_ch": 3016,
    "peak_ch": 2404
  },
  {
    "rank": 42,
    "name": "Cleriway",
    "first_name": "Cleriway",
    "last_name": "Cleriway",
    "aliases": "Apprentice Cleriway",
    "tier": "Major Recurring Character",
    "faction": "Noel Clan / Occult Research",
    "role": "Apprentice of Master Oriana & Natural/Alchemy Scholar",
    "arc": "Natural Science & Cross-Realm Research Arcs (Ch. 1583–3262)",
    "abilities": "Natural Science Magic, Herbalism & Alchemy, Magic Array Assistance",
    "bio": "The sharp-eyed, hat-wearing apprentice of Master Oriana. Initially cautious of Fang Heng's scrutiny, she collaborates with him across multiple research and natural science advancement missions.",
    "mentions": 335,
    "chapters": 76,
    "first_ch": 1583,
    "last_ch": 3262,
    "peak_ch": 1583
  },
  {
    "rank": 43,
    "name": "Tippy",
    "first_name": "Tippy",
    "last_name": "Tippy",
    "aliases": "Saintess Tippy",
    "tier": "Major Recurring Character",
    "faction": "Tree Spirit Tribe / World of Forests",
    "role": "Leader of the Soul Tribe (Tree Spirit Race)",
    "arc": "World of Forests & Sacred Tree Trial Arc (Ch. 2249–2402)",
    "abilities": "Soul Tribe Magic, Spiritual Sensing, Sacred Tree Rituals",
    "bio": "A prominent figure of the Soul Tribe within the Tree Spirit Alliance who confronts Vannes over the Sacred Tree crisis and later participates in the dimensional defense of the forest realm.",
    "mentions": 329,
    "chapters": 40,
    "first_ch": 2249,
    "last_ch": 2402,
    "peak_ch": 2348
  },
  {
    "rank": 44,
    "name": "Bellamy",
    "first_name": "Bellamy",
    "last_name": "Bellamy",
    "aliases": "Duchess Bellamy, Duke Bellamy",
    "tier": "Major Recurring Character",
    "faction": "Vampire Clan",
    "role": "Vampire Duchess & Chief Bloodline Researcher",
    "arc": "District 7, Vampire World & World of Forests Arcs (Ch. 588–2400)",
    "abilities": "Duke-Tier Hemomancy, Biological & Tissue Research, Blood Seals",
    "bio": "A scholarly Vampire Duchess fascinated by Hila's tissue samples and the Sacred Tree Angetas. After Fang Heng claims the Vampire King's inheritance, Duchess Bellamy pledges loyalty to him, slaying Holy Court archbishops and leading vampire research under his command.",
    "mentions": 318,
    "chapters": 70,
    "first_ch": 588,
    "last_ch": 2400,
    "peak_ch": 851
  },
  {
    "rank": 45,
    "name": "Ruan Ziying",
    "first_name": "Ziying",
    "last_name": "Ruan",
    "aliases": "Operative Ruan Ziying",
    "tier": "Major Recurring Character",
    "faction": "Punoze / Revolution Society",
    "role": "Core Operative of the Revolution Society",
    "arc": "Punoze & Revolution Society Arc (Ch. 1490–2540)",
    "abilities": "Urban Infiltration, Intelligence Relay, Natural Science Support",
    "bio": "A calm, capable female operative in Punoze who introduces Fang Heng to the local resistance network and accompanies him to Cole's safehouse.",
    "mentions": 316,
    "chapters": 46,
    "first_ch": 1490,
    "last_ch": 2540,
    "peak_ch": 1546
  },
  {
    "rank": 46,
    "name": "Nasir",
    "first_name": "Nasir",
    "last_name": "Nasir",
    "aliases": "Instructor Nasir, Master Nasir",
    "tier": "Major Recurring Character",
    "faction": "Noel Clan / Occult Research",
    "role": "Transcendent Alchemy Instructor",
    "arc": "Noel Clan & Demigod Alchemy Arc (Ch. 3081–3190)",
    "abilities": "Transcendent/Demigod Alchemy, Ancient Magic Arrays, Occult Synthesis",
    "bio": "A reclusive master alchemist associated with the Noel Clan whose teachings and array blueprints play a central role in Fang Heng's leap from Grandmaster to Demigod-level Alchemy.",
    "mentions": 315,
    "chapters": 36,
    "first_ch": 3081,
    "last_ch": 3190,
    "peak_ch": 3082
  },
  {
    "rank": 47,
    "name": "Wu Yi",
    "first_name": "Yi",
    "last_name": "Wu",
    "aliases": "Envoy Wu Yi",
    "tier": "Major Recurring Character",
    "faction": "Netherworld / Death Realm / Evil Clan",
    "role": "Evil Clan Liaison & Vanguard Scout",
    "arc": "Mechanical Legion & Evil Clan Arc (Ch. 3158–3455)",
    "abilities": "Evil Clan Secret Arts, Stealth Reconnaissance, Battlefield Reporting",
    "bio": "A female operative dispatched by the Elders of the Evil Clan to establish contact with Fang Heng during the advance of the mechanical legion.",
    "mentions": 311,
    "chapters": 50,
    "first_ch": 3158,
    "last_ch": 3455,
    "peak_ch": 3165
  },
  {
    "rank": 48,
    "name": "Ovi",
    "first_name": "Ovi",
    "last_name": "Ovi",
    "aliases": "Ovi of the Leaf Tribe",
    "tier": "Major Recurring Character",
    "faction": "Tree Spirit Tribe / World of Forests",
    "role": "Young Elite of the Leaf Tribe",
    "arc": "World of Forests & Temple of Incantation Arc (Ch. 2244–2309)",
    "abilities": "Leaf Tribe Nature Arts, Dimensional Passage Guiding, Temple Guarding",
    "bio": "A young Leaf Tribe member assigned by Patriarch Rudyard to guide Fang Heng into the Temple of Incantation and dimensional world, who ends up witnessing Fang Heng and Abe Akaya siphon the temple's dimensional energy.",
    "mentions": 302,
    "chapters": 31,
    "first_ch": 2244,
    "last_ch": 2309,
    "peak_ch": 2254
  },
  {
    "rank": 49,
    "name": "Nate",
    "first_name": "Nate",
    "last_name": "Nate",
    "aliases": "Duke Nate",
    "tier": "Major Recurring Character",
    "faction": "Vampire Clan",
    "role": "Vampire Duke & Guardian of the Underground Sacred Tree Cave",
    "arc": "District 7 & Vampire Headquarters Arc (Ch. 582–979)",
    "abilities": "Duke-Tier Blood Magic, Blood Pool Control, Bat Swarm Transformation",
    "bio": "A stern Vampire Duke originally in charge of defending the Sacred Tree Angetas against intruders, who is repeatedly outmaneuvered when Fang Heng infiltrates the blood pool and steals the Sacred Tree.",
    "mentions": 294,
    "chapters": 47,
    "first_ch": 582,
    "last_ch": 979,
    "peak_ch": 839
  },
  {
    "rank": 50,
    "name": "Chen Lin",
    "first_name": "Lin",
    "last_name": "Chen",
    "aliases": "Hunter Chen Lin",
    "tier": "Major Recurring Character",
    "faction": "Black Castle / Demon Hunters",
    "role": "Elite Demon Hunter Commander",
    "arc": "Demon Hunters & Vampire Inheritance Arc (Ch. 735–943)",
    "abilities": "Demon Hunter Martial Arts, Extreme Speed & Burst Combat, Anti-Vampire Weapons",
    "bio": "A fierce, high-ranking Demon Hunter who tests Fang Heng's strength firsthand and becomes entangled in the three-way struggle between Demon Hunters, Vampires, and the Holy Court.",
    "mentions": 294,
    "chapters": 31,
    "first_ch": 735,
    "last_ch": 943,
    "peak_ch": 736
  },
  {
    "rank": 51,
    "name": "Ding Min",
    "first_name": "Min",
    "last_name": "Ding",
    "aliases": "Researcher Ding Min",
    "tier": "Key Arc Figure",
    "faction": "Federation",
    "role": "Cultivation Pod & Biological Researcher",
    "arc": "District 7 Research Base & Vaccine Arc (Ch. 426–2701)",
    "abilities": "Cultivation Pod Engineering, Original Liquid Analysis, Virus Purification Research",
    "bio": "A Federation scientist who introduces Fang Heng to advanced cultivation pods and original viral liquids during the District 7 research base operation.",
    "mentions": 293,
    "chapters": 72,
    "first_ch": 426,
    "last_ch": 2701,
    "peak_ch": 542
  },
  {
    "rank": 52,
    "name": "Kapa",
    "first_name": "Kapa",
    "last_name": "Kapa",
    "aliases": "Captain Kapa",
    "tier": "Key Arc Figure",
    "faction": "Tree Spirit Tribe / World of Forests",
    "role": "Captain of the Flying Squirrel Clan",
    "arc": "Starship & Elven/Tree Spirit Alliance Arc (Ch. 3034–3244)",
    "abilities": "Dimensional Airship Navigation, Main Control Hall Operations, Tribal Diplomacy",
    "bio": "The jovial captain of the Flying Squirrel Clan who welcomes Fang Heng aboard the command vessel and coordinates travel alongside Prince Cole Karot.",
    "mentions": 288,
    "chapters": 45,
    "first_ch": 3034,
    "last_ch": 3244,
    "peak_ch": 3049
  },
  {
    "rank": 53,
    "name": "Zoran",
    "first_name": "Zoran",
    "last_name": "Zoran",
    "aliases": "Captain Zoran",
    "tier": "Key Arc Figure",
    "faction": "Federation",
    "role": "Western District Security & Mercenary Captain",
    "arc": "Western District Federation Arc (Ch. 2815–2945)",
    "abilities": "Security Command, Anti-Mutant Tactics, Facility Defense",
    "bio": "A gruff security captain in the Western District Federation who oversees incoming mercenary teams that Fang Heng's group infiltrates.",
    "mentions": 286,
    "chapters": 43,
    "first_ch": 2815,
    "last_ch": 2945,
    "peak_ch": 2924
  },
  {
    "rank": 54,
    "name": "Yu Jiayuan",
    "first_name": "Jiayuan",
    "last_name": "Yu",
    "aliases": "Operative Yu Jiayuan",
    "tier": "Key Arc Figure",
    "faction": "Punoze / Revolution Society",
    "role": "Vigilant Investigator of the Revolution Society",
    "arc": "Punoze & Holy Door Arc (Ch. 1508–2540)",
    "abilities": "Reconnaissance, Combat Support, Counter-Espionage",
    "bio": "A sharp, vigilant member of the Revolution Society in Punoze who works alongside Ruan Ziying, Luo Xu, and Sheng Tao during the uprising against the Holy Court.",
    "mentions": 279,
    "chapters": 48,
    "first_ch": 1508,
    "last_ch": 2540,
    "peak_ch": 1522
  },
  {
    "rank": 55,
    "name": "Meng Hao",
    "first_name": "Hao",
    "last_name": "Meng",
    "aliases": "Officer Meng Hao",
    "tier": "Key Arc Figure",
    "faction": "Federation",
    "role": "Federation Intelligence & Video Analysis Officer",
    "arc": "District 8 & District 7 Intelligence Arcs (Ch. 222–967)",
    "abilities": "Surveillance Analysis, Tactical Briefing, Regional Coordination",
    "bio": "A rising officer in the Federation who analyzes combat footage of Fang Heng's mutated zombies and coordinates early intelligence exchanges.",
    "mentions": 276,
    "chapters": 46,
    "first_ch": 222,
    "last_ch": 967,
    "peak_ch": 705
  },
  {
    "rank": 56,
    "name": "Zhong Lei",
    "first_name": "Lei",
    "last_name": "Zhong",
    "aliases": "Deputy Commander Zhong Lei",
    "tier": "Key Arc Figure",
    "faction": "Federation",
    "role": "Deputy Commander of the District 7 Federation Forces",
    "arc": "District 7 Vaccine & Vampire Invasion Arc (Ch. 436–640)",
    "abilities": "Military Operations, Frontline Defense, Joint Taskforce Command",
    "bio": "Deputy Commander under Tian Zhen in District 7 who accompanies Fang Heng into the vampire-infested underground and is left dumbstruck when Fang Heng uproots and steals the entire Vampire Sacred Tree.",
    "mentions": 272,
    "chapters": 61,
    "first_ch": 436,
    "last_ch": 640,
    "peak_ch": 462
  },
  {
    "rank": 57,
    "name": "Karkkila",
    "first_name": "Karkkila",
    "last_name": "Karkkila",
    "aliases": "Bishop Karkkila, Archbishop Karkkila",
    "tier": "Key Arc Figure",
    "faction": "Holy Court / Purifiers",
    "role": "Archbishop of the Holy Court in the Enkama Imperial City",
    "arc": "Enkama Empire & Imperial Capital Arc (Ch. 1217–1531)",
    "abilities": "Archbishop-Tier Holy Light, Divine Prayers, Sacred Barrier Summoning",
    "bio": "A zealous Archbishop of the Holy Court stationed in the Enkama Empire who manipulates Emperor Tang Wu and clashes violently with Fang Heng and Abe Akaya during the Imperial City crisis.",
    "mentions": 270,
    "chapters": 37,
    "first_ch": 1217,
    "last_ch": 1531,
    "peak_ch": 1290
  },
  {
    "rank": 58,
    "name": "Atina",
    "first_name": "Atina",
    "last_name": "Atina",
    "aliases": "Blood Mage Atina",
    "tier": "Key Arc Figure",
    "faction": "Vampire Clan",
    "role": "Vampire Blood Curse Specialist",
    "arc": "District 7 Vampire Invasion Arc (Ch. 537–875)",
    "abilities": "Binding Blood Curse, Sacred Tree Rituals, Blood Sealing",
    "bio": "A seductive, dangerous vampire specialist skilled in binding blood curses who attempts to seal Fang Heng's Fusion Tyrant clones under the Sacred Tree Angetas.",
    "mentions": 269,
    "chapters": 39,
    "first_ch": 537,
    "last_ch": 875,
    "peak_ch": 639
  },
  {
    "rank": 59,
    "name": "Sheng Tao",
    "first_name": "Tao",
    "last_name": "Sheng",
    "aliases": "Leader Sheng Tao",
    "tier": "Key Arc Figure",
    "faction": "Punoze / Revolution Society",
    "role": "Key Vanguard Leader of the Revolution Society",
    "arc": "Punoze Uprising & Holy Door Arc (Ch. 1527–2527)",
    "abilities": "Revolutionary Command, Anti-Holy Court Warfare, Siege Operations",
    "bio": "A prominent, charismatic leader of the Revolution Society whose arrival in Punoze sparks the major confrontation against the Holy Court's sealed Holy Door.",
    "mentions": 268,
    "chapters": 38,
    "first_ch": 1527,
    "last_ch": 2527,
    "peak_ch": 1540
  },
  {
    "rank": 60,
    "name": "Mikhael",
    "first_name": "Mikhael",
    "last_name": "Mikhael",
    "aliases": "World Lord Mikhael",
    "tier": "Key Arc Figure",
    "faction": "Federation",
    "role": "World Lord of District 6 (Western/Northern Coalition)",
    "arc": "World Lords Summit & Enkama Empire Arcs (Ch. 509–1488)",
    "abilities": "World Lord Authority, Rival Coalition Command, High-Tier Combat",
    "bio": "The mocking, opportunistic World Lord of District 6 who rivals Wei Tao at the World Lords Summit and seeks to exploit the Eastern Federation's troubles before running afoul of Fang Heng.",
    "mentions": 266,
    "chapters": 73,
    "first_ch": 509,
    "last_ch": 1488,
    "peak_ch": 1124
  },
  {
    "rank": 61,
    "name": "Georgi",
    "first_name": "Georgi",
    "last_name": "Gonsalves",
    "aliases": "Georgi Gonsalves, Commander Georgi",
    "tier": "Key Arc Figure",
    "faction": "Holy Court / Purifiers",
    "role": "Commander-in-Chief of the Holy Court Expedition in Chiporeya",
    "arc": "Chiporeya World & Death Realm Arcs (Ch. 1943–3387)",
    "abilities": "Holy Court Armada Command, Sacred Light Pillars, Inquisition Tactics",
    "bio": "Commander-in-Chief Georgi Gonsalves, dispatched by the Holy Court to conquer the Chiporeya game world, where his crusading forces collide with Fang Heng's alchemy arrays and undead legions.",
    "mentions": 264,
    "chapters": 76,
    "first_ch": 1943,
    "last_ch": 3387,
    "peak_ch": 2705
  },
  {
    "rank": 62,
    "name": "Kou Huai",
    "first_name": "Huai",
    "last_name": "Kou",
    "aliases": "Director Kou Huai",
    "tier": "Key Arc Figure",
    "faction": "Federation",
    "role": "Chief Director of the Federation's District 7 Operation",
    "arc": "District 7 Investigation Arc (Ch. 345–593)",
    "abilities": "Strategic Intelligence, Operations Management, Classified File Control",
    "bio": " Cheng Ya's superior and the strategic head of the Federation's District 7 operations who evaluates Fang Heng's early actions with the Scavenger Army.",
    "mentions": 264,
    "chapters": 45,
    "first_ch": 345,
    "last_ch": 593,
    "peak_ch": 513
  },
  {
    "rank": 63,
    "name": "Xiao Yun",
    "first_name": "Yun",
    "last_name": "Xiao",
    "aliases": "Commander Xiao Yun",
    "tier": "Key Arc Figure",
    "faction": "Enkama Empire / Royal Family",
    "role": "Commander of the Imperial Royal Guards",
    "arc": "Enkama Empire Royal Palace Arc (Ch. 1165–1385)",
    "abilities": "Royal Guard Swordsmanship, Lifeblood Burst, Palace Defense",
    "bio": "The fiercely loyal commander of the royal guards in the Enkama Empire who battles Fang Heng's summoned Vampire King's Coffin and blood altars.",
    "mentions": 263,
    "chapters": 38,
    "first_ch": 1165,
    "last_ch": 1385,
    "peak_ch": 1350
  },
  {
    "rank": 64,
    "name": "Wayne",
    "first_name": "Wayne",
    "last_name": "Wayne",
    "aliases": "President Wayne",
    "tier": "Key Arc Figure",
    "faction": "Vampire Clan",
    "role": "President of the Vampire Elders Council / Vampire Association",
    "arc": "Vampire Headquarters & Dimensional Vampire Arcs (Ch. 661–2964)",
    "abilities": "Elder-Tier Hemomancy, Clan Governance, Bloodline Evaluation",
    "bio": "The calculating president of the vampire leadership who oversees responses to intruders and later evaluates Arkley and Fang Heng's dimensional bloodline power.",
    "mentions": 262,
    "chapters": 56,
    "first_ch": 661,
    "last_ch": 2964,
    "peak_ch": 2834
  },
  {
    "rank": 65,
    "name": "Ma Xiaowan",
    "first_name": "Xiaowan",
    "last_name": "Ma",
    "aliases": "Deputy Commander Ma Xiaowan",
    "tier": "Key Arc Figure",
    "faction": "Enkama Empire / Royal Family",
    "role": "Deputy Commander of the Tianli Mercenary Group",
    "arc": "Enkama Border & Forest Entry Arc (Ch. 1016–1221)",
    "abilities": "Mercenary Tactics, Reconnaissance, Defensive Command",
    "bio": "The cautious and perceptive deputy commander of the Tianli Mercenary Group who escorts Tang Mingyue and Fang Heng's party through war-torn imperial territory.",
    "mentions": 260,
    "chapters": 45,
    "first_ch": 1016,
    "last_ch": 1221,
    "peak_ch": 1024
  },
  {
    "rank": 66,
    "name": "Hao Zhou",
    "first_name": "Zhou",
    "last_name": "Hao",
    "aliases": "Leader Hao Zhou",
    "tier": "Key Arc Figure",
    "faction": "Dark Knights / Apocalypse Merchants",
    "role": "Mercenary Mission Leader in District 8",
    "arc": "Early District 8 Hospital & Prison Arc (Ch. 49–285)",
    "abilities": "Explosives Handling, Heavy Melee, Squad Leadership",
    "bio": "A sturdy veteran mission leader hired through Old Black in District 8 who leads the early hospital infiltration alongside Fang Heng.",
    "mentions": 260,
    "chapters": 33,
    "first_ch": 49,
    "last_ch": 285,
    "peak_ch": 61
  },
  {
    "rank": 67,
    "name": "Cole",
    "first_name": "Cole",
    "last_name": "Cole",
    "aliases": "Editor Cole",
    "tier": "Key Arc Figure",
    "faction": "Punoze / Revolution Society",
    "role": "Senior Column Editor & Underground Safehouse Keeper",
    "arc": "Punoze Underground Arc (Ch. 1497–1577)",
    "abilities": "Information Publishing, Safehouse Concealment, Underground Networking",
    "bio": "A senior column editor in Punoze whose secluded hut serves as a critical safehouse and meeting point for Fang Heng, Ruan Ziying, and the Revolution Society.",
    "mentions": 258,
    "chapters": 24,
    "first_ch": 1497,
    "last_ch": 1577,
    "peak_ch": 1565
  },
  {
    "rank": 68,
    "name": "Proust",
    "first_name": "Proust",
    "last_name": "Proust",
    "aliases": "Lord Proust",
    "tier": "Key Arc Figure",
    "faction": "Netherworld / Death Realm / Evil Clan",
    "role": "Evolved Death Realm Overlord",
    "arc": "Death Realm & Disaster Fusion Arc (Ch. 2603–2998)",
    "abilities": "Disaster & Death Realm Fusion, 90%+ Potential Awakening, Undead Domination",
    "bio": "A formidable Death Realm warlord allied with Mu Qingxin who fuses Disaster power with Death Realm energy to conquer native creatures before clashing with Fang Heng.",
    "mentions": 253,
    "chapters": 26,
    "first_ch": 2603,
    "last_ch": 2998,
    "peak_ch": 2705
  },
  {
    "rank": 69,
    "name": "Tang Mo",
    "first_name": "Mo",
    "last_name": "Tang",
    "aliases": "Prince Tang Mo",
    "tier": "Key Arc Figure",
    "faction": "Enkama Empire / Royal Family",
    "role": "Royal Family Scion & Rival Commander",
    "arc": "Enkama Empire Succession Arc (Ch. 1055–1299)",
    "abilities": "Imperial Martial Arts, Royal Guard Command, Political Ambition",
    "bio": "A powerful member of the Tang royal clan who seeks out Tang Mingyue during the imperial succession struggle.",
    "mentions": 251,
    "chapters": 50,
    "first_ch": 1055,
    "last_ch": 1299,
    "peak_ch": 1263
  },
  {
    "rank": 70,
    "name": "Tang Wu",
    "first_name": "Wu",
    "last_name": "Tang",
    "aliases": "Emperor Tang Wu, His Majesty Tang Wu",
    "tier": "Key Arc Figure",
    "faction": "Enkama Empire / Royal Family",
    "role": "Ruling Monarch of the Enkama Empire",
    "arc": "Enkama Imperial City Climax (Ch. 1247–1384)",
    "abilities": "Imperial Authority, Capital Defense Arrays, Pact with Holy Court",
    "bio": "The desperate ruler of the Enkama Imperial City who allies with Archbishop Karkkila of the Holy Court, only to watch terrifying tentacles and Abe Akaya's roots erupt beneath his capital.",
    "mentions": 249,
    "chapters": 47,
    "first_ch": 1247,
    "last_ch": 1384,
    "peak_ch": 1263
  },
  {
    "rank": 71,
    "name": "Luo Xu",
    "first_name": "Xu",
    "last_name": "Luo",
    "aliases": "Sir Luo Xu",
    "tier": "Key Arc Figure",
    "faction": "Punoze / Revolution Society",
    "role": "High-Ranking Enforcer & Investigator in Punoze",
    "arc": "Punoze & Revolution Society Arc (Ch. 1510–2542)",
    "abilities": "Tracking & Pursuit, High-Tier Combat, Faction Command",
    "bio": "A tall, gaunt high-ranking figure with prominent cheekbones who relentlessly hunts for Fang Heng's true identity during the Punoze upheaval.",
    "mentions": 249,
    "chapters": 47,
    "first_ch": 1510,
    "last_ch": 2542,
    "peak_ch": 1576
  },
  {
    "rank": 72,
    "name": "Zhao Dongyang",
    "first_name": "Dongyang",
    "last_name": "Zhao",
    "aliases": "Specialist Zhao Dongyang",
    "tier": "Key Arc Figure",
    "faction": "Federation",
    "role": "Special Vampire Countermeasures Expert",
    "arc": "District 7 Vampire Cave Arc (Ch. 562–639)",
    "abilities": "Vampire Lore, Anti-Bloodline Gadgets, Underground Navigation",
    "bio": "A specialist hired by the Federation through special channels to guide Zhong Lei, Cheng Ya, and Fang Heng into the vampire underground in District 7.",
    "mentions": 246,
    "chapters": 46,
    "first_ch": 562,
    "last_ch": 639,
    "peak_ch": 564
  },
  {
    "rank": 73,
    "name": "Osborne",
    "first_name": "Osborne",
    "last_name": "Osborne",
    "aliases": "Master Osborne",
    "tier": "Key Arc Figure",
    "faction": "Dark Knights / Apocalypse Merchants",
    "role": "Potionology & Warehouse Quartermaster",
    "arc": "Potionology & Warlord Potion Arc (Ch. 392–553)",
    "abilities": "Potion Appraisal, Bulk Supply Management, Formula Distribution",
    "bio": "An alchemy/potion quartermaster working alongside Yatu who supplies Fang Heng with raw materials and witnesses Fang Heng's zombie clones mass-produce thousands of modified Warlord Potions.",
    "mentions": 245,
    "chapters": 41,
    "first_ch": 392,
    "last_ch": 553,
    "peak_ch": 401
  },
  {
    "rank": 74,
    "name": "Dodd",
    "first_name": "Dodd",
    "last_name": "Dodd",
    "aliases": "Investigator Dodd",
    "tier": "Key Arc Figure",
    "faction": "Necromancer Association / Tower of Bones",
    "role": "Missing Primeval Forest Investigator & Professor Eddington's Friend",
    "arc": "Primeval Forest & Tower of Bones Arcs (Ch. 821–1799)",
    "abilities": "Field Investigation, Ancient Ruins Lore, Survival",
    "bio": "A former friend of Professor Eddington whose disappearance while investigating the Glorious Sunlight Association in the primeval forest triggers a major chain mission for Fang Heng.",
    "mentions": 240,
    "chapters": 40,
    "first_ch": 821,
    "last_ch": 1799,
    "peak_ch": 1636
  },
  {
    "rank": 75,
    "name": "Mo Jianghe",
    "first_name": "Jianghe",
    "last_name": "Mo",
    "aliases": "Master Mo Jianghe",
    "tier": "Key Arc Figure",
    "faction": "Noel Clan / Occult Research",
    "role": "Grandmaster of the Sealing Art Association",
    "arc": "Sealing Art Academy & Trial Grounds Arcs (Ch. 489–2746)",
    "abilities": "Master/Grandmaster Sealing Techniques, Seal Calligraphy, Trial Administration",
    "bio": "A renowned lecturer and elder of the Sealing Art Association whose weekend seal lectures Fang Heng attends early on, and who later witnesses Fang Heng conquer the Demigod Sealing Art trial.",
    "mentions": 230,
    "chapters": 35,
    "first_ch": 489,
    "last_ch": 2746,
    "peak_ch": 2630
  },
  {
    "rank": 76,
    "name": "Warren",
    "first_name": "Warren",
    "last_name": "Warren",
    "aliases": "Lord Warren",
    "tier": "Key Arc Figure",
    "faction": "Enkama Empire / Royal Family",
    "role": "Imperial Noble & Chief Logistics Patron of Tang Mingyue",
    "arc": "Enkama Empire Civil War Arc (Ch. 1124–1354)",
    "abilities": "Noble Domain Management, Supply Line Mobilization, Political Diplomacy",
    "bio": "A powerful feudal lord in the Enkama Empire who covertly supplies Princess Tang Mingyue and Fang Heng with vital war materials.",
    "mentions": 229,
    "chapters": 51,
    "first_ch": 1124,
    "last_ch": 1354,
    "peak_ch": 1194
  },
  {
    "rank": 77,
    "name": "Lin Hanzheng",
    "first_name": "Hanzheng",
    "last_name": "Lin",
    "aliases": "Operative Lin Hanzheng",
    "tier": "Key Arc Figure",
    "faction": "Federation",
    "role": "Undercover Scout in the Necromancer / Night Owl Conflict",
    "arc": "District 7 & Night Owl Arc (Ch. 532–638)",
    "abilities": "NPC Disguise, Stealth Infiltration, Field Reporting",
    "bio": "A resourceful player who disguises himself as an ordinary NPC to survive Night Owl's ambushes and witnesses Fang Heng's clashes in District 7.",
    "mentions": 228,
    "chapters": 45,
    "first_ch": 532,
    "last_ch": 638,
    "peak_ch": 539
  },
  {
    "rank": 78,
    "name": "Ignis",
    "first_name": "Ignis",
    "last_name": "Ignis",
    "aliases": "Young Master Ignis",
    "tier": "Key Arc Figure",
    "faction": "Netherworld / Death Realm / Evil Clan",
    "role": "Strongest Youth of the Mag Clan in Hell",
    "arc": "Hell Layers 37–99 Arc (Ch. 3458–3515)",
    "abilities": "Mag Clan Hellfire Combat, Lava Adaptation, Elite Squad Leadership",
    "bio": "The strongest young warrior of the Mag Clan dispatched by his patriarch to investigate the 37th upper layer of Hell, where he runs directly into Fang Heng and Abe Akaya devouring the Hell grottos.",
    "mentions": 227,
    "chapters": 31,
    "first_ch": 3458,
    "last_ch": 3515,
    "peak_ch": 3461
  },
  {
    "rank": 79,
    "name": "Ji Qiubei",
    "first_name": "Qiubei",
    "last_name": "Ji",
    "aliases": "Representative Ji Qiubei",
    "tier": "Key Arc Figure",
    "faction": "Night Owl Organization",
    "role": "De Facto Representative of the Night Owl Organization",
    "arc": "Night Owl Conspiracy & District 7 Arc (Ch. 476–659)",
    "abilities": "Mainframe Deduction Talent, Strategic Conspiracy, Assassin Mobilization",
    "bio": "A round-faced, smiling schemer whose predictive talent makes him the representative of the Night Owl organization. Despite his mainframe predicting a 95%+ success rate against Fang Heng, every single plot he orchestrates ends in catastrophic failure.",
    "mentions": 225,
    "chapters": 33,
    "first_ch": 476,
    "last_ch": 659,
    "peak_ch": 589
  },
  {
    "rank": 80,
    "name": "Eugene",
    "first_name": "Eugene",
    "last_name": "Eugene",
    "aliases": "Commander Eugene",
    "tier": "Key Arc Figure",
    "faction": "God Clan / Tribunal of Sin",
    "role": "Lead God Clan Investigator",
    "arc": "God Clan Pursuit Arc (Ch. 3367–3388)",
    "abilities": "Dark Gold Mental Strength Arrows, God Clan Coercion, Spatial Tracking",
    "bio": "An arrogant elite of the God Clan who leads Archbishop Auston and a divine squad to investigate Kevin's death, wielding tangible dark-gold arrows of mental strength against Fang Heng.",
    "mentions": 211,
    "chapters": 16,
    "first_ch": 3367,
    "last_ch": 3388,
    "peak_ch": 3384
  },
  {
    "rank": 81,
    "name": "Xius",
    "first_name": "Xius",
    "last_name": "Xius",
    "aliases": "Lord Xius",
    "tier": "Key Arc Figure",
    "faction": "God Clan / Tribunal of Sin",
    "role": "High-Ranking God Clan Overseer",
    "arc": "Netherworld & God Clan Arc (Ch. 3252–3538)",
    "abilities": "Divine Realm Authority, Spatial Sensing, Multi-Race Subjugation",
    "bio": "A prideful leader among the God Clan who receives the submission of lower races and monitors the spatial anomalies triggered by Fang Heng's Blood Explosion and Netherworld expansion.",
    "mentions": 209,
    "chapters": 33,
    "first_ch": 3252,
    "last_ch": 3538,
    "peak_ch": 3300
  },
  {
    "rank": 82,
    "name": "Rudyard",
    "first_name": "Rudyard",
    "last_name": "Rudyard",
    "aliases": "Patriarch Rudyard",
    "tier": "Key Arc Figure",
    "faction": "Tree Spirit Tribe / World of Forests",
    "role": "Patriarch of the Leaf Tribe",
    "arc": "World of Forests & Temple of Incantation Arc (Ch. 2211–2312)",
    "abilities": "Leaf Tribe Nature Power, Sacred Tree Sensing, Tribal Warfare",
    "bio": "The stern patriarch of the Leaf Tribe who guards the island of the Sacred Tree and eventually falls victim to Abe Akaya's Blood Nutrient absorption during the climax of the forest conflict.",
    "mentions": 209,
    "chapters": 25,
    "first_ch": 2211,
    "last_ch": 2312,
    "peak_ch": 2302
  },
  {
    "rank": 83,
    "name": "Orkney",
    "first_name": "Orkney",
    "last_name": "Orkney",
    "aliases": "Adjudicator Orkney",
    "tier": "Key Arc Figure",
    "faction": "Holy Court / Purifiers",
    "role": "Holy Realm Adjudicator of the Holy Court",
    "arc": "Duncha World & Holy Realm Investigation Arcs (Ch. 2048–2797)",
    "abilities": "Holy Adjudication, Divine Judgement Arrays, Cross-Realm Investigation",
    "bio": "A high-ranking adjudicator dispatched from the Holy Realm with five arbitrator officials to investigate Fang Heng's devastation of Holy Court forces in the lower realms.",
    "mentions": 206,
    "chapters": 38,
    "first_ch": 2048,
    "last_ch": 2797,
    "peak_ch": 2792
  },
  {
    "rank": 84,
    "name": "Pena",
    "first_name": "Pena",
    "last_name": "Pena",
    "aliases": "Envoy Pena",
    "tier": "Key Arc Figure",
    "faction": "Netherworld / Death Realm / Evil Clan",
    "role": "Netherworld Contact & Associate of Zane",
    "arc": "Netherworld & Hell Entry Arc (Ch. 3391–3447)",
    "abilities": "Underworld Intelligence, Shadow Passage Control, Soul Bartering",
    "bio": "A pragmatic female operative in the Netherworld and longtime acquaintance of Zane who assists Fang Heng's group during their deeper push toward the Hell passages.",
    "mentions": 206,
    "chapters": 37,
    "first_ch": 3391,
    "last_ch": 3447,
    "peak_ch": 3438
  },
  {
    "rank": 85,
    "name": "Hain",
    "first_name": "Hain",
    "last_name": "Hain",
    "aliases": "Commander Hain",
    "tier": "Key Arc Figure",
    "faction": "Holy Court / Purifiers",
    "role": "Commander of the God's Punishment Knight Legion",
    "arc": "Demon Suppressing Temple & Starry Temple Arc (Ch. 2756–3018)",
    "abilities": "God's Punishment Holy Strikes, Knight Legion Command, Ancient Temple Lore",
    "bio": "The veteran commander of the God's Punishment Knight Legion at the Demon Suppressing Temple who tests Fang Heng's claim as the Great Sage's inheritor.",
    "mentions": 205,
    "chapters": 27,
    "first_ch": 2756,
    "last_ch": 3018,
    "peak_ch": 2758
  },
  {
    "rank": 86,
    "name": "Argyll",
    "first_name": "Argyll",
    "last_name": "Argyll",
    "aliases": "Guide Argyll",
    "tier": "Key Arc Figure",
    "faction": "Enkama Empire / Royal Family",
    "role": "Veteran Pathfinder & Expedition Specialist",
    "arc": "Enkama Underground & Starry Temple Arcs (Ch. 1079–2744)",
    "abilities": "Subterranean Navigation, Trap Detection, Ruin Exploration",
    "bio": "A thin, middle-aged specialist who accompanies Mo Jiawei and Fang Heng down perilous rock walls and ancient ruins.",
    "mentions": 204,
    "chapters": 29,
    "first_ch": 1079,
    "last_ch": 2744,
    "peak_ch": 2740
  },
  {
    "rank": 87,
    "name": "Mu Shunan",
    "first_name": "Mu",
    "last_name": "Shunan",
    "aliases": "Warrior Mu Shunan",
    "tier": "Key Arc Figure",
    "faction": "Noel Clan / Occult Research",
    "role": "External Demigod Occult Warrior of the Noel Clan",
    "arc": "Noel Clan & Demigod Occult Arc (Ch. 3072–3175)",
    "abilities": "Demigod-Level Occultism, Meditation Array Control, Spiritual Combat",
    "bio": "A warm, accomplished outsider warrior possessing demigod-level Occult strength recruited by the Noel Clan, who welcomes Fang Heng and connects him with Instructor Nasir's alchemy lineage.",
    "mentions": 204,
    "chapters": 26,
    "first_ch": 3072,
    "last_ch": 3175,
    "peak_ch": 3080
  },
  {
    "rank": 88,
    "name": "Emery",
    "first_name": "Emery",
    "last_name": "Emery",
    "aliases": "Chief Inspector Emery",
    "tier": "Key Arc Figure",
    "faction": "Federation",
    "role": "Chief Inspector of the Mutant Worm Cocoon Investigation",
    "arc": "Western District Cocoon Theft Arc (Ch. 2902–2966)",
    "abilities": "Forensic Detection, Psychological Interrogation, Lockdown Command",
    "bio": "The sharp-eyed chief inspector assigned to investigate the disappearance of the mutant worm cocoons (which Fang Heng secretly absorbed to upgrade his Seed of Ouroboros).",
    "mentions": 203,
    "chapters": 26,
    "first_ch": 2902,
    "last_ch": 2966,
    "peak_ch": 2935
  },
  {
    "rank": 89,
    "name": "Zheng Yuping",
    "first_name": "Yuping",
    "last_name": "Zheng",
    "aliases": "Captain Zheng Yuping",
    "tier": "Key Arc Figure",
    "faction": "Federation",
    "role": "Captain of the Federation Enforcement Team",
    "arc": "Tower of Bones Entry Arc (Ch. 1394–1458)",
    "abilities": "Law Enforcement Tactics, Player Level Verification, Squad Lockdown",
    "bio": "The captain of the Federation's enforcement team outside the Tower of Bones who is stunned to discover that Fang Heng has already reached Level 30 and unlocked the second talent advancement.",
    "mentions": 201,
    "chapters": 30,
    "first_ch": 1394,
    "last_ch": 1458,
    "peak_ch": 1406
  },
  {
    "rank": 90,
    "name": "Anthea",
    "first_name": "Anthea",
    "last_name": "Anthea",
    "aliases": "Commander Anthea",
    "tier": "Key Arc Figure",
    "faction": "Enkama Empire / Royal Family",
    "role": "Female Commander of the Jones Kingdom Expedition",
    "arc": "Enkama Border & Jones Kingdom Arc (Ch. 1893–1926)",
    "abilities": "Border Warfare, Expeditionary Command, Defensive Formations",
    "bio": "A prudent female military commander of the Jones Kingdom ordered by her king to explore the hazardous border regions of the Enkama Empire.",
    "mentions": 200,
    "chapters": 27,
    "first_ch": 1893,
    "last_ch": 1926,
    "peak_ch": 1899
  },
  {
    "rank": 91,
    "name": "Vettel",
    "first_name": "Vettel",
    "last_name": "Vettel",
    "aliases": "Merchant Vettel",
    "tier": "Key Arc Figure",
    "faction": "Dark Knights / Apocalypse Merchants",
    "role": "Apocalypse Merchant Camp Leader in District 8",
    "arc": "Early District 8 Survival & Talent Plan Arc (Ch. 10–1614)",
    "abilities": "Apocalypse Trade System, Bounty Issuance, Talent Plan Appraisal",
    "bio": "The very first Apocalypse Merchant NPC Fang Heng deals with in Chapter 10. Vettel buys Fang Heng's massive zombie-harvested wood stockpiles, issues the lumberyard clearing quest, and rewards him with the A-minus Talent Enhancement Plan.",
    "mentions": 198,
    "chapters": 40,
    "first_ch": 10,
    "last_ch": 1614,
    "peak_ch": 42
  },
  {
    "rank": 92,
    "name": "Arkley",
    "first_name": "Arkley",
    "last_name": "Arkley",
    "aliases": "Lord Arkley",
    "tier": "Key Arc Figure",
    "faction": "Vampire Clan",
    "role": "Dimensional-Empowered Vampire Prodigy",
    "arc": "Western District & Dimensional Vampire Arc (Ch. 2831–3270)",
    "abilities": "Dimensional Bloodline Power, High-Speed Blood Assault, Elder Council Backing",
    "bio": "A vampire with a special identity whose combat power skyrockets after absorbing dimensional energy, serving as President Wayne's benchmark against Fang Heng.",
    "mentions": 196,
    "chapters": 52,
    "first_ch": 2831,
    "last_ch": 3270,
    "peak_ch": 2835
  },
  {
    "rank": 93,
    "name": "Simone",
    "first_name": "Simone",
    "last_name": "Simone",
    "aliases": "Broker Simone",
    "tier": "Key Arc Figure",
    "faction": "Noel Clan / Occult Research",
    "role": "Urban Village Internet Café Contact",
    "arc": "Demonic Seed & Ring Mission Arc (Ch. 2464–2496)",
    "abilities": "Encrypted Communications, Ring Mission Coordination, Underground Guiding",
    "bio": "A key contact hiding in an urban village internet café whose ring mission leads Fang Heng into the Demonic Seed arena and Occult Research plotline.",
    "mentions": 196,
    "chapters": 20,
    "first_ch": 2464,
    "last_ch": 2496,
    "peak_ch": 2467
  },
  {
    "rank": 94,
    "name": "Meng Bo",
    "first_name": "Bo",
    "last_name": "Meng",
    "aliases": "Captain Meng Bo",
    "tier": "Key Arc Figure",
    "faction": "Vampire Clan",
    "role": "Vampire-Turned Scavenger Investigator",
    "arc": "District 7 Sacred Tree Rebirth Arc (Ch. 536–590)",
    "abilities": "Binding Blood Curse, Sacred Tree Soul Rebirth, Undercover Sabotage",
    "bio": "An arrogant operative who obtains the binding blood curse from Atina and is repeatedly killed and reborn through the Vampire Sacred Tree Angetas, inadvertently revealing Angetas's soul-rebirth mechanics to Fang Heng.",
    "mentions": 195,
    "chapters": 18,
    "first_ch": 536,
    "last_ch": 590,
    "peak_ch": 555
  },
  {
    "rank": 95,
    "name": "Norbert",
    "first_name": "Norbert",
    "last_name": "Norbert",
    "aliases": "President Norbert",
    "tier": "Key Arc Figure",
    "faction": "Necromancer Association / Tower of Bones",
    "role": "President of the Eternal Night Guild",
    "arc": "Tower of Bones Defense Arc (Ch. 2408–2447)",
    "abilities": "Guild Command, Necromancy Support, Defensive Coordination",
    "bio": "The respectful young president of the Eternal Night Guild who coordinates with Fang Heng, Li Shaoqiang, and Tan Shuo during the Purifiers' assault on the Tower of Bones.",
    "mentions": 195,
    "chapters": 18,
    "first_ch": 2408,
    "last_ch": 2447,
    "peak_ch": 2444
  },
  {
    "rank": 96,
    "name": "Robben",
    "first_name": "Robben",
    "last_name": "Robben",
    "aliases": "Leader Robben",
    "tier": "Key Arc Figure",
    "faction": "Federation",
    "role": "Federation Expedition Leader in Punoze",
    "arc": "Tower of Bones & Punoze Entry Arc (Ch. 1410–1484)",
    "abilities": "Diplomatic Badges, Team Coordination, Tactical Reconnaissance",
    "bio": "A smiling, well-prepared Federation team leader who distributes special badges and coordinates joint entry operations with Fang Heng's group.",
    "mentions": 192,
    "chapters": 22,
    "first_ch": 1410,
    "last_ch": 1484,
    "peak_ch": 1478
  },
  {
    "rank": 97,
    "name": "Augustine",
    "first_name": "Augustine",
    "last_name": "Augustine",
    "aliases": "Director Augustine",
    "tier": "Key Arc Figure",
    "faction": "Federation",
    "role": "Director of the Black Fog Crisis Management Division (Western Federation Parliament)",
    "arc": "Western District Black Fog & Netherworld Arc (Ch. 2925–3344)",
    "abilities": "Black Fog Countermeasures, Parliamentary Crisis Authority, Elite Taskforce Command",
    "bio": "The affable yet sharp Director of the Black Fog Crisis Management Division in the Western District Federation Parliament who recruits elite operatives to contain the spreading Black Fog.",
    "mentions": 190,
    "chapters": 32,
    "first_ch": 2925,
    "last_ch": 3344,
    "peak_ch": 3330
  },
  {
    "rank": 98,
    "name": "Cheng Ya",
    "first_name": "Ya",
    "last_name": "Cheng",
    "aliases": "Operative Cheng Ya",
    "tier": "Key Arc Figure",
    "faction": "Federation",
    "role": "District 7 Federation Field Operative",
    "arc": "District 7 Scavenger Army & Vampire Arc (Ch. 343–583)",
    "abilities": "Field Reconnaissance, Intelligence Reporting, Tactical Firearms",
    "bio": "A proud female operative under Kou Huai in District 7 who initially keeps her distance from Fang Heng before being drawn into his audacious operations against the Scavenger Army and Vampires.",
    "mentions": 187,
    "chapters": 32,
    "first_ch": 343,
    "last_ch": 583,
    "peak_ch": 345
  },
  {
    "rank": 99,
    "name": "Tian Zhen",
    "first_name": "Zhen",
    "last_name": "Tian",
    "aliases": "Commander Tian Zhen",
    "tier": "Key Arc Figure",
    "faction": "Federation",
    "role": "Chief Commander of the Federation in District 7",
    "arc": "District 7 Vaccine & Vampire War Arc (Ch. 403–642)",
    "abilities": "Regional Military Command, Guild Coalition Leadership, Crisis Defense",
    "bio": "The stressed Chief Commander of District 7 who rallies the major player guilds and relies on Fang Heng's shelter research to survive the viral mutation and vampire invasion.",
    "mentions": 187,
    "chapters": 30,
    "first_ch": 403,
    "last_ch": 642,
    "peak_ch": 441
  },
  {
    "rank": 100,
    "name": "Xie Junhao",
    "first_name": "Junhao",
    "last_name": "Xie",
    "aliases": "Deputy Chief Commander Xie Junhao",
    "tier": "Key Arc Figure",
    "faction": "Federation",
    "role": "Hostile Deputy Chief Commander Sent to District 7",
    "arc": "District 7 Vampire Sacred Tree Climax (Ch. 582–642)",
    "abilities": "Heavy Military Command, Political Coercion, Frontline Blockade",
    "bio": "An ambitious, ill-intentioned Deputy Chief Commander dispatched by higher-ups to seize credit in District 7, who ends up scapegoated by the furious Vampires when Fang Heng steals their Sacred Tree.",
    "mentions": 186,
    "chapters": 27,
    "first_ch": 582,
    "last_ch": 642,
    "peak_ch": 625
  },
  {
    "rank": 101,
    "name": "Karolina",
    "first_name": "Karolina",
    "last_name": "Karolina",
    "aliases": "Purifier Karolina",
    "tier": "Supporting Character",
    "faction": "Holy Court / Purifiers",
    "role": "Purifier Instructor from the Holy Realm",
    "arc": "Tower of Bones Siege Arc (Ch. 2418–2460)",
    "abilities": "Holy Purification Arrays, Purifier Squad Command",
    "bio": "An elite Purifier instructor from the Holy Realm who leads the Holy Court's purification siege against the Tower of Bones while Fang Heng absorbs the undead aura inside.",
    "mentions": 179,
    "chapters": 20,
    "first_ch": 2418,
    "last_ch": 2460,
    "peak_ch": 2458
  },
  {
    "rank": 102,
    "name": "Zet",
    "first_name": "Zet",
    "last_name": "Zet",
    "aliases": "Mage Zet",
    "tier": "Supporting Character",
    "faction": "Tree Spirit Tribe / World of Forests",
    "role": "Magic Array Overseer of the Tree Spirit Tribe",
    "arc": "World of Forests Temple Arc (Ch. 2269–2292)",
    "abilities": "Sacred Tree Array Construction, Dimensional Channeling",
    "bio": "A specialist trusted by Elder Vannes to oversee the construction of the Sacred Tree magic array, unwittingly giving Fang Heng direct access to siphon dimensional energy.",
    "mentions": 179,
    "chapters": 17,
    "first_ch": 2269,
    "last_ch": 2292,
    "peak_ch": 2270
  },
  {
    "rank": 103,
    "name": "Patrick",
    "first_name": "Patrick",
    "last_name": "Patrick",
    "aliases": "Commander Patrick",
    "tier": "Supporting Character",
    "faction": "God Clan / Tribunal of Sin",
    "role": "Divine Expedition Leader in Hell",
    "arc": "Eyes of Hell & God Clan Arc (Ch. 3484–3520)",
    "abilities": "Sustained Divine Brilliance, Hell Expedition Command",
    "bio": "A powerful commander who leads an expedition deep into Hell to reclaim the Eyes of Hell before encountering Fang Heng's overwhelming forces.",
    "mentions": 178,
    "chapters": 22,
    "first_ch": 3484,
    "last_ch": 3520,
    "peak_ch": 3493
  },
  {
    "rank": 104,
    "name": "Gano",
    "first_name": "Gano",
    "last_name": "Gano",
    "aliases": "Operative Gano",
    "tier": "Supporting Character",
    "faction": "Punoze / Revolution Society",
    "role": "Impulsive Field Leader in Punoze",
    "arc": "Punoze Faction Conflict Arc (Ch. 1446–1627)",
    "abilities": "Close-Quarters Assault, Urban Raids",
    "bio": "A hot-tempered faction leader in Punoze who clashes with Yatsek's Chamber of Commerce and gets caught up in the chaos surrounding Fang Heng.",
    "mentions": 176,
    "chapters": 18,
    "first_ch": 1446,
    "last_ch": 1627,
    "peak_ch": 1451
  },
  {
    "rank": 105,
    "name": "Chadwick",
    "first_name": "Chadwick",
    "last_name": "Chadwick",
    "aliases": "Lord Chadwick",
    "tier": "Supporting Character",
    "faction": "Enkama Empire / Royal Family",
    "role": "Treacherous Imperial Feudal Lord",
    "arc": "Enkama Empire Betrayal Arc (Ch. 1222–1336)",
    "abilities": "Feudal Cavalry Command, Ambush Warfare",
    "bio": "A feudal lord of the Enkama Empire who suddenly turns hostile and backstabs Mo Jiawei, triggering Fang Heng's ruthless retaliation.",
    "mentions": 173,
    "chapters": 30,
    "first_ch": 1222,
    "last_ch": 1336,
    "peak_ch": 1269
  },
  {
    "rank": 106,
    "name": "Gisele",
    "first_name": "Gisele",
    "last_name": "Gisele",
    "aliases": "Captain Gisele",
    "tier": "Supporting Character",
    "faction": "Federation",
    "role": "Captain of the Western Federation Security Guard",
    "arc": "Western District Cocoon & Black Fog Arc (Ch. 2904–2979)",
    "abilities": "Facility Lockdown, Squad Tactics, Investigation Support",
    "bio": "A security captain working alongside Chief Inspector Emery during the Western District mutant cocoon investigation.",
    "mentions": 172,
    "chapters": 32,
    "first_ch": 2904,
    "last_ch": 2979,
    "peak_ch": 2968
  },
  {
    "rank": 107,
    "name": "An Qian",
    "first_name": "Qian",
    "last_name": "An",
    "aliases": "Envoy An Qian",
    "tier": "Supporting Character",
    "faction": "Noel Clan / Occult Research",
    "role": "Noel Clan Liaison & Recruiter",
    "arc": "Noel Clan & Elder Ambrose Arc (Ch. 3069–3246)",
    "abilities": "Occultism, Clan Etiquette & Liaison",
    "bio": "A polite, perceptive member of the Noel Clan who recruits Fang Heng as an external warrior and introduces him to Mu Shunan and Great Elder Ambrose.",
    "mentions": 171,
    "chapters": 43,
    "first_ch": 3069,
    "last_ch": 3246,
    "peak_ch": 3071
  },
  {
    "rank": 108,
    "name": "Raven",
    "first_name": "Raven",
    "last_name": "Raven",
    "aliases": "Operative Raven",
    "tier": "Supporting Character",
    "faction": "Tree Spirit Tribe / World of Forests",
    "role": "Scout & Field Operative",
    "arc": "World of Forests & Western District Arcs (Ch. 2174–2855)",
    "abilities": "Forest Reconnaissance, Stealth Tracking",
    "bio": "A recurring field operative active during the World of Forests and Western District campaigns.",
    "mentions": 170,
    "chapters": 20,
    "first_ch": 2174,
    "last_ch": 2855,
    "peak_ch": 2174
  },
  {
    "rank": 109,
    "name": "Zhao Nan",
    "first_name": "Nan",
    "last_name": "Zhao",
    "aliases": "Captain Zhao Nan",
    "tier": "Supporting Character",
    "faction": "Federation",
    "role": "Federation Defense Captain",
    "arc": "Holy Court Incursion Arc (Ch. 669–719)",
    "abilities": "Defensive Line Command, Firearms Mastery",
    "bio": "A frontline captain who coordinates player defenses during the early Holy Court and vampire skirmishes.",
    "mentions": 169,
    "chapters": 18,
    "first_ch": 669,
    "last_ch": 719,
    "peak_ch": 690
  },
  {
    "rank": 110,
    "name": "Qiao Wei",
    "first_name": "Wei",
    "last_name": "Qiao",
    "aliases": "Investigator Qiao Wei",
    "tier": "Supporting Character",
    "faction": "Federation",
    "role": "Special School Incident Investigator",
    "arc": "Real-World & Demi-Human Investigation Arc (Ch. 1776–1835)",
    "abilities": "Field Forensics, Demi-Human Tracking",
    "bio": "An investigator working with Kleinman on the abnormal school incident and demi-human emergence.",
    "mentions": 169,
    "chapters": 16,
    "first_ch": 1776,
    "last_ch": 1835,
    "peak_ch": 1779
  },
  {
    "rank": 111,
    "name": "Narlyev",
    "first_name": "Narlyev",
    "last_name": "Narlyev",
    "aliases": "Master Narlyev",
    "tier": "Supporting Character",
    "faction": "Noel Clan / Occult Research",
    "role": "Occult Research Association Elder",
    "arc": "Jealousy Demonic Seed Arc (Ch. 2511–2540)",
    "abilities": "Occult Sealing, Demonic Seed Analysis",
    "bio": "A senior member of the Occult Research Association during the campaign to suppress and absorb the Jealousy Demonic Seed.",
    "mentions": 164,
    "chapters": 21,
    "first_ch": 2511,
    "last_ch": 2540,
    "peak_ch": 2513
  },
  {
    "rank": 112,
    "name": "Prisoner Snake",
    "first_name": "Snake",
    "last_name": "Prisoner",
    "aliases": "Snake",
    "tier": "Supporting Character",
    "faction": "Prison 507 / Zombie Apocalypse",
    "role": "Notorious Inmate Boss of Prison No. 507",
    "arc": "Early Prison No. 507 Clearing Arc (Ch. 19–132)",
    "abilities": "Prison Gang Control, Firearms & Riot Gear",
    "bio": "The ruthless inmate boss who originally controlled part of Prison No. 507 before Fang Heng's growing zombie horde wiped out his gang and claimed the prison.",
    "mentions": 164,
    "chapters": 18,
    "first_ch": 19,
    "last_ch": 132,
    "peak_ch": 87
  },
  {
    "rank": 113,
    "name": "Lin Nuo",
    "first_name": "Nuo",
    "last_name": "Lin",
    "aliases": "Hunter Lin Nuo",
    "tier": "Supporting Character",
    "faction": "Black Castle / Demon Hunters",
    "role": "Top-Tier Demon Hunter",
    "arc": "Sacred Tree Angetas & Demon Hunter Arc (Ch. 728–792)",
    "abilities": "Demon Hunting Blade Arts, Blood Pool Ambush",
    "bio": "An elite Demon Hunter who confronts Fang Heng in front of the Vampire Sacred Tree Angetas and witnesses Fang Heng tank the lethal blood poison with his Undying Body.",
    "mentions": 160,
    "chapters": 24,
    "first_ch": 728,
    "last_ch": 792,
    "peak_ch": 772
  },
  {
    "rank": 114,
    "name": "Mo Yunxiao",
    "first_name": "Yunxiao",
    "last_name": "Mo",
    "aliases": "Elder Mo Yunxiao",
    "tier": "Supporting Character",
    "faction": "Necromancer Association / Tower of Bones",
    "role": "Senior Necromancer & Mentor Contact",
    "arc": "District 8 to Tower of Bones Arcs (Ch. 252–1497)",
    "abilities": "Necromancy, Faction Diplomacy",
    "bio": "A respected necromancer who bridges Fang Heng's early necromancy studies with Dickey and the wider Necromancer Association.",
    "mentions": 159,
    "chapters": 41,
    "first_ch": 252,
    "last_ch": 1497,
    "peak_ch": 252
  },
  {
    "rank": 115,
    "name": "Randolf",
    "first_name": "Randolf",
    "last_name": "Randolf",
    "aliases": "Lord Randolf",
    "tier": "Supporting Character",
    "faction": "Enkama Empire / Royal Family",
    "role": "Imperial Noble & Commander",
    "arc": "Enkama Empire Campaign (Ch. 1069–1333)",
    "abilities": "Noble Command, Siege Defense",
    "bio": "An imperial nobleman involved in the military struggle surrounding Tang Mingyue's faction in the Enkama Empire.",
    "mentions": 159,
    "chapters": 30,
    "first_ch": 1069,
    "last_ch": 1333,
    "peak_ch": 1104
  },
  {
    "rank": 116,
    "name": "Joel",
    "first_name": "Joel",
    "last_name": "Joel",
    "aliases": "Vampire Joel",
    "tier": "Supporting Character",
    "faction": "Vampire Clan",
    "role": "Vampire Clan Officer",
    "arc": "Vampire World & Forest Arcs (Ch. 770–2160)",
    "abilities": "Hemomancy, Blood Scout",
    "bio": "A vampire officer who participates in the bloodline wars and cross-realm operations.",
    "mentions": 159,
    "chapters": 19,
    "first_ch": 770,
    "last_ch": 2160,
    "peak_ch": 989
  },
  {
    "rank": 117,
    "name": "Roche",
    "first_name": "Roche",
    "last_name": "Roche",
    "aliases": "Commander Roche",
    "tier": "Supporting Character",
    "faction": "Dark Knights / Apocalypse Merchants",
    "role": "Scavenger Army & Potion Arc Commander",
    "arc": "District 7 Scavenger Army Arc (Ch. 341–448)",
    "abilities": "Arms Dealing, Base Command",
    "bio": "A regional commander in District 7 who interacts with Fang Heng during the Scavenger Army weapons and potion operations.",
    "mentions": 158,
    "chapters": 27,
    "first_ch": 341,
    "last_ch": 448,
    "peak_ch": 395
  },
  {
    "rank": 118,
    "name": "Brutus",
    "first_name": "Brutus",
    "last_name": "Brutus",
    "aliases": "Lord Brutus",
    "tier": "Supporting Character",
    "faction": "Netherworld / Death Realm / Evil Clan",
    "role": "Ancient Undead / Void-Touched Warlord",
    "arc": "Vampire Inheritance & Origin Power Arcs (Ch. 958–3436)",
    "abilities": "Heavy Undead Combat, Origin Power Clash",
    "bio": "A powerful recurring antagonist/warlord who appears across the Vampire inheritance and late-game Origin Power battles.",
    "mentions": 156,
    "chapters": 22,
    "first_ch": 958,
    "last_ch": 3436,
    "peak_ch": 3418
  },
  {
    "rank": 119,
    "name": "Zhou Yi",
    "first_name": "Yi",
    "last_name": "Zhou",
    "aliases": "Player Zhou Yi",
    "tier": "Supporting Character",
    "faction": "Prison 507 / Zombie Apocalypse",
    "role": "Early Survivor & Companion of Lu Yu",
    "arc": "Starter Forest & Merchant Camp Arc (Ch. 15–334)",
    "abilities": "Basic Survival, Resource Gathering",
    "bio": "An early player traveling with Lu Yu in District 8 who is floored by Fang Heng's massive survival point transactions and wood stockpiles.",
    "mentions": 155,
    "chapters": 23,
    "first_ch": 15,
    "last_ch": 334,
    "peak_ch": 41
  },
  {
    "rank": 120,
    "name": "Deng Xin",
    "first_name": "Xin",
    "last_name": "Deng",
    "aliases": "Leader Deng Xin",
    "tier": "Supporting Character",
    "faction": "Federation",
    "role": "Early District 8 Player Guild Leader",
    "arc": "District 8 Shelter Competition Arc (Ch. 134–298)",
    "abilities": "Guild Management, Early Firearms",
    "bio": "A local player leader in District 8 who witnesses Fang Heng's rapid monopolization of the server's resources and missions.",
    "mentions": 155,
    "chapters": 18,
    "first_ch": 134,
    "last_ch": 298,
    "peak_ch": 135
  },
  {
    "rank": 121,
    "name": "Sydney",
    "first_name": "Sydney",
    "last_name": "Sydney",
    "aliases": "Alchemist Sydney",
    "tier": "Supporting Character",
    "faction": "Enkama Empire / Royal Family",
    "role": "Dual-Array Eye Alchemist in Enkama",
    "arc": "Enkama Alchemy & Omniscient Eye Arc (Ch. 1192–1286)",
    "abilities": "Optical Alchemy Arrays, Magic Circle Control",
    "bio": "A mysterious robed alchemist with dual alchemy magic arrays in his eyes encountered by Fang Heng and Tang Mingyue prior to Fang Heng acquiring the Omniscient Eye.",
    "mentions": 154,
    "chapters": 21,
    "first_ch": 1192,
    "last_ch": 1286,
    "peak_ch": 1209
  },
  {
    "rank": 122,
    "name": "Damon",
    "first_name": "Damon",
    "last_name": "Damon",
    "aliases": "President Damon",
    "tier": "Supporting Character",
    "faction": "Noel Clan / Occult Research",
    "role": "President of the Sealing Art Association",
    "arc": "Sealing Art Trial Grounds Arc (Ch. 2631–3379)",
    "abilities": "Grandmaster/Demigod Sealing Arts, Association Governance",
    "bio": "The diligent president of the Sealing Art Association who oversees the Sealing Art trial grounds alongside Mo Jianghe.",
    "mentions": 152,
    "chapters": 17,
    "first_ch": 2631,
    "last_ch": 3379,
    "peak_ch": 3360
  },
  {
    "rank": 123,
    "name": "Shi Lipeng",
    "first_name": "Lipeng",
    "last_name": "Shi",
    "aliases": "Commander Shi Lipeng",
    "tier": "Supporting Character",
    "faction": "Necromancer Association / Tower of Bones",
    "role": "Young Operations Commander at Miyisca Fortress",
    "arc": "Miyisca Fortress & Dark City Arc (Ch. 2371–2726)",
    "abilities": "Fortress Deployment, Undead Coalition Tactics",
    "bio": "A young military planner at Miyisca Fortress who works closely with Li Qingran and Tang Chuji during the Death Realm and Dark City campaigns.",
    "mentions": 150,
    "chapters": 37,
    "first_ch": 2371,
    "last_ch": 2726,
    "peak_ch": 2660
  },
  {
    "rank": 124,
    "name": "Zhong Haoyang",
    "first_name": "Haoyang",
    "last_name": "Zhong",
    "aliases": "Captain Zhong Haoyang",
    "tier": "Supporting Character",
    "faction": "Federation",
    "role": "Captain of the Western Federation Player Team",
    "arc": "Vampire World & Western Federation Arc (Ch. 755–997)",
    "abilities": "Squad Command, Tactical Assault",
    "bio": "Captain of an elite player team from the Western Federation who chooses diplomacy over hostility when encountering Fang Heng.",
    "mentions": 148,
    "chapters": 22,
    "first_ch": 755,
    "last_ch": 997,
    "peak_ch": 974
  },
  {
    "rank": 125,
    "name": "Dormer",
    "first_name": "Dormer",
    "last_name": "Dormer",
    "aliases": "Captain Dormer",
    "tier": "Supporting Character",
    "faction": "Federation",
    "role": "Captain of the Federal Field Team",
    "arc": "Mutant Zone & Late-Game Arcs (Ch. 1709–3499)",
    "abilities": "Field Medicine Support, Tactical Command",
    "bio": "A seasoned federal team captain who cooperates with Fang Heng during high-risk field operations.",
    "mentions": 147,
    "chapters": 27,
    "first_ch": 1709,
    "last_ch": 3499,
    "peak_ch": 3496
  },
  {
    "rank": 126,
    "name": "Jite",
    "first_name": "Jite",
    "last_name": "Jite",
    "aliases": "Boss Jite",
    "tier": "Supporting Character",
    "faction": "Black Castle / Demon Hunters",
    "role": "Gang Leader in the City of Darkness",
    "arc": "City of Darkness Arc (Ch. 1833–1999)",
    "abilities": "Underworld Brawl, Gang Mobilization",
    "bio": "A fierce local gang leader in the City of Darkness who negotiates with Meng Ruhui and the Mundt Gang.",
    "mentions": 147,
    "chapters": 17,
    "first_ch": 1833,
    "last_ch": 1999,
    "peak_ch": 1849
  },
  {
    "rank": 127,
    "name": "Yimamu",
    "first_name": "Yimamu",
    "last_name": "Yimamu",
    "aliases": "Elder Yimamu",
    "tier": "Supporting Character",
    "faction": "Enkama Empire / Royal Family",
    "role": "Shrewd Desert/Border Faction Leader",
    "arc": "Enkama Plague & Border Arc (Ch. 1309–1330)",
    "abilities": "Border Navigation, Faction Negotiation",
    "bio": "An older, shrewd leader encountered during the Enkama border and plague aura storyline.",
    "mentions": 145,
    "chapters": 19,
    "first_ch": 1309,
    "last_ch": 1330,
    "peak_ch": 1314
  },
  {
    "rank": 128,
    "name": "Ji Shaojie",
    "first_name": "Shaojie",
    "last_name": "Ji",
    "aliases": "Player Ji Shaojie",
    "tier": "Supporting Character",
    "faction": "Federation",
    "role": "Bloodline Awakening Player under Miyamoto Teru",
    "arc": "Bloodline Cultivation Arc (Ch. 2006–2021)",
    "abilities": "Bloodline Awakening, Martial Combat",
    "bio": "A player who volunteers to assist Miyamoto Teru in exchange for bloodline cultivation opportunities, only to witness Fang Heng's overwhelming power.",
    "mentions": 145,
    "chapters": 16,
    "first_ch": 2006,
    "last_ch": 2021,
    "peak_ch": 2020
  },
  {
    "rank": 129,
    "name": "Wu Siying",
    "first_name": "Siying",
    "last_name": "Wu",
    "aliases": "Assassin Wu Siying",
    "tier": "Supporting Character",
    "faction": "Federation",
    "role": "Dagger Specialist & Agile Combatant",
    "arc": "District 7 & Mid-Game Arcs (Ch. 443–1764)",
    "abilities": "Close-Range Dagger Arts, High Agility Evasion",
    "bio": "A skilled female dagger specialist who participates in the District 7 combat operations.",
    "mentions": 144,
    "chapters": 27,
    "first_ch": 443,
    "last_ch": 1764,
    "peak_ch": 913
  },
  {
    "rank": 130,
    "name": "Elisa",
    "first_name": "Elisa",
    "last_name": "Elisa",
    "aliases": "Miss Elisa",
    "tier": "Supporting Character",
    "faction": "Necromancer Association / Tower of Bones",
    "role": "Scion of the Herta Family Branch",
    "arc": "Tower of Bones Entry Arc (Ch. 1392–1458)",
    "abilities": "Necromantic Heritage, Noble Connections",
    "bio": "A young lady from a branch of the Herta family who travels with Old Man Herta to the Tower of Bones.",
    "mentions": 144,
    "chapters": 24,
    "first_ch": 1392,
    "last_ch": 1458,
    "peak_ch": 1424
  },
  {
    "rank": 131,
    "name": "David",
    "first_name": "David",
    "last_name": "David",
    "aliases": "Mr. David",
    "tier": "Supporting Character",
    "faction": "Dark Knights / Apocalypse Merchants",
    "role": "Dark Knights Liaison in District 8",
    "arc": "District 8 S-Rank Talent Plan Arc (Ch. 83–572)",
    "abilities": "Faction Appraisal, Mission Dispatch, Honor Rank Management",
    "bio": "Fang Heng's primary contact within the Dark Knights who rewards him with his first S-rank Talent Enhancement Plan (Zombie Clone Summoning).",
    "mentions": 142,
    "chapters": 33,
    "first_ch": 83,
    "last_ch": 572,
    "peak_ch": 273
  },
  {
    "rank": 132,
    "name": "Su Guantong",
    "first_name": "Guantong",
    "last_name": "Su",
    "aliases": "Operative Su Guantong",
    "tier": "Supporting Character",
    "faction": "Federation",
    "role": "Western District Train & Recruitment Operative",
    "arc": "Western District Federation Arc (Ch. 2809–2964)",
    "abilities": "Tactical Cooperation, Intelligence Gathering",
    "bio": "A composed female operative who teams up with Fang Heng and Zaka aboard the train bound for the Western District Federation recruitment center.",
    "mentions": 140,
    "chapters": 45,
    "first_ch": 2809,
    "last_ch": 2964,
    "peak_ch": 2826
  },
  {
    "rank": 133,
    "name": "Brent",
    "first_name": "Brent",
    "last_name": "Brent",
    "aliases": "Lord Brent",
    "tier": "Supporting Character",
    "faction": "Enkama Empire / Royal Family",
    "role": "Leader of the Imperial Feudal Lords Coalition",
    "arc": "Enkama Empire Feudal Politics Arc (Ch. 1106–1330)",
    "abilities": "Noble Coalition Leadership, Political Pressure",
    "bio": "A prominent feudal lord in the Enkama Empire who leads a delegation of lords suspicious of Fang Heng's necromancer identity.",
    "mentions": 140,
    "chapters": 28,
    "first_ch": 1106,
    "last_ch": 1330,
    "peak_ch": 1120
  },
  {
    "rank": 134,
    "name": "Dean",
    "first_name": "Dean",
    "last_name": "Dean",
    "aliases": "Great Sage Dean",
    "tier": "Supporting Character",
    "faction": "Holy Court / Purifiers",
    "role": "One of the Twelve Great Sages of the Holy Court",
    "arc": "Holy Court & Divine Realm Arc (Ch. 2783–3522)",
    "abilities": "Demigod/God-Tier Sacred Study, Holy Judgement",
    "bio": "A high-ranking Great Sage of the Holy Court involved in the late-game sacred trials and conflicts against Fang Heng.",
    "mentions": 136,
    "chapters": 19,
    "first_ch": 2783,
    "last_ch": 3522,
    "peak_ch": 3019
  },
  {
    "rank": 135,
    "name": "Wendy",
    "first_name": "Wendy",
    "last_name": "Wendy",
    "aliases": "NPC Wendy",
    "tier": "Supporting Character",
    "faction": "Prison 507 / Zombie Apocalypse",
    "role": "Key Ring-Mission Giver in District 8",
    "arc": "District 8 Hidden Storyline Arc (Ch. 309–1458)",
    "abilities": "Clue Provision, Storyline Triggers",
    "bio": "An important mission NPC in District 8 whose exclusive timed quest chain provides Fang Heng with critical early-to-mid game storyline clues.",
    "mentions": 135,
    "chapters": 22,
    "first_ch": 309,
    "last_ch": 1458,
    "peak_ch": 322
  },
  {
    "rank": 136,
    "name": "Yu Jie",
    "first_name": "Jie",
    "last_name": "Yu",
    "aliases": "Commander Yu Jie",
    "tier": "Supporting Character",
    "faction": "Federation",
    "role": "Main Person in Charge of the Regional Shelter",
    "arc": "District 8 / District 7 Shelter Defense Arc (Ch. 292–508)",
    "abilities": "Shelter Governance, Defensive Command",
    "bio": "A resolute shelter commander who manages survivor defenses during the escalating zombie waves.",
    "mentions": 134,
    "chapters": 30,
    "first_ch": 292,
    "last_ch": 508,
    "peak_ch": 317
  },
  {
    "rank": 137,
    "name": "Cole Karot",
    "first_name": "Cole",
    "last_name": "Karot",
    "aliases": "Prince Cole Karot",
    "tier": "Supporting Character",
    "faction": "Tree Spirit Tribe / World of Forests",
    "role": "Crown Prince of the Elves",
    "arc": "Elven & Flying Squirrel Alliance Arc (Ch. 3034–3162)",
    "abilities": "Royal Elven Magic, Nature & Elemental Mastery",
    "bio": "The noble Crown Prince and heir to the Elven throne who boards Captain Kapa's vessel and interacts with Fang Heng during the late-game dimensional alliance.",
    "mentions": 133,
    "chapters": 25,
    "first_ch": 3034,
    "last_ch": 3162,
    "peak_ch": 3058
  },
  {
    "rank": 138,
    "name": "Xiao Jing",
    "first_name": "Jing",
    "last_name": "Xiao",
    "aliases": "Player Xiao Jing",
    "tier": "Supporting Character",
    "faction": "Federation",
    "role": "Federation Frontline Marksman",
    "arc": "District 8 & District 7 Operations (Ch. 162–486)",
    "abilities": "Rifle Marksmanship, Squad Support",
    "bio": "A Federation player under Chen Yu's command who participates in early joint operations with Fang Heng.",
    "mentions": 133,
    "chapters": 20,
    "first_ch": 162,
    "last_ch": 486,
    "peak_ch": 482
  },
  {
    "rank": 139,
    "name": "Miguel",
    "first_name": "Miguel",
    "last_name": "Miguel",
    "aliases": "Captain Miguel",
    "tier": "Supporting Character",
    "faction": "God Clan / Tribunal of Sin",
    "role": "Secret Teleportation & Ambush Coordinator",
    "arc": "Late-Game Research Remains Arc (Ch. 3206–3232)",
    "abilities": "Spatial Transfer Logistics, Ambush Command",
    "bio": "An officer tasked with secretly transferring remains and setting up ambushes against intruders in the late-game arc.",
    "mentions": 133,
    "chapters": 19,
    "first_ch": 3206,
    "last_ch": 3232,
    "peak_ch": 3227
  },
  {
    "rank": 140,
    "name": "Qiu Xiaoling",
    "first_name": "Xiaoling",
    "last_name": "Qiu",
    "aliases": "Gluttony Seed Qiu Xiaoling",
    "tier": "Supporting Character",
    "faction": "Noel Clan / Occult Research",
    "role": "Host of the Demonic Seed of Gluttony",
    "arc": "Demonic Seeds Arena Arc (Ch. 2496–2780)",
    "abilities": "Gluttony Demonic Seed Power, Devouring Aura",
    "bio": "One of the awakened hosts of the Demonic Seed of Gluttony who introduces Fang Heng (disguised as Fang Bai) to the arena alongside Abulati.",
    "mentions": 132,
    "chapters": 25,
    "first_ch": 2496,
    "last_ch": 2780,
    "peak_ch": 2497
  },
  {
    "rank": 141,
    "name": "Alba",
    "first_name": "Alba",
    "last_name": "Alba",
    "aliases": "Commander Alba",
    "tier": "Supporting Character",
    "faction": "Federation",
    "role": "Commander of the Federation's Southwest Region",
    "arc": "Southwest Region & Primeval Forest Arc (Ch. 794–835)",
    "abilities": "Regional Administration, Identity Verification",
    "bio": "The Federation commander overseeing the Southwest region who monitors Fang Heng's rapid expansion.",
    "mentions": 132,
    "chapters": 15,
    "first_ch": 794,
    "last_ch": 835,
    "peak_ch": 823
  },
  {
    "rank": 142,
    "name": "Mu Qingxin",
    "first_name": "Mu",
    "last_name": "Qingxin",
    "aliases": "Overlord Mu Qingxin",
    "tier": "Supporting Character",
    "faction": "Netherworld / Death Realm / Evil Clan",
    "role": "Death Realm Territory Lord",
    "arc": "Death Realm & Disaster Fusion Arc (Ch. 2584–2996)",
    "abilities": "Death Realm Domain Control, Potential Unlocking",
    "bio": "A feared female territory lord in the Death Realm who partners with Proust to fuse Disaster and Death Realm powers.",
    "mentions": 129,
    "chapters": 26,
    "first_ch": 2584,
    "last_ch": 2996,
    "peak_ch": 2988
  },
  {
    "rank": 143,
    "name": "Qiu Hai",
    "first_name": "Hai",
    "last_name": "Qiu",
    "aliases": "Commander Qiu Hai",
    "tier": "Supporting Character",
    "faction": "Necromancer Association / Tower of Bones",
    "role": "Death Realm Camp Commander",
    "arc": "Death Realm Rift Arc (Ch. 943–1374)",
    "abilities": "Camp Defense, Undead Suppression",
    "bio": "A regional camp commander who investigates the massive magic array Fang Heng uses to siphon Death Realm aura.",
    "mentions": 127,
    "chapters": 18,
    "first_ch": 943,
    "last_ch": 1374,
    "peak_ch": 951
  },
  {
    "rank": 144,
    "name": "Vionne",
    "first_name": "Vionne",
    "last_name": "Vionne",
    "aliases": "Expert Vionne",
    "tier": "Supporting Character",
    "faction": "Federation",
    "role": "Special Expert from the Western Federation Presidential Office",
    "arc": "Mutant Cocoon Investigation Arc (Ch. 2947–2979)",
    "abilities": "Biological Inspection, Presidential Authority",
    "bio": "A smug special expert dispatched by the Presidential Office of the Western District Federation who butts heads with Collete during the cocoon crisis.",
    "mentions": 127,
    "chapters": 18,
    "first_ch": 2947,
    "last_ch": 2979,
    "peak_ch": 2958
  },
  {
    "rank": 145,
    "name": "Kou Ming",
    "first_name": "Ming",
    "last_name": "Kou",
    "aliases": "Player Kou Ming",
    "tier": "Supporting Character",
    "faction": "Necromancer Association / Tower of Bones",
    "role": "Tower of Bones Necromancer Recruit",
    "arc": "Tower of Bones Arc (Ch. 1394–1627)",
    "abilities": "Necromancy, Reconnaissance",
    "bio": "A necromancer player at the Tower of Bones who witnesses Fang Heng's shockingly fast progression to Level 30.",
    "mentions": 124,
    "chapters": 32,
    "first_ch": 1394,
    "last_ch": 1627,
    "peak_ch": 1425
  },
  {
    "rank": 146,
    "name": "Li Xue",
    "first_name": "Xue",
    "last_name": "Li",
    "aliases": "Coordinator Li Xue",
    "tier": "Supporting Character",
    "faction": "Enkama Empire / Royal Family",
    "role": "Offline Operations Coordinator",
    "arc": "Enkama Empire & Real-World Strategy Arc (Ch. 1238–1353)",
    "abilities": "Tactical Coordination, Offline Intelligence",
    "bio": "The capable coordinator in charge of offline strategy sessions who quickly grasps the brilliance of Fang Heng's battle plans.",
    "mentions": 123,
    "chapters": 45,
    "first_ch": 1238,
    "last_ch": 1353,
    "peak_ch": 1251
  },
  {
    "rank": 147,
    "name": "Hayez",
    "first_name": "Hayez",
    "last_name": "Hayez",
    "aliases": "Elder Hayez",
    "tier": "Supporting Character",
    "faction": "Vampire Clan",
    "role": "Elder of the Tremere Vampire Clan",
    "arc": "Vampire Clan Trial & Inheritance Arc (Ch. 842–1409)",
    "abilities": "Tremere Blood Magic, Clan Adjudication",
    "bio": "A senior elder of the Tremere vampire clan who presides over bloodline evaluations and praises Fang Heng's talent.",
    "mentions": 122,
    "chapters": 32,
    "first_ch": 842,
    "last_ch": 1409,
    "peak_ch": 844
  },
  {
    "rank": 148,
    "name": "Wu Xiao",
    "first_name": "Xiao",
    "last_name": "Wu",
    "aliases": "Leader Wu Xiao",
    "tier": "Supporting Character",
    "faction": "Federation",
    "role": "Mercenary Tough in the Western District",
    "arc": "Western District Recruitment Arc (Ch. 2828–2917)",
    "abilities": "Brawl & Intimidation, Squad Skirmishing",
    "bio": "An aggressive mercenary leader in the Western District who tries to intimidate Fang Heng's group before being surrounded and humbled.",
    "mentions": 122,
    "chapters": 17,
    "first_ch": 1257,
    "last_ch": 2917,
    "peak_ch": 2830
  },
  {
    "rank": 149,
    "name": "Zhang Zhe",
    "first_name": "Zhe",
    "last_name": "Zhang",
    "aliases": "Officer Zhang Zhe",
    "tier": "Supporting Character",
    "faction": "Federation",
    "role": "Federation Intelligence & Dossier Analyst",
    "arc": "District 8 Report Arc (Ch. 258–307)",
    "abilities": "Data Analysis, Strategic Assessment",
    "bio": "An overworked, dark-circled Federation analyst who reviews Chen Yu's increasingly unbelievable intelligence reports on Fang Heng.",
    "mentions": 120,
    "chapters": 20,
    "first_ch": 258,
    "last_ch": 307,
    "peak_ch": 293
  },
  {
    "rank": 150,
    "name": "Chen Li",
    "first_name": "Li",
    "last_name": "Chen",
    "aliases": "Bishop Chen Li",
    "tier": "Supporting Character",
    "faction": "Holy Court / Purifiers",
    "role": "Regional Bishop of the Holy Court",
    "arc": "District 7 / Holy Court Purge Arc (Ch. 678–727)",
    "abilities": "Bishop-Tier Holy Light, Inquisition Command",
    "bio": "A serious regional bishop who gathers high-ranking Holy Court officials to purge necromancers and vampires before running into Fang Heng.",
    "mentions": 120,
    "chapters": 17,
    "first_ch": 678,
    "last_ch": 727,
    "peak_ch": 715
  }
]


def calculate_zombies(max_level):
    """
    Calculates zombie counts for each level up to max_level.
    Preserves backward compatibility with zombiecalc.py while adding
    6h/12h/18h proliferator stages, unenhanced baseline comparison, and novel chapter notes.
    """
    results = []
    total_zombies = 0

    for level in range(1, max_level + 1):
        if level <= 10:
            gained = level
            total_zombies += gained
            prolif_6h = ""
            prolif_12h = ""
            proliferators_total = ""
        else:
            # Exact 20% ceiling: (total_zombies + 4) // 5 matches math.ceil(total_zombies * 1.2)
            new_total = math.ceil(total_zombies * 1.2)
            gained = new_total - total_zombies
            total_zombies = new_total
            prolif_6h = total_zombies * 2
            prolif_12h = total_zombies * 3
            proliferators_total = total_zombies * 4

        unenhanced_total = level * (level + 1) // 2
        ch_cite, ch_note = NOVEL_VERIFIED_LEVELS.get(level, ("", ""))

        results.append({
            "Level": level,
            "Zombies Gained": gained,
            "Total Zombies": total_zombies,
            "6h (+1 Prolif)": prolif_6h,
            "12h (+2 Prolif)": prolif_12h,
            "Total Zombies + Proliferators": proliferators_total,
            "Unenhanced S-Rank": unenhanced_total,
            "Novel Chapter": ch_cite,
            "Milestone Note": ch_note
        })
    return results


def print_table(results, extended=False):
    if extended:
        headers = [
            "Level", "Zombies Gained", "Total Zombies",
            "Total Zombies + Proliferators", "Unenhanced S-Rank", "Novel Chapter"
        ]
    else:
        headers = ["Level", "Zombies Gained", "Total Zombies", "Total Zombies + Proliferators"]

    formatted_rows = []
    for row in results:
        r_fmt = {}
        for h in headers:
            val = row[h]
            if isinstance(val, int):
                r_fmt[h] = f"{val:,}"
            else:
                r_fmt[h] = str(val)
        formatted_rows.append(r_fmt)

    col_widths = {header: len(header) for header in headers}
    for r_fmt in formatted_rows:
        for header in headers:
            col_widths[header] = max(col_widths[header], len(r_fmt[header]))

    fmt_str = "  ".join("{:<" + str(col_widths[header] + 2) + "}" for header in headers)
    header_row = fmt_str.format(*headers)
    print(header_row)
    print("-" * len(header_row))

    for r_fmt in formatted_rows:
        print(fmt_str.format(*(r_fmt[h] for h in headers)))


def calculate_abe_akaya(tree_level, prayer_temple_discount=True):
    """
    Calculates Sacred Tree Abe Akaya's maximum Dimensional Level and Vampire Clan attribute bonus
    based on Chapters 2280–3031.
    Formula: Max Dimensional Level = floor(Tree_Level / 10) + 1 (once Dimensional Form is unlocked at Lv 41+).
    """
    max_dim_level = (tree_level // 10) + 1
    if tree_level < 40:
        stage = "Sapling / Early Growth Stage (Blood & Filthy Form)"
    elif tree_level < 160:
        stage = "Mature Dimensional Form (Ch. 2281+)"
    elif tree_level < 277:
        stage = "High-Tier Dimensional Form (Complete Form Eligible at Lv 160+, Ch. 2332)"
    else:
        stage = "Complete Form — Tree of Hell (Seven Deadly Sins Fused, Ch. 3031+)"

    # Interpolated Vampire Clan attribute bonus schedule from Ch. 2290-2766
    dim_bonus_table = {
        1: 20, 2: 40, 3: 60, 5: 100, 8: 150, 11: 230, 16: 380, 24: 680, 27: 1480, 32: 2980
    }
    vampire_boost_pct = max_dim_level * 20 if max_dim_level <= 5 else int(max_dim_level ** 2 * 1.5)
    discount_mult = 0.88 if prayer_temple_discount else 1.0

    return {
        "tree_level": tree_level,
        "evolution_stage": stage,
        "max_dimensional_level": max_dim_level,
        "prayer_temple_discount": "12% Reduced Energy Cost (Active)" if prayer_temple_discount else "None",
        "estimated_vampire_attribute_boost_pct": f"+{vampire_boost_pct}%",
        "cost_multiplier": discount_mult
    }


def calculate_solidification_cost(num_clones, form_key):
    form = ZOMBIE_FORMS.get(form_key)
    if not form:
        raise ValueError(f"Unknown form key: {form_key}")
    totals = {res: amt * num_clones for res, amt in form["unit_cost"].items()}
    return {
        "form_name": form["name"],
        "num_clones": num_clones,
        "total_costs": totals,
        "notes": form["notes"]
    }


def query_characters(sort_by="mentions", search_query="", limit=50):
    filtered = CHARACTERS_DB
    if search_query:
        q = search_query.lower()
        filtered = [
            c for c in CHARACTERS_DB
            if q in c["name"].lower()
            or q in c["first_name"].lower()
            or q in c["last_name"].lower()
            or q in c["aliases"].lower()
            or q in c["faction"].lower()
            or q in c["role"].lower()
            or q in c["bio"].lower()
        ]

    if sort_by == "mentions":
        filtered = sorted(filtered, key=lambda x: (-x["mentions"], -x["chapters"]))
    elif sort_by == "chapters":
        filtered = sorted(filtered, key=lambda x: (-x["chapters"], -x["mentions"]))
    elif sort_by == "first":
        filtered = sorted(filtered, key=lambda x: (x["first_name"].lower(), -x["mentions"]))
    elif sort_by == "last":
        filtered = sorted(filtered, key=lambda x: (x["last_name"].lower(), x["first_name"].lower(), -x["mentions"]))
    elif sort_by == "full":
        filtered = sorted(filtered, key=lambda x: (x["name"].lower(), -x["mentions"]))
    elif sort_by == "debut":
        filtered = sorted(filtered, key=lambda x: (x["first_ch"], -x["mentions"]))

    return filtered[:limit]


def print_character_table(chars):
    headers = ["Rank", "Name", "First/Given", "Last/Family", "Mentions", "Chapters", "Span", "Faction", "Role"]
    rows = []
    for c in chars:
        rows.append({
            "Rank": f"#{c['rank']}",
            "Name": c["name"],
            "First/Given": c["first_name"],
            "Last/Family": c["last_name"],
            "Mentions": f"{c['mentions']:,}",
            "Chapters": f"{c['chapters']:,}",
            "Span": f"Ch.{c['first_ch']}-{c['last_ch']}",
            "Faction": c["faction"][:26],
            "Role": c["role"][:34]
        })
    if not rows:
        print("No matching characters found.")
        return
    widths = {h: max(len(h), max(len(r[h]) for r in rows)) for h in headers}
    fmt = "  ".join("{:<" + str(widths[h]) + "}" for h in headers)
    hdr = fmt.format(*headers)
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(fmt.format(*(r[h] for h in headers)))


def interactive_menu():
    while True:
        print("\n" + "=" * 72)
        print("  GLOBAL GAME: AFK IN THE ZOMBIE APOCALYPSE GAME — STAT & WIKI SUITE")
        print("=" * 72)
        print("  1. Zombie Clone & Proliferator Table (Lv 1 to N)")
        print("  2. Inspect Specific Player Level (Clones, Proliferators & Lore Note)")
        print("  3. Zombie Form Solidification & Mutation Cost Calculator")
        print("  4. Sacred Tree Abe Akaya Dimensional Calculator")
        print("  5. Character Wiki Index (Sort by Mentions / First Name / Last Name / Debut)")
        print("  6. Search Character Dossier by Name or Faction")
        print("  7. Export Zombie Table & Character Wiki to CSV")
        print("  0. Exit")
        choice = input("\nSelect an option (0-7): ").strip()

        if choice == "0":
            break
        elif choice == "1":
            val = input("Enter maximum level [default 70]: ").strip()
            max_lv = int(val) if val.isdigit() and int(val) > 0 else 70
            res = calculate_zombies(max_lv)
            print_table(res, extended=True)
        elif choice == "2":
            val = input("Enter Fang Heng's character level (1-150): ").strip()
            lv = int(val) if val.isdigit() and int(val) > 0 else 40
            row = calculate_zombies(lv)[-1]
            print(f"\n--- Level {lv} Zombie Army Breakdown ---")
            print(f"  Zombies Gained at Lv {lv}:       +{row['Zombies Gained']:,}")
            print(f"  Total Base Zombie Clones:      {row['Total Zombies']:,}")
            if lv >= 11:
                print(f"  After 6h  (+1 Proliferator):   {row['6h (+1 Prolif)']:,}")
                print(f"  After 12h (+2 Proliferators):  {row['12h (+2 Prolif)']:,}")
                print(f"  After 18h (+3 Proliferators):  {row['Total Zombies + Proliferators']:,} (Full 4x Army)")
            print(f"  Unenhanced S-Rank Baseline:    {row['Unenhanced S-Rank']:,}")
            if row["Novel Chapter"]:
                print(f"  Novel Verification:            [{row['Novel Chapter']}] {row['Milestone Note']}")
        elif choice == "3":
            print("\nAvailable Zombie Modifications:")
            keys = list(ZOMBIE_FORMS.keys())
            for idx, k in enumerate(keys, 1):
                print(f"  {idx}. {ZOMBIE_FORMS[k]['name']}")
            f_idx = input("Choose form (1-7) [default 1]: ").strip()
            k = keys[int(f_idx) - 1] if f_idx.isdigit() and 1 <= int(f_idx) <= len(keys) else keys[0]
            c_str = input("Enter number of zombie clones to solidify [default 13548]: ").strip()
            n_clones = int(c_str) if c_str.isdigit() else 13548
            res = calculate_solidification_cost(n_clones, k)
            print(f"\n--- {res['form_name']} ({n_clones:,} Clones) ---")
            for resource, amount in res["total_costs"].items():
                print(f"  {resource}: {amount:,}")
            print(f"  Notes: {res['notes']}")
        elif choice == "4":
            t_str = input("Enter Sacred Tree Abe Akaya's Level [default 148]: ").strip()
            t_lv = int(t_str) if t_str.isdigit() else 148
            info = calculate_abe_akaya(t_lv)
            print(f"\n--- Sacred Tree Abe Akaya (Level {t_lv}) ---")
            for k, v in info.items():
                print(f"  {k}: {v}")
        elif choice == "5":
            s_mode = input("Sort by [mentions / chapters / first / last / full / debut] (default: mentions): ").strip().lower() or "mentions"
            lim_str = input("How many characters to display (1-150) [default 50]: ").strip()
            lim = int(lim_str) if lim_str.isdigit() else 50
            chars = query_characters(sort_by=s_mode, limit=lim)
            print_character_table(chars)
        elif choice == "6":
            q = input("Enter character name, faction, or keyword: ").strip()
            matches = query_characters(search_query=q, limit=10)
            for c in matches:
                print(f"\n[#{c['rank']}] {c['name']} (First: {c['first_name']} | Last: {c['last_name']})")
                print(f"  Aliases:   {c['aliases']}")
                print(f"  Tier/Role: {c['tier']} — {c['role']} ({c['faction']})")
                print(f"  Mentions:  {c['mentions']:,} mentions across {c['chapters']:,} chapters (Ch.{c['first_ch']}–{c['last_ch']}, Peak: Ch.{c['peak_ch']})")
                print(f"  Abilities: {c['abilities']}")
                print(f"  Profile:   {c['bio']}")
        elif choice == "7":
            z_rows = calculate_zombies(100)
            with open("zombie_levels_1_to_100.csv", "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=list(z_rows[0].keys()))
                w.writeheader()
                w.writerows(z_rows)
            with open("novel_characters_top_150.csv", "w", newline="", encoding="utf-8") as f:
                w = csv.DictWriter(f, fieldnames=list(CHARACTERS_DB[0].keys()))
                w.writeheader()
                w.writerows(CHARACTERS_DB)
            print("Exported 'zombie_levels_1_to_100.csv' and 'novel_characters_top_150.csv'!")


def main():
    parser = argparse.ArgumentParser(description="Global Game: AFK In The Zombie Apocalypse Game — Stat & Wiki Tracker")
    parser.add_argument("--max-level", type=int, help="Print Zombie Clone table up to MAX_LEVEL (e.g. 70)")
    parser.add_argument("--level", type=int, help="Inspect a single character level (e.g. 40 or 63)")
    parser.add_argument("--extended", action="store_true", help="Include novel chapter verification columns in zombie table")
    parser.add_argument("--wiki", action="store_true", help="Print the Character Wiki Index table")
    parser.add_argument("--sort", choices=["mentions", "chapters", "first", "last", "full", "debut"], default="mentions", help="Sort order for Character Wiki Index")
    parser.add_argument("--search", type=str, default="", help="Search character wiki by name, faction, or role")
    parser.add_argument("--limit", type=int, default=50, help="Number of characters to display in Wiki Index")
    parser.add_argument("--abe-level", type=int, help="Calculate Sacred Tree Abe Akaya stats at a given tree level")
    parser.add_argument("--interactive", action="store_true", help="Launch interactive terminal menu")

    args = parser.parse_args()

    if args.interactive:
        interactive_menu()
        return

    if args.level:
        row = calculate_zombies(args.level)[-1]
        print(json.dumps(row, indent=2))
        return

    if args.abe_level:
        print(json.dumps(calculate_abe_akaya(args.abe_level), indent=2))
        return

    if args.wiki or args.search:
        chars = query_characters(sort_by=args.sort, search_query=args.search, limit=args.limit)
        print_character_table(chars)
        return

    # Default behavior matches original zombiecalc.py (prints Lv 1-70 table)
    max_lv = args.max_level if args.max_level else 70
    results = calculate_zombies(max_lv)
    print_table(results, extended=args.extended)


if __name__ == "__main__":
    main()
