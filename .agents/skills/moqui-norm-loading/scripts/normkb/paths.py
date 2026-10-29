"""Where the norm tooling reads and writes. The scripts live in the skills of moqui-agent-skills; what they read and
generate lives in the mantle-compliance component:

    data/                     the seed data (39_ stubs, 40_ norms, 42_ cross references, 60_, 70_ files)
    data/norms/norms.json     the norms and their sources, reader settings
    data/norms/figures/       figures written in our own words, per norm
    data/norms/tables/        transcriptions of tables printed as images (licensed norms: not committed)
    data/norms/vocabulary/    VOCAB-BASE.json, HOOKS-<normId>.json, LABELS-<lang>.json
    data/norms/associations/  associations reviewed by an expert
    build/norm-kb/            intermediate files (ir/, items/), never committed

The data loader reads only the files at the top of data/, so data/norms/ is never loaded.

The component is the directory in env MANTLE_COMPLIANCE, else the first mantle-compliance component found from the
current directory upwards (the component itself, a Moqui root with runtime/component/mantle-compliance, or a
directory holding it).
"""
import os
import sys
from pathlib import Path

SKILLS = Path(__file__).resolve().parents[3]          # normkb -> scripts -> moqui-norm-loading -> skills
LOADING = SKILLS / 'moqui-norm-loading' / 'scripts'
HOOKS = SKILLS / 'moqui-norm-hooks' / 'scripts'
ASSOC = SKILLS / 'moqui-norm-associations' / 'scripts'


def is_component(d):
    f = Path(d) / 'component.xml'
    return f.is_file() and 'name="mantle-compliance"' in f.read_text(encoding='utf-8')


def find_component():
    env = os.environ.get('MANTLE_COMPLIANCE')
    if env:
        if not is_component(env):
            sys.exit(f'MANTLE_COMPLIANCE={env} is not the mantle-compliance component')
        return Path(env).resolve()
    cwd = Path.cwd().resolve()
    for d in (cwd, *cwd.parents):
        for c in (d, d / 'runtime' / 'component' / 'mantle-compliance', d / 'mantle-compliance'):
            if is_component(c):
                return c
    sys.exit('mantle-compliance component not found: set MANTLE_COMPLIANCE or run from inside the Moqui root')


COMPONENT = find_component()
FRAMEWORK = COMPONENT.parents[2]                       # component -> runtime/component -> runtime -> framework root
DATA = COMPONENT / 'data'
# headers of the documents the norms cite and that are not loaded: loaded before the norms that cite them (a
# reference of a 40_ file is a foreign key to its Agreement), so a fresh database loads in the order of the prefixes
STUBS = '39_NormStubs.xml'
NORMS = DATA / 'norms'
CONFIG = NORMS / 'norms.json'
FIGURES = NORMS / 'figures'
TABLES = NORMS / 'tables'
VOCABULARY = NORMS / 'vocabulary'
ASSOCIATIONS = NORMS / 'associations'
WORK = COMPONENT / 'build' / 'norm-kb'
IR = WORK / 'ir'
ITEMS = WORK / 'items'
