"""Pronounceable fake word generation.

Ported from VB6 PronounceableWord() in Main.bas.
"""

from pyfwert.random import rand
from pyfwert.utils import pick_one
from pyfwert.constants import VOWELS2, CONSONANTS2, CONSONANTS3


# Vowel suffixes that can end words
VOWEL_SUFFIXES = (
    "ing ers ance ence le ness ings ment ize ate ive ute acy ous ify "
    "ought some edness ed es ly less ment able ible les led ious ant "
    "ary iety ist ism ial ate act ure iac ice aint ent ant ure ide ify les"
)

# Consonant suffixes that can end words
CONSONANT_SUFFIXES = (
    "cked cker tor ter ly rer tic nst lyst onic ght nge nce zer cy ly "
    "ny lic dged red ate ndle ching tching lent ged zen ted nnial lic "
    "rly stic se les"
)

# T-ending suffixes
T_SUFFIXES = "ion ity ient ment ance ly less ter tor"


def pronounceable_word():
    """Generate a fake but pronounceable word.

    Returns:
        A random pronounceable word.

    The algorithm alternates between vowels and consonants,
    with chances to add common word endings.
    """
    word = ""
    vowel_next = rand(1) == 1

    for i in range(rand(5, 4)):
        word_len = len(word)

        if vowel_next:
            # Maybe add a vowel suffix and exit
            if rand(3) == 0 and word_len > 1:
                word += pick_one(VOWEL_SUFFIXES)
                break

            word += pick_one(VOWELS2, 2)
        else:
            # Maybe add a consonant suffix and exit
            if rand(3) == 0 and word_len > 0:
                word += pick_one(CONSONANT_SUFFIXES)
                break

            # Add consonant cluster or single consonant
            if rand(3) == 0 and word_len > 0:
                word += pick_one(CONSONANTS3)
            else:
                word += pick_one(CONSONANTS2, 2)

            # Check for special T-endings
            if word.endswith("t"):
                if rand(2) == 0 and word_len > 1:
                    word += pick_one(T_SUFFIXES)
                    break

        vowel_next = not vowel_next

    # Clean up doubled letters that shouldn't be doubled
    cleanup_pairs = [
        ("aa", "a"), ("hh", "h"), ("ii", "i"), ("jj", "j"),
        ("kk", "k"), ("qq", "qu"), ("uu", "u"), ("vv", "v"),
        ("ww", "w"), ("xx", "x"), ("yy", "y")
    ]
    for old, new in cleanup_pairs:
        if old in word:
            word = word.replace(old, new)

    # "i before e except after c"
    if "cie" in word:
        word = word.replace("cie", "cei")

    # Don't start a word with double letters
    if len(word) >= 2 and word[0] == word[1]:
        word = word[1:]

    return word


def fakeword(base_word):
    """Create a fake word by adding prefixes and/or suffixes to a base word.

    Args:
        base_word: The base word to modify.

    Returns:
        A new fake word derived from the base.
    """
    prefixes = (
        "a ab abso aca acri admini alpha ambi ana ant ante anti apro aqua "
        "archi astro atmo audi auto be bene beta beva bi bio centa chrono "
        "circum co co- com con contra counter credo cryo cyber cyclo de "
        "deca demo dextro di dia dicto dis double- duo dyna dyno dys e "
        "ecto ef endo entre equi euro every ex exo extra fa fan fict fiz "
        "flo fore fun gag gamma gap geo gig giga glyco goo gyro he hemi "
        "hetero hexa his holo homeo homo hosp hu hydro hyper hypo id "
        "identi ig imi in info infra int inter intra intro iso kilo kno "
        "la lacto li longi luma ma macro magni mali mega meso meta micro "
        "milli mini mis mono multi nano navi neo non non- novi octa octo "
        "omni otco over oxy pan para peda penta per peri philo phoni "
        "phono physi pico poly post pre pre- pro proto quad re retro "
        "sancti semi septo similli steno sub super supra synchro tele "
        "tera tetra thermo trans tre tri ultra un una under uni uno "
        "vario vita xantho xero"
    )

    suffixes = (
        "able ad aero alooza any ation be bi bio cate cede ceed cess "
        "eting fest fy gram graph iac ible ify ing ism ist ity ize log "
        "logue logy maniac ment meter metry ogram ograph oid ology "
        "ometer opath opsy osity phile phobe phobia phone super tion "
        "tious ty"
    )

    prefix = pick_one(prefixes)
    suffix = pick_one(suffixes)

    # Sometimes add hyphen after prefix
    if rand(100) <= 20:
        if "-" not in prefix:
            prefix = prefix + "-"

    # Build the new word
    choice = rand(5, 1)
    if choice == 1:
        new_word = prefix + base_word + suffix
    elif choice == 2:
        new_word = base_word + suffix
    else:
        new_word = prefix + base_word

    # Clean up repeated letters
    cleanup = [
        ("aa", "a"), ("ii", "i"), ("hh", "h"), ("jj", "j"),
        ("kk", "k"), ("qq", "q"), ("uu", "u"), ("ww", "w"),
        ("xx", "x"), ("yy", "y"), ("zz", "z"), ("eae", "ae")
    ]
    for old, new in cleanup:
        new_word = new_word.replace(old, new)

    return new_word
