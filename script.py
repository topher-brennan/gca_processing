import re
from collections import defaultdict

MAGIC_FILENAME = "GURPS Magic 4e.gdf"
WIZARDRY_REFINED_FILENAME = "GURPS Dungeon Fantasy Pyramid 3-60 Wizardry Redefined.gdf"
ADVENTURERS_FILENAME = "GURPS Dungeon Fantasy  1 - Adventurers.GDF"
NEXT_LEVEL_FILENAME = "GURPS Dungeon Fantasy  3 - Next Level.gdf"
CLERICS_FILENAME = "GURPS Dungeon Fantasy  7 - Clerics.gdf"
DFRPG_FILENAME = "Dungeon Fantasy RPG.gdf"

SPELL_PATTERN = r'(?<=SP:)[\w \(\)\[\]]+(?=\n)'
DELETE_PATTERN = r'(?<=#Delete "SP:)[\w \(\)\[\]]+(?=")'
HOLY_PATTERN = r'(?<=SP:)[\w \(\)\[\]]+Holy\)'
DRUIDIC_PATTERN = r'(?<=SP:)[\w \(\)\[\]]+Druidic\)'
UNHOLY_PATTERN = r'(?<=SP:)[\w \(\)\[\]]+Unholy\)'
CLONE_PATTERN = r'(?<=#Clone "SP:)[\w \(\)\[\]]+(?=")'
SPELL_BLOCK_PATTERN = r'.+, type.+\n.+\n.+\n?.*Prereq Count: \d.+\)'
DFRPG_SPELL_BLOCK_PATTERN = r'.+,\n\tcat.+(?:\n\t.+)+Prereq Count: \d+ Prerequisites: .+'
PREREQ_COUNT_PATTERN = r'(?<=Prereq Count: )\d+'
PREREQ_PATTERN = r'(?<=Prerequisites: ).+(?=\))'

DFRPG_COLLEGE_PATTERN_START = r'.+,\n\tcat\('
DFRPG_COLLEGE_PATTERN_END = r'.+(?:\n\t.+)+Prereq Count: \d+ Prerequisites: .+'

COLLEGES = [
    'Air',
    'Body Control',
    'Communication & Empathy',
    'Earth',
    'Fire',
    'Food',
    'Gate',
    'Healing',
    'Illusion',
    'Knowledge',
    'Light & Darkness',
    'Making & Breaking',
    'Meta-Spells',
    'Mind Control',
    'Movement',
    'Necromantic',
    'Protection & Warning',
    'Sound',
    'Water',
    'Weather',
]


def remove_word(string, word):
    string = ''.join(string.split(f' ({word})'))
    string = ''.join(string.split(f'; {word}'))
    return string

def from_different_system(spell_name):
    return 'Clerical' in spell_name or 'Syntactic' in spell_name or 'Ritual' in spell_name

def print_set(s):
    print(f'{sorted(list(s))} ({len(s)} items)')

def get_prereq_map(file_contents, pattern=SPELL_BLOCK_PATTERN, string_filter=''):
    spell_blocks = re.findall(pattern, file_contents)
    prereq_map = {}
    for spell_block in spell_blocks:
        if string_filter not in spell_block:
            continue
        spell_name = spell_block.split(',')[0]
        # TODO: improve this to handle "or"s.
        prereq_count = re.search(PREREQ_COUNT_PATTERN, spell_block).group()
        prereqs_match = re.search(PREREQ_PATTERN, spell_block)
        if prereqs_match:
            prereqs = set([prereq.replace('and ', '') for prereq in prereqs_match.group().split(', ')])
        else:
            prereqs = set()
        prereq_map[spell_name] = [prereqs, prereq_count]
    return prereq_map

magic = open(MAGIC_FILENAME).read()
all_spells = set([spell_name for spell_name in re.findall(SPELL_PATTERN, magic) if not from_different_system(spell_name)])

wizardry_refined = open(WIZARDRY_REFINED_FILENAME).read()
wizardry_refined_forbidden = set(re.findall(DELETE_PATTERN, wizardry_refined))

def produce_with_cache(producer, cache={}):
    if producer not in cache:
        cache[producer] = producer()
    return cache[producer]

