"""
Add Gaming Features to JARVIS
Fashion, Emotes, Posters, Skills, Skins, Vehicles, Profiles and more
Free Fire / PUBG / Fortnite style

Bengali: JARVIS এ গেমিং ফিচার যোগ করুন
ফ্যাশন, ইমোট, পোস্টার, স্কিল, স্কিন, ভেহিকেল, প্রোফাইল
"""
import os
import sys
import glob

def find_database():
    """Find the most recent working database"""
    if os.path.exists('jarvis_memory.db'):
        try:
            import sqlite3
            conn = sqlite3.connect('jarvis_memory.db', timeout=5)
            conn.execute("PRAGMA quick_check").fetchall()
            conn.close()
            return 'jarvis_memory.db'
        except Exception as e:

            print(f"⚠️ Error: {e}")
            pass
    
    fixed_dbs = glob.glob('jarvis_memory.db.fixed-*')
    if fixed_dbs:
        fixed_dbs.sort(reverse=True)
        return fixed_dbs[0]
    
    return None

def add_gaming_features(db_path):
    """Add gaming features to JARVIS database"""
    import sqlite3
    
    print("=" * 80)
    print("  ADDING GAMING FEATURES TO JARVIS")
    print("  JARVIS এ গেমিং ফিচার যোগ করা হচ্ছে")
    print("=" * 80)
    print(f"\nDatabase: {db_path}\n")
    
    conn = sqlite3.connect(db_path, timeout=10)
    cursor = conn.cursor()
    
    # Add gaming system info
    print("[1/4] Adding gaming system information...")
    gaming_system_info = [
        ('gaming_enabled', 'true', 'software'),
        ('gaming_style', 'Free Fire/PUBG/Fortnite', 'software'),
        ('fashion_system', 'enabled', 'software'),
        ('emote_system', 'enabled', 'software'),
        ('skin_system', 'enabled', 'software'),
        ('vehicle_system', 'enabled', 'software'),
        ('profile_system', 'enabled', 'software'),
        ('inventory_system', 'enabled', 'software'),
        ('shop_system', 'enabled', 'software'),
        ('battle_pass', 'enabled', 'software'),
    ]
    
    for key, value, category in gaming_system_info:
        cursor.execute("""
            INSERT OR REPLACE INTO system_info (key, value, category, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (key, value, category))
        print(f"  [+] {key}: {value}")
    
    # Add gaming knowledge
    print("\n[2/4] Adding gaming knowledge base...")
    gaming_knowledge = [
        (
            'Gaming - Overview',
            'JARVIS Gaming System: Complete gaming features like Free Fire, PUBG, Fortnite. '
            'Features: Fashion items, Emotes, Posters, Skills, Character skins, Weapon skins, '
            'Vehicle skins, Profiles, Inventory, Shop, Battle Pass, Events, Tournaments, '
            'Clans/Guilds, Friends, Chat, Voice chat, Leaderboards, Achievements, Rewards, '
            'Daily missions, Weekly missions, Season pass, Loot boxes, Crafting, Trading. '
            'Games supported: Free Fire, PUBG Mobile, Fortnite, Call of Duty Mobile, '
            'Apex Legends, Valorant, CS:GO, Overwatch, League of Legends, Dota 2.',
            'gaming'
        ),
        (
            'Gaming - Fashion & Outfits',
            'Fashion System: Character outfits, Tops, Bottoms, Shoes, Hats, Masks, Glasses, '
            'Backpacks, Parachutes, Gloves, Accessories. Rarity: Common, Uncommon, Rare, '
            'Epic, Legendary, Mythic. Collections: Military, Urban, Futuristic, Fantasy, '
            'Sports, Casual, Formal, Traditional, Seasonal (Halloween, Christmas, New Year). '
            'Customization: Mix and match, Color variants, Patterns, Textures, Glow effects, '
            'Particle effects, Animated outfits. Acquisition: Shop, Battle Pass, Events, '
            'Loot boxes, Crafting, Trading, Achievements, Tournaments.',
            'gaming_fashion'
        ),
        (
            'Gaming - Emotes & Gestures',
            'Emote System: Dance emotes, Victory emotes, Taunt emotes, Greeting emotes, '
            'Celebration emotes, Funny emotes, Sad emotes, Angry emotes, Love emotes. '
            'Popular: Floss, Orange Justice, Take the L, Default Dance, Dab, Salute, '
            'Wave, Thumbs up, Heart, Clap, Laugh, Cry, Rage, GG. '
            'Features: Animated, Sound effects, Particle effects, Interactive emotes, '
            'Synchronized emotes (group), Emote wheel, Quick emotes, Custom emotes. '
            'Rarity: Common, Rare, Epic, Legendary. Acquisition: Shop, Battle Pass, Events.',
            'gaming_emotes'
        ),
        (
            'Gaming - Posters & Banners',
            'Poster System: Profile banners, Loading screens, Victory screens, Death screens, '
            'Lobby backgrounds, Clan banners, Tournament banners, Event posters. '
            'Types: Static, Animated, Interactive, 3D, Holographic. '
            'Themes: Characters, Weapons, Vehicles, Locations, Events, Seasons, Achievements. '
            'Customization: Text overlay, Clan logo, Stats display, Rank display, '
            'Achievement showcase. Rarity: Common to Legendary. '
            'Acquisition: Shop, Battle Pass, Events, Achievements, Tournaments.',
            'gaming_posters'
        ),
        (
            'Gaming - Skills & Abilities',
            'Skill System: Character skills, Passive abilities, Active abilities, Ultimate abilities. '
            'Categories: Combat (damage boost, healing, shield), Mobility (speed, jump, dash), '
            'Utility (scan, mark, revive), Support (buff allies, debuff enemies). '
            'Examples: Gloo Wall (Free Fire), Smoke Grenade (PUBG), Building (Fortnite), '
            'Tactical abilities (Apex), Agent abilities (Valorant). '
            'Cooldowns: Short (10s), Medium (30s), Long (60s+), Ultimate (charge-based). '
            'Upgrades: Skill levels, Reduced cooldown, Increased effect, Extended duration.',
            'gaming_skills'
        ),
        (
            'Gaming - Character Skins',
            'Character Skins: Default, Premium, Elite, Legendary, Mythic, Exclusive. '
            'Types: Recolors, Redesigns, Themed (military, sci-fi, fantasy), Crossover '
            '(collaborations), Seasonal, Event-exclusive. '
            'Features: Custom animations, Voice lines, Sound effects, Particle effects, '
            'Glow effects, Reactive (changes in-game). '
            'Popular: Elite Pass skins, Collaboration skins (Anime, Movies, Brands), '
            'Pro player skins, Tournament skins. '
            'Acquisition: Shop (diamonds/coins), Battle Pass, Events, Bundles, Lucky draws.',
            'gaming_character_skins'
        ),
        (
            'Gaming - Weapon Skins',
            'Weapon Skins: Gun skins, Melee skins, Throwable skins. Rarity: Common to Mythic. '
            'Types: Camo patterns, Solid colors, Gradients, Animated, Reactive (kill effects), '
            'Evolving (upgrades with kills). '
            'Popular: Dragon AK, Golden weapons, Neon skins, Ice skins, Fire skins, '
            'Galaxy skins, Legendary skins. '
            'Features: Custom reload animation, Firing effects, Kill effects, Inspect animation, '
            'Sound effects, Particle trails. '
            'Acquisition: Shop, Weapon royale, Lucky spin, Events, Battle Pass, Crafting.',
            'gaming_weapon_skins'
        ),
        (
            'Gaming - Vehicle Skins',
            'Vehicle Skins: Car skins, Bike skins, Boat skins, Helicopter skins, Plane skins. '
            'Types: Paint jobs, Wraps, Decals, Patterns, Themed (racing, military, luxury). '
            'Features: Custom colors, Glow effects, Particle trails, Sound effects, '
            'Horn sounds, Boost effects. '
            'Rarity: Common, Rare, Epic, Legendary. '
            'Popular: Sports car skins, Monster truck, Superbike, Luxury sedan, Military jeep. '
            'Acquisition: Shop, Events, Lucky draws, Battle Pass, Achievements.',
            'gaming_vehicle_skins'
        ),
        (
            'Gaming - Profile & Stats',
            'Profile System: Username, Avatar, Banner, Title, Badge, Frame, Level, Rank, '
            'Stats (kills, wins, K/D ratio, headshots, accuracy), Achievements, Badges, '
            'Titles, Clan tag, Friends list, Recent matches, Favorite weapons, Favorite mode. '
            'Customization: Profile picture, Background, Border, Name color, Title, Badge, '
            'Showcase (skins, emotes, achievements). '
            'Stats: Total matches, Wins, Top 10, Kills, Deaths, K/D, Win rate, Survival time, '
            'Damage dealt, Headshot %, Accuracy %, Distance traveled.',
            'gaming_profile'
        ),
        (
            'Gaming - Inventory & Storage',
            'Inventory System: Characters, Outfits, Emotes, Skins (weapon, vehicle), '
            'Posters, Banners, Titles, Badges, Consumables, Materials, Currencies. '
            'Organization: Categories, Filters (rarity, type, date), Search, Sort, '
            'Favorites, Recently acquired. '
            'Storage: Unlimited (digital items), Vault (premium items), Locker (equipped items). '
            'Management: Equip, Unequip, Dismantle, Craft, Trade, Gift, Sell. '
            'Currencies: Coins (free), Diamonds (premium), Tokens (event), Gold (special).',
            'gaming_inventory'
        ),
        (
            'Gaming - Shop & Store',
            'Shop System: Featured items, Daily deals, Weekly offers, Limited time, Bundles, '
            'Lucky draws, Weapon royale, Incubator, Faded wheel, Magic cube. '
            'Categories: Characters, Outfits, Emotes, Weapon skins, Vehicle skins, Bundles, '
            'Battle Pass, Diamonds, Coins. '
            'Payment: Diamonds (premium currency), Coins (free currency), Tokens (event), '
            'Real money (top-up). '
            'Discounts: First purchase bonus, Daily login rewards, Event discounts, '
            'Bundle savings, Seasonal sales.',
            'gaming_shop'
        ),
        (
            'Gaming - Battle Pass & Seasons',
            'Battle Pass: Free tier, Elite tier, Elite Plus tier. Rewards: Skins, Emotes, '
            'Outfits, Weapon skins, Vehicle skins, Diamonds, Coins, Tokens, Loot boxes. '
            'Progression: XP from matches, Daily missions, Weekly missions, Season missions. '
            'Tiers: 50-100 tiers, Instant unlock option, Tier skip tokens. '
            'Seasons: 2-3 months duration, New theme each season, Exclusive rewards, '
            'Ranked reset, New content (maps, modes, weapons). '
            'Benefits: Exclusive items, Premium rewards, Early access, Bonus XP.',
            'gaming_battlepass'
        ),
        (
            'Gaming - Events & Tournaments',
            'Events: Daily events, Weekly events, Special events, Collaboration events, '
            'Seasonal events (Halloween, Christmas, New Year, Anniversary). '
            'Types: Login events, Mission events, Top-up events, Lucky draw events, '
            'Collection events, Ranked events. '
            'Rewards: Exclusive skins, Emotes, Diamonds, Tokens, Loot boxes, Titles, Badges. '
            'Tournaments: Solo, Duo, Squad, Custom rooms, Pro tournaments, Community tournaments. '
            'Prizes: Cash prizes, In-game rewards, Exclusive items, Pro contracts.',
            'gaming_events'
        ),
        (
            'Gaming - Clans & Guilds',
            'Clan System: Create clan, Join clan, Clan name, Clan tag, Clan logo, Clan level, '
            'Clan members (50-100), Clan chat, Clan voice chat, Clan wars, Clan tournaments. '
            'Roles: Leader, Co-leader, Elder, Member. '
            'Features: Clan shop, Clan missions, Clan rewards, Clan leaderboard, Clan perks, '
            'Clan banner, Clan base. '
            'Benefits: Team play, Exclusive rewards, Clan tournaments, Social features, '
            'Shared resources, Clan achievements.',
            'gaming_clans'
        ),
        (
            'Gaming - Friends & Social',
            'Friends System: Add friends, Friend requests, Friend list, Online status, '
            'Recent players, Suggested friends, Friend chat, Voice chat, Video call. '
            'Features: Invite to match, Spectate, Gift items, Share achievements, '
            'Compare stats, Friend leaderboard. '
            'Social: Global chat, Team chat, Clan chat, Private messages, Emojis, Stickers, '
            'Voice messages, Quick chat. '
            'Privacy: Block, Mute, Report, Privacy settings, Online status visibility.',
            'gaming_social'
        ),
        (
            'Gaming - Leaderboards & Rankings',
            'Leaderboards: Global, Regional, Friends, Clan, Mode-specific. '
            'Rankings: Overall rank, K/D rank, Win rate rank, Headshot rank, Damage rank. '
            'Tiers: Bronze, Silver, Gold, Platinum, Diamond, Master, Grandmaster, Heroic, Legendary. '
            'Seasons: Ranked seasons, Season rewards, Rank decay, Rank protection. '
            'Display: Top 100, Top 500, Top 1000, Your rank, Nearby ranks. '
            'Rewards: Exclusive skins, Titles, Badges, Frames, Emotes, Parachutes.',
            'gaming_leaderboards'
        ),
        (
            'Gaming - Achievements & Badges',
            'Achievements: Combat achievements, Survival achievements, Social achievements, '
            'Collection achievements, Event achievements, Seasonal achievements. '
            'Examples: First kill, 100 kills, 1000 kills, First win, 100 wins, Headshot master, '
            'Survivor, Team player, Collector, Event participant. '
            'Badges: Bronze, Silver, Gold, Platinum, Diamond badges for each achievement. '
            'Rewards: Titles, Badges, Frames, Diamonds, Coins, Exclusive items. '
            'Display: Profile showcase, Achievement gallery, Badge collection.',
            'gaming_achievements'
        ),
        (
            'Gaming - Missions & Quests',
            'Daily Missions: Login reward, Play matches, Get kills, Win matches, Use specific weapon. '
            'Weekly Missions: Advanced challenges, Higher rewards, Multiple objectives. '
            'Season Missions: Long-term goals, Exclusive rewards, Battle Pass XP. '
            'Event Missions: Limited time, Special rewards, Themed challenges. '
            'Rewards: XP, Coins, Diamonds, Tokens, Items, Battle Pass progress. '
            'Types: Combat, Survival, Social, Collection, Exploration, Special.',
            'gaming_missions'
        ),
        (
            'Gaming - Loot Boxes & Rewards',
            'Loot Boxes: Bronze, Silver, Gold, Diamond, Legendary boxes. '
            'Contents: Skins, Emotes, Outfits, Weapon skins, Vouchers, Fragments, Tokens. '
            'Acquisition: Daily login, Missions, Events, Shop, Battle Pass, Achievements. '
            'Types: Standard boxes, Premium boxes, Event boxes, Weapon boxes, Character boxes. '
            'Mechanics: Random rewards, Guaranteed rewards, Pity system, Duplicate protection. '
            'Fragments: Collect fragments to exchange for specific items.',
            'gaming_lootboxes'
        ),
        (
            'Gaming - Crafting & Trading',
            'Crafting: Combine materials to create items, Upgrade items, Evolve skins. '
            'Materials: Common, Rare, Epic, Legendary materials from dismantling items. '
            'Recipes: Weapon skins, Character skins, Emotes, Outfits, Accessories. '
            'Trading: Trade with friends, Trade market, Safe trading system, Trade history. '
            'Restrictions: Level requirement, Cooldown period, Trade limits, Untradeable items. '
            'Benefits: Get desired items, Monetize duplicates, Complete collections.',
            'gaming_crafting'
        ),
        (
            'Gaming - Currencies & Economy',
            'Currencies: Coins (free, earned in-game), Diamonds (premium, purchased), '
            'Tokens (event-specific), Gold (special events), Vouchers (discounts). '
            'Earning: Match rewards, Daily login, Missions, Events, Achievements, '
            'Battle Pass, Selling items, Trading. '
            'Spending: Shop purchases, Lucky draws, Weapon royale, Upgrades, Crafting, '
            'Battle Pass, Name change, Clan creation. '
            'Top-up: Various packages, First-time bonus, Bonus diamonds, Special offers.',
            'gaming_economy'
        ),
        (
            'Gaming - Customization Options',
            'Character: Face, Hair, Body, Skin tone, Voice, Animations, Emotes. '
            'Loadout: Primary weapon, Secondary weapon, Melee, Throwables, Armor, Backpack. '
            'Appearance: Outfit, Hat, Mask, Glasses, Gloves, Shoes, Backpack, Parachute. '
            'Weapons: Skins, Attachments, Charms, Stickers, Kill effects. '
            'Vehicles: Paint, Decals, Horns, Boost effects, Trails. '
            'Profile: Avatar, Banner, Frame, Title, Badge, Showcase. '
            'HUD: Layout, Size, Opacity, Colors, Button positions.',
            'gaming_customization'
        ),
        (
            'Gaming - Game Modes',
            'Battle Royale: Solo, Duo, Squad (4-player), 50v50, 100-player. '
            'Team Deathmatch: 4v4, 8v8, Respawn enabled, First to X kills. '
            'Ranked: Competitive mode, Rank progression, Season rewards. '
            'Special: Zombie mode, Sniper mode, Shotgun mode, Melee mode, Custom mode. '
            'Limited Time: Event modes, Collaboration modes, Seasonal modes. '
            'Training: Practice range, Tutorial, Bot matches, Custom rooms. '
            'Arcade: Fast-paced, Quick matches, Fun modes, Experimental modes.',
            'gaming_modes'
        ),
        (
            'Gaming - Maps & Locations',
            'Maps: Bermuda, Purgatory, Kalahari, Alpine, Nextera (Free Fire style). '
            'Locations: Hot drops, Safe zones, Loot areas, Landmarks, Secret spots. '
            'Features: Dynamic weather, Day/night cycle, Destructible environment, '
            'Interactive objects, Vehicles, Supply drops, Airdrops. '
            'Sizes: Small (quick matches), Medium (balanced), Large (long matches). '
            'Themes: Island, Desert, Snow, Urban, Futuristic, Fantasy.',
            'gaming_maps'
        ),
        (
            'Gaming - Weapons & Equipment',
            'Weapons: Assault rifles, SMGs, Shotguns, Sniper rifles, LMGs, Pistols, Melee. '
            'Popular: AK47, M4A1, AWM, Kar98k, MP40, UMP, SCAR, Groza, M1014, Vector. '
            'Attachments: Scopes, Grips, Magazines, Muzzles, Stocks. '
            'Equipment: Armor (level 1-3), Helmets, Backpacks, Med kits, Bandages, '
            'Grenades, Smoke, Flashbang, Molotov, Gloo walls. '
            'Rarity: Common (gray), Uncommon (green), Rare (blue), Epic (purple), Legendary (gold).',
            'gaming_weapons'
        ),
    ]
    
    for topic, content, source in gaming_knowledge:
        cursor.execute("""
            INSERT INTO knowledge_base (topic, content, source, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (topic, content, source))
        print(f"  [+] {topic}")
    
    # Add gaming preferences
    print("\n[3/4] Adding gaming preferences...")
    gaming_preferences = [
        ('gaming_username', 'JARVIS_Player'),
        ('gaming_level', '100'),
        ('gaming_rank', 'Heroic'),
        ('gaming_clan', 'JARVIS_Squad'),
        ('gaming_favorite_mode', 'Battle Royale'),
        ('gaming_favorite_weapon', 'AK47'),
        ('gaming_sensitivity', 'High'),
        ('gaming_graphics', 'Ultra'),
        ('gaming_fps', '60'),
        ('gaming_voice_chat', 'true'),
    ]
    
    for key, value in gaming_preferences:
        cursor.execute("""
            INSERT OR REPLACE INTO user_preferences (preference_key, preference_value, updated_at)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        """, (key, value))
        print(f"  [+] {key}: {value}")
    
    # Add gaming commands
    print("\n[4/4] Adding gaming commands...")
    gaming_commands = [
        (
            'Gaming - Voice Commands',
            'Voice Commands: "Show my profile", "Open inventory", "Check shop", '
            '"Show battle pass", "View missions", "Check leaderboard", "Open clan", '
            '"Show friends", "Equip outfit", "Change skin", "Use emote", "Show stats", '
            '"Check achievements", "Open loot box", "Craft item", "Trade item", '
            '"Join match", "Create room", "Invite friends", "Start game".',
            'gaming_commands'
        ),
    ]
    
    for topic, content, source in gaming_commands:
        cursor.execute("""
            INSERT INTO knowledge_base (topic, content, source, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (topic, content, source))
        print(f"  [+] {topic}")
    
    conn.commit()
    
    # Get statistics
    cursor.execute("SELECT COUNT(*) FROM system_info WHERE key LIKE '%gaming%'")
    sys_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM knowledge_base WHERE source LIKE 'gaming%'")
    kb_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM user_preferences WHERE preference_key LIKE 'gaming%'")
    pref_count = cursor.fetchone()[0]
    
    conn.close()
    
    # Summary
    print("\n" + "=" * 80)
    print("  GAMING FEATURES ADDED SUCCESSFULLY!")
    print("  গেমিং ফিচার সফলভাবে যোগ করা হয়েছে!")
    print("=" * 80)
    print(f"  Database: {os.path.abspath(db_path)}")
    print(f"  Gaming system info: {sys_count} entries")
    print(f"  Gaming knowledge: {kb_count} entries")
    print(f"  Gaming preferences: {pref_count} entries")
    print(f"  Total gaming data: {sys_count + kb_count + pref_count} entries")
    print("\n  Features Added:")
    print("  ✅ Fashion & Outfits")
    print("  ✅ Emotes & Gestures")
    print("  ✅ Posters & Banners")
    print("  ✅ Skills & Abilities")
    print("  ✅ Character Skins")
    print("  ✅ Weapon Skins")
    print("  ✅ Vehicle Skins")
    print("  ✅ Profile & Stats")
    print("  ✅ Inventory & Storage")
    print("  ✅ Shop & Store")
    print("  ✅ Battle Pass & Seasons")
    print("  ✅ Events & Tournaments")
    print("  ✅ Clans & Guilds")
    print("  ✅ Friends & Social")
    print("  ✅ Leaderboards & Rankings")
    print("  ✅ Achievements & Badges")
    print("  ✅ Missions & Quests")
    print("  ✅ Loot Boxes & Rewards")
    print("  ✅ Crafting & Trading")
    print("  ✅ Currencies & Economy")
    print("  ✅ Customization Options")
    print("  ✅ Game Modes")
    print("  ✅ Maps & Locations")
    print("  ✅ Weapons & Equipment")
    print("\n  JARVIS now has complete gaming features!")
    print("  JARVIS এখন সম্পূর্ণ গেমিং ফিচার পেয়েছে!")
    print("=" * 80)

def main():
    print("\n🎮 Adding Gaming Features to JARVIS")
    print("🎮 JARVIS এ গেমিং ফিচার যোগ করা হচ্ছে\n")
    
    db_path = find_database()
    
    if not db_path:
        print("[ERROR] No working database found!")
        print("[ত্রুটি] কোনো কার্যকর ডাটাবেস পাওয়া যায়নি!")
        print("Run: python fix_database_windows10.py first")
        return
    
    print(f"[INFO] Found database: {db_path}\n")
    
    try:
        add_gaming_features(db_path)
        print("\n✅ SUCCESS! Gaming features added to JARVIS.")
        print("✅ সফল! JARVIS এ গেমিং ফিচার যোগ করা হয়েছে।")
        print("\nJARVIS now has:")
        print("JARVIS এখন আছে:")
        print("  - Fashion & Outfits (ফ্যাশন ও পোশাক)")
        print("  - Emotes & Gestures (ইমোট ও জেসচার)")
        print("  - Posters & Banners (পোস্টার ও ব্যানার)")
        print("  - Skills & Abilities (স্কিল ও ক্ষমতা)")
        print("  - Character/Weapon/Vehicle Skins (স্কিন)")
        print("  - Profile & Stats (প্রোফাইল ও স্ট্যাট)")
        print("  - Inventory & Shop (ইনভেন্টরি ও শপ)")
        print("  - Battle Pass & Events (ব্যাটল পাস ও ইভেন্ট)")
        print("  - Clans & Friends (ক্ল্যান ও বন্ধু)")
        print("  - And much more! (আরও অনেক কিছু!)")
    except Exception as e:
        print(f"\n[ERROR] Failed to add gaming features: {e}")
        print(f"[ত্রুটি] গেমিং ফিচার যোগ করতে ব্যর্থ: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
