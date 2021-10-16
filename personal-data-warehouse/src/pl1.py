#!/usr/bin/env python3

import os
import csv
import argparse
import requests

def search_player(pattern):
    url = "https://baseballsavant.mlb.com/player/search-all?search=" + pattern
    with requests.get(url) as r:
        r.raise_for_status()
        matches = r.json()

    if not matches:
        print("No matches found.")
        return False

    for match in matches:
        if not isinstance(match, dict):
            continue

        player_name = match.get("name", False)
        if not player_name:
            continue

        print("=============================================")
        print("Match found: {name}".format(name=player_name))

        user_input = input(
            "Type yes if this is the player you want"
            " or press enter to go to the next match."
        )
        if user_input.strip().lower() == "yes":
            return match

    return False
    
def import_player_data(year, player, player_type):
    if not isinstance(player, dict):
        print("Importer player parameter is invalid.")
        return

    player_id = player.get("id", False)
    if not player_id:
        print("Player has no unique id.")
        return

    url = "https://baseballsavant.mlb.com/feed"
    parameters = {
        "warehouse": True,
        "hfGT": "R|PO|",
        "min_pitches": 0,
        "min_results": 0,
        "min_pas": 0,
        "type": "details",
        "player_type": player_type,
        "player_id": player_id,
        "hfSea": "{y}|".format(y=year)
    }
    with requests.get(url, params=parameters) as r:
        r.raise_for_status()
        response = r.json()

    return response
    
def save_to_file(player, player_data):
    if not player_data:
        print("No player data to save to file.")
        return

    player_name = player["name"].replace(".", "").strip().lower()
    filename = "_".join(player_name.split(" ")) + ".csv"
    filepath = os.path.join(os.getcwd(), filename)
    with open(filepath, "w") as csv_file:
        rows = []
        writer = csv.writer(
            csv_file,
            delimiter=",",
            quotechar="\""
        )

        header = player_data[0].keys()
        rows.append(header)

        for data in player_data:
            row = [data[key] for key in header]
            rows.append(row)

        writer.writerows(rows)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Statcast data importer.")
    parser.add_argument(
        "--year",
        nargs=1,
        type=int,
        required=True,
        help="Year to import."
    )
    parser.add_argument(
        "--batter",
        nargs=1,
        type=str,
        required=False,
        help="Batter to import."
    )
    parser.add_argument(
        "--pitcher",
        nargs=1,
        type=str,
        required=False,
        help="Pitcher to import."
    )
    args = parser.parse_args()

    year = args.year[0]	
    if args.batter:
        player = search_player(args.batter[0])
        if player:
            player_data = import_player_data(year, player, "batter")
            save_to_file(player, player_data)

    elif args.pitcher:
        player = search_player(args.pitcher[0])
        if player:
            player_data = import_player_data(year, player, "pitcher")
            save_to_file(player, player_data)

    else:
        print("Must provide a batter or pitcher.")
