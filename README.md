# P99 Loot Analyzer

A Python tool for analyzing EverQuest Project 1999 log files and collecting loot statistics to help update and improve the [Project 1999 Wiki](https://wiki.project1999.com/Main_Page).

## Purpose

The goal of this project is to automate the collection and analysis of loot data from EverQuest Project 1999 log files.
Instead of manually recording every kill and loot, the analyzer reads the EverQuest log and builds structured statistics for each monster encountered.
The collected data can then be used to update loot tables and statistics on the Project 1999 Wiki.

## Current Features

- Select an EverQuest log file through the graphical interface
- Validate the selected log file
- Detect monsters killed
- Detect kills reported by other players
- Count kills by monster
- Detect looted items
- Count loot by monster
- Detect money received from corpses
- Track Platinum, Gold, Silver and Copper
- Keep loot statistics separated by monster
- Sort monsters by number of kills in descending order
- Sort loot items by quantity in descending order
- Display collected statistics in a graphical interface
- Scroll through results using the mouse wheel
- Export collected statistics to CSV

## Installation

### Requirements

- Python 3.10 or newer
- Tkinter
- Pillow

Clone or Download the Repository:

```bash
git clone https://github.com/benoitmignault/p99-loot-analyzer.git
```

Navigate to the project directory:

```bash
cd p99-loot-analyzer
```

### Install Dependencies

Install the required Python package:

```bash
pip install pillow
```
Tkinter is included with most Python installations on Windows.

## How to Use

1. Start the Application 

```bash
python gui.py
```

2. Select an EverQuest Log File

Click the Select Log File button.

The selected file must:

Be a .txt file
Start with eqlog_

For example: 

`eqlog_Halfskeleting_P1999Green.txt`


- Once a valid log file has been selected, the selected character name is displayed on the button and the Run Analysis button becomes available.

3. Run the Analysis

The analyzer processes the selected EverQuest log file and displays the collected statistics.
Monsters are displayed in descending order according to the number of kills.
Loot items for each monster are also displayed in descending order according to the quantity looted.

4. Export the Results to CSV

Once the analysis has been completed, click Export CSV.
Choose the location and filename for the CSV file.
The CSV contains:

- Monster
- Number of kills
- Platinum
- Gold
- Silver
- Copper
- Looted items

Each unique loot item becomes its own column.
If a monster did not produce a particular item, the value is set to 0.

For example:

    Monster        | Kills | Platinum | Gold | Silver | Copper | Bear Meat | Grizzly Skin
    a grizzly bear | 12    | 0        | 2    | 5      | 10     | 6         | 3
    a kodiak bear  | 8     | 0        | 1    | 3      | 5      | 2         | 0

## How It Works

The analyzer processes the EverQuest log line by line.

For example:

    You have slain a bandit!
    You receive 3 gold, 17 silver and 13 copper from the corpse.
    --You have looted a Bandit Sash.--

The program identifies:

- The monster: `a bandit`
- The money received from the corpse
- The item looted

The information is then stored in a dynamic data structure.

## Data Collection Guidelines

When collecting loot data in a zone containing multiple types of monsters, it is important to fully loot a monster before killing another one.

The analyzer associates looted items and money with the most recently detected monster kill.

For example:

    Kill Monster A
    Kill Monster B
    Loot Monster A
    Loot Monster B

The log does not provide enough information for the analyzer to reliably determine which corpse the loot from Monster A came from. 
The loot and money may therefore be incorrectly associated with Monster B.

### Recommended procedure

Always follow this sequence:

    Kill Monster A
    Loot Monster A
    Kill Monster B
    Loot Monster B
    Kill Monster C
    Loot Monster C

This ensures that items and money are correctly associated with the monster that dropped them.

This is especially important in zones where several different monster types are being analyzed simultaneously.

### Single Monster Type Zones

If the zone contains only one type of monster being analyzed, this restriction does not apply.

For example, if you are collecting data only for `a grizzly bear`, you can kill several grizzly bears before looting them. Since all kills are the same monster type, the loot and currency can still be correctly associated with `a grizzly bear`.

This restriction is therefore only important when collecting data for multiple monster types at the same time.

## Example

A simplified result might look like:

    Monster: a bandit
    Kills: 107

    --- Money ---
    Gold: 137
    Silver: 879
    Copper: 837

    --- Loot ---
    Bandit Sash: 11
    Bronze Two Handed Sword: 6
    Human Blood: 10

## Data Collection

The statistics generated by this project are intended to contribute to the Project 1999 Wiki.

The goal is to collect larger samples of real gameplay data and use them to improve the available information about EverQuest NPC loot tables.

## Planned Features

- Select an EverQuest log file through a graphical interface
- Automatically locate the EverQuest Logs directory
- Calculate loot drop rates
- Calculate total loot value
- Export statistics to CSV
- Generate tables formatted for the Project 1999 Wiki
- Track statistics by zone
- Improve handling of multiple characters and group looting

## Project Status

Work in progress.

The current version focuses on parsing EverQuest log files and building the underlying data structure used for loot statistics.

## License

This project is licensed under the MIT License.
