from csv import reader
import pygame

def lire_csv(chemin):
    terrain_map = []
    with open(chemin) as level_map:
        layout = reader(level_map,delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map