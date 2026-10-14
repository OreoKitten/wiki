# 📚 OreoKitten's Wiki Hub — Novel & Software Compendium

Welcome to the central repository for my personal collection of **self-made, Gemini-generated, and Claude-generated wikis, encyclopedias, and interactive stat trackers** for web novels and software tools.

🌐 **Live Hub Website:**
- **GitHub Pages:** [https://oreokitten.github.io/wiki/](https://www.google.com/search?q=https%3A%2F%2Foreokitten.github.io%2Fwiki%2F)
- **Cloudflare Pages:** Configurable via zero-build static deployment from the `main` branch
- **Source Repository:** [https://github.com/OreoKitten/wiki](https://www.google.com/search?q=https%3A%2F%2Fgithub.com%2FOreoKitten%2Fwiki)

## 🗂️ Master Wiki & Subfolder Directory

Each novel or software project lives in its own dedicated subfolder at the root of this repository.

| Code / Subfolder | Title & Subject | Category | Built With | Interactive Web App (`.html`) | Markdown Wiki (`.md`) | Calculators & Scripts (`.py`) | Key Highlights |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **`AITZA/`** | **Global Game: AFK In The Zombie Apocalypse Game** *(by Empire Black Knight)* | 📚 Novel Wiki & Tracker | ✨ Gemini / Self-Made | [Launch Web App](https://www.google.com/search?q=.%2FAITZA%2Findex.html) *(or [global\_game\_wiki\_and\_tracker.html](https://www.google.com/search?q=.%2FAITZA%2Fglobal_game_wiki_and_tracker.html))* | [Read Wiki](https://www.google.com/search?q=.%2FAITZA%2FREADME.md) *(or [global\_game\_character\_wiki.md](https://www.google.com/search?q=.%2FAITZA%2Fglobal_game_character_wiki.md))* | [global\_game\_tracker.py](https://www.google.com/search?q=.%2FAITZA%2Fglobal_game_tracker.py) | 3,555 chapters parsed, 150 ranked characters (66,802 Fang Heng mentions), Lv 1–120+ Zombie & Proliferator calculator, Abe Akaya & Ouroboros calculators, Spoiler-Free Chapter Time-Machine |

## 🏗️ Recommended Subfolder Structure & Naming Convention

Because every subfolder contains **one single-file HTML web app**, **one Markdown reference**, and **optional Python calculators**, renaming the HTML file to `index.html` and the Markdown file to `README.md` inside each subfolder unlocks the best experience on both **GitHub** and **GitHub Pages / Cloudflare Pages**:

1. **Clean Browser URLs (`<SUBFOLDER>/index.html`)**: Visiting `https://oreokitten.github.io/wiki/AITZA/` (or your Cloudflare Pages URL `/AITZA/`) automatically loads `AITZA/index.html` without needing to type a long filename in the URL bar.
2. **Automatic GitHub Folder Rendering (`<SUBFOLDER>/README.md`)**: Opening `https://github.com/OreoKitten/wiki/tree/main/AITZA` on GitHub automatically renders `README.md` below the file list as a formatted encyclopedia.
3. **Dual-Mode Support in the Hub**: The root `index.html` hub supports **both** standardized names (`index.html` / `README.md`) and your original descriptive filenames (`global_game_wiki_and_tracker.html` / `global_game_character_wiki.md`) via a one-click Path Mode toggle in the top toolbar.

### Repository File Tree

```text
wiki/
├── index.html                                  # Interactive Hub Portal (Root Website)
├── README.md                                   # Repository Documentation & Master Index
├── LICENSE                                     # MIT License
└── AITZA/                                      # Subfolder: Global Game: AFK In The Zombie Apocalypse
    ├── index.html                              # Renamed from global_game_wiki_and_tracker.html (Recommended)
    ├── README.md                               # Renamed from global_game_character_wiki.md (Recommended)
    └── global_game_tracker.py                  # Standalone CLI Stat Calculator & Character Database
```

*(Note: If you prefer keeping the original filenames `global_game_wiki_and_tracker.html` and `global_game_character_wiki.md` inside `AITZA/`, or keeping both copies, the hub website's **Filename Mode Switcher** links directly to either convention.)*

## 🧟 Featured Subfolder: `AITZA` — AFK In The Zombie Apocalypse

The first subfolder (`AITZA/`) catalogs all **3,555 chapters** (~28.04 million characters of text) of *Global Game: AFK In The Zombie Apocalypse Game* centered on protagonist **Fang Heng**.

### What's Inside `AITZA/`

- **Interactive Single-File Web App (`AITZA/index.html` / `global_game_wiki_and_tracker.html`)**:
  - **Character Wiki & Index (150 Characters)**: Searchable and filterable by Faction, Prominence Tier, and A–Z initials, with multi-mode sorting by Total Mentions, Total Chapters, First/Given Name (`Heng`), Last/Family Name (`Fang`), Full Name, and Debut Chapter.
  - **Zombie Clone & Proliferator Calculator (Lv 1–120+)**: Implements the exact novel math (`n` clones/level for Lv 1–10 = 55 clones; `ceil(prev * 1.2)` base clones for Lv 11+ with `x2` at 6h, `x3` at 12h, and `x4` full army at 18h) cross-checked against 27 novel-verified chapter milestones.
  - **Zombie Form Solidification Cost Calculator**: Computes Survival Points, Evolution Crystals, and King of Gods' Points for Vine+Tyrant, Mutant Worm, Rapid Division, Undead Conversion, Underworld Hunter, and God of the Underworld forms.
  - **Sacred Tree Abe Akaya & Seed of Ouroboros Calculators**: Tracks Abe Akaya's Dimensional Level (`floor(Lv / 10) + 1`), Vampire Clan attribute boosts, Prayer Temple discount (`-12%`), Seven Deadly Sins Demonic Seeds, and Ouroboros external modification slots.
  - **Reading Chapter Time-Machine (Ch. 1–3,555)**: Spoiler-free slider that displays Fang Heng's exact level, zombie count, active arc, and active characters (`±40` chapters) at your current reading chapter, saved automatically in `localStorage`.
- **Master Markdown Encyclopedia (`AITZA/README.md` / `global_game_character_wiki.md`)**:
  - Complete Markdown reference tables for the Top 150 characters (ordered by frequency, Given Name A–Z, and Surname A–Z), detailed character dossiers (#1–#100), and the Level 1–70 Zombie Clone & Proliferator reference table.
- **Python CLI Stat Tracker (`AITZA/global_game_tracker.py`)**:
  - Zero-dependency Python 3 script upgraded from `zombiecalc.py` with both CLI flags and an interactive terminal menu.

### Running the `AITZA` Python Calculator Locally

```bash
# 1. Launch the interactive terminal menu (options 1-7 + CSV export)
python3 AITZA/global_game_tracker.py --interactive

# 2. Print the Lv 1-70 Zombie Clone & Proliferator table with novel chapter citations
python3 AITZA/global_game_tracker.py --max-level 70 --extended

# 3. Inspect a single level (e.g., Level 40 or Level 63) as JSON
python3 AITZA/global_game_tracker.py --level 40

# 4. Query the 150-character wiki sorted by First Name, Last Name, or Mentions
python3 AITZA/global_game_tracker.py --wiki --sort first --limit 30
python3 AITZA/global_game_tracker.py --search "Vampire"

# 5. Calculate Sacred Tree Abe Akaya stats at a specific tree level
python3 AITZA/global_game_tracker.py --abe-level 148
```

## ➕ How to Add a New Novel or Software Subfolder

1. **Create the Subfolder**: Create a new directory at the repository root using a short code or slug (e.g., `LOTM/`, `ORV/`, `OBSIDIAN/`).
2. **Add Your Files**:
   - Place the interactive HTML file inside as `<SUBFOLDER>/index.html` (or keep its custom `.html` name).
   - Place the Markdown wiki inside as `<SUBFOLDER>/README.md` (or keep its custom `.md` name).
   - Place any Python calculators or helper scripts inside `<SUBFOLDER>/`.
3. **Register the Card in the Hub (Optional if using Auto-Discovery)**:
   - Open the live Hub (`index.html`), click **➕ Add Subfolder Entry**, fill in the folder code and file names, and copy the generated JSON entry into the `WIKI_PROJECTS` array in root `index.html`.
   - Even if you haven't added an entry to `WIKI_PROJECTS` yet, clicking **🔄 Sync GitHub Repo** on the hub queries the GitHub API (`OreoKitten/wiki`) and automatically discovers any new subfolders in the `main` branch!

## 🚀 Deployment Guide: GitHub Pages & Cloudflare Pages

Because this repository uses **100% static HTML/CSS/JS with relative paths (`./<SUBFOLDER>/...`)**, it works on **both** GitHub Pages and Cloudflare Pages simultaneously with zero build steps.

| Hosting Platform | Setup Steps | Resulting URL Structure |
| :--- | :--- | :--- |
| **GitHub Pages** | 1. Go to **Settings → Pages** in `OreoKitten/wiki`<br>2. Under **Build and deployment**, select **Deploy from a branch**<br>3. Select branch **`main`** and folder **`/ (root)`**, then click **Save** | Hub: `https://oreokitten.github.io/wiki/`<br>AITZA: `https://oreokitten.github.io/wiki/AITZA/` |
| **Cloudflare Pages** | 1. Go to **Cloudflare Dashboard → Workers & Pages → Create → Pages → Connect to Git**<br>2. Select `OreoKitten/wiki` and branch **`main`**<br>3. Leave **Build command** blank and set **Build output directory** to `/` | Hub: `https://<project>.pages.dev/`<br>AITZA: `https://<project>.pages.dev/AITZA/` |

## 📄 License

Distributed under the [MIT License](https://www.google.com/search?q=.%2FLICENSE).