def _get_adventurers():
    return open(ADVENTURERS_FILENAME).read()

def get_adventurers(cache=[]):
    return produce_with_cache(_get_adventurers)

def _get_standard_cleric_spells():
    return set([remove_word(spell_name, 'Holy') for spell_name in re.findall(HOLY_PATTERN, get_adventurers())])
    
def get_standard_cleric_spells():
    return produce_with_cache(_get_standard_cleric_spells)

def _get_druid_spells():
    return set([remove_word(spell_name, 'Druidic') for spell_name in re.findall(DRUIDIC_PATTERN, get_adventurers())])

def get_druid_spells(cache=[]):
    return produce_with_cache(_get_druid_spells)

def _get_next_level():
    return open(NEXT_LEVEL_FILENAME).read()

def get_next_level():
    return produce_with_cache(_get_next_level)

def _get_evil_cleric_spells():
    return set([remove_word(spell_name, 'Unholy') for spell_name in re.findall(UNHOLY_PATTERN, get_next_level)])

def get_evil_cleric_spells():
    return produce_with_cache(_get_evil_cleric_spells)

clerics = open(CLERICS_FILENAME).read()
specialist_cleric_spells = set(re.findall(CLONE_PATTERN, clerics))

# prereq_map = get_prereq_map(magic)
# wizardry_refined_prereq_map = get_prereq_map(wizardry_refined)

# TODO: These need to be changed to function calls
# all_cleric_spells = standard_cleric_spells.union(evil_cleric_spells).union(specialist_cleric_spells)
# druid_exclusives = druid_spells - all_cleric_spells
# standard_cleric_exclusives = standard_cleric_spells - evil_cleric_spells - specialist_cleric_spells
# evil_cleric_exclusives = evil_cleric_spells - standard_cleric_spells - specialist_cleric_spells
# wizard_exclusives = all_spells - wizardry_refined_forbidden - all_cleric_spells - druid_spells

# I wrote this code to help me design a magical style (per GURPS Thuamatology: Magical Styles)
# Unfortunately, I don't really remember what I was going for with said style
"""
def print_style_candidates():
    style_spell_candidates = set()
    for spell_name in wizard_exclusives:
        if prereq_map.get(spell_name) and \
                (prereq_map[spell_name][0].intersection(all_cleric_spells) or \
                prereq_map[spell_name][1] == '0'):
            style_spell_candidates.add(spell_name)

    print_set(style_spell_candidates)

    for candidate in sorted(list(style_spell_candidates)):
        if 'Divination' not in candidate and 'Command Spirit' not in candidate:
            print(f'{candidate}: {prereq_map[candidate][1]}')
"""

# print_set(evil_cleric_exclusives)
# print_set(standard_cleric_exclusives)
# print_set(wizard_exclusives)
# print_set(all_cleric_spells)
# print_set(druid_exclusives)

dfrpg = open(DFRPG_FILENAME).read()
dfrpg_prereq_map = get_prereq_map(dfrpg, DFRPG_SPELL_BLOCK_PATTERN)

# print(dfrpg_prereq_map)
# print(prereq_map)

def to_graphviz(prereq_map):
    reversed_prereq_map = defaultdict(list)
    for spell, info in prereq_map.items():
        for prereq in info[0]:
            if 'Magery' not in prereq:
                reversed_prereq_map[prereq].append(spell)
            else:
                pass # TODO: Indicate Magery prerequisites in some other way.

    result = 'digraph {\n'
    for prereq, prereq_for in reversed_prereq_map.items():
        safe_prereq = prereq.replace('"', "'")
        result += f'    "{safe_prereq}" -> '
        result += '{ '
        result += ', '.join([f'"{spell}"' for spell in prereq_for])
        result += ' }\n'
    result += '}'

    return result

for college in COLLEGES:
    pattern = DFRPG_COLLEGE_PATTERN_START + re.escape(college) + DFRPG_COLLEGE_PATTERN_END
    snake_case_college = college.lower().replace(" ", "_")
    file_name = f"{snake_case_college}_spells.dot"
    open(file_name, 'w').write(to_graphviz(get_prereq_map(dfrpg, pattern)))
