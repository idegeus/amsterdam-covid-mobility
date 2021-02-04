#!/usr/bin/python3
"""
File:       append_areas.py
Author:     Martijn Schendstok
Date:       January 2021
"""

import sys
import json
import os
import pandas as pd
from shapely.geometry import shape, GeometryCollection, Point
DROOT = '/Users/martijn/Documents/Data Science/Data Systems Project.nosync/Data'


def append_area(df, geoJSON, area_title):
    df[area_title] = ""

    with open(geoJSON, 'r') as f:
        js = json.load(f)

    for index, row in df.iterrows():
        point = Point(row['AankomstLon'], row['AankomstLat'])

        for feature in js['features']:
            polygon = shape(feature['geometry'])
            if polygon.contains(point):
                df.at[index, area_title] = feature["properties"][area_title]
                #print('{}:'.format(area_title), feature["properties"][area_title])

    return df


def main(argv):
    path = os.path.join(DROOT, "/gvb/")

    with open(path + "Bestemming_Uur_merged_one_location.csv", "r") as csv_file:
        df = pd.read_csv(csv_file, sep=',')

    df = append_area(df, "data/geoJSON/GEBIED_STADSDELEN.json", "Stadsdeel")
    df = append_area(df, "data/geoJSON/GEBIED_WIJKEN.json", "Buurtcombinatie")

    df.to_csv("data/Bestemming_Uur_merged_one_location_with_areas.csv")


if __name__ == "__main__":
    main(sys.argv)