import re

MAGIC_FILENAME = "GURPS Magic 4e.gdf"
WIZARDRY_REFINED_FILENAME = "GURPS Dungeon Fantasy Pyramid 3-60 Wizardry Redefined.gdf"
ADVENTURERS_FILENAME = "GURPS Dungeon Fantasy  1 - Adventurers.GDF"
NEXT_LEVEL_FILENAME = "GURPS Dungeon Fantasy  3 - Next Level.gdf"
CLERICS_FILENAME = 'GURPS Dungeon Fantasy  7 - Clerics.gdf'

SPELL_PATTERN = r'(?<=SP:)[\w \(\)\[\]]+(?=\n)'
DELETE_PATTERN = r'(?<=#Delete "SP:)[\w \(\)\[\]]+(?=")'
HOLY_PATTERN = r'(?<=SP:)[\w \(\)\[\]]+Holy\)'
UNHOLY_PATTERN = r'(?<=SP:)[\w \(\)\[\]]+Unholy\)'
CLONE_PATTERN = r'(?<=#Clone "SP:)[\w \(\)\[\]]+(?=")'

def remove_word(string, word):
    string = ''.join(string.split(f' ({word})'))
    string = ''.join(string.split(f'; {word}'))
    return string

def from_different_system(spell_name):
    return 'Clerical' in spell_name or 'Syntactic' in spell_name or 'Ritual' in spell_name

def print_set(s):
    print(f'{sorted(list(s))} ({len(s)} items)')

magic = open(MAGIC_FILENAME).read()
all_spells = set([spell_name for spell_name in re.findall(SPELL_PATTERN, magic) if not from_different_system(spell_name)])

wizardry_refined = open(WIZARDRY_REFINED_FILENAME).read()
wizardry_refined_forbidden = set(re.findall(DELETE_PATTERN, wizardry_refined))

adventurers = open(ADVENTURERS_FILENAME).read()
standard_cleric_spells = set([remove_word(spell_name, 'Holy') for spell_name in re.findall(HOLY_PATTERN, adventurers)])

next_level = open(NEXT_LEVEL_FILENAME).read()
evil_cleric_spells = set([remove_word(spell_name, 'Unholy') for spell_name in re.findall(UNHOLY_PATTERN, next_level)])

clerics = open(CLERICS_FILENAME).read()
specialist_cleric_spells = set(re.findall(CLONE_PATTERN, clerics))

all_cleric_spells = standard_cleric_spells.union(evil_cleric_spells).union(specialist_cleric_spells)
evil_cleric_exclusives = evil_cleric_spells - standard_cleric_spells - specialist_cleric_spells
wizard_exclusives = all_spells - wizardry_refined_forbidden - all_cleric_spells

# print_set(evil_cleric_exclusives)
# print_set(wizard_exclusives)
print_set(all_cleric_spells)
