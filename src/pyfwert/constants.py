"""Character sets and constants for password generation.

Ported from VB6 Constants.bas
"""

# Vowels in order of frequency
VOWELS = "eaoiu"

# Consonants in order of frequency
CONSONANTS = "tnshrdlcmfgypwbvkxjqz"

# Symbol choices (space-separated for pick_one)
SYMBOLS = "! @ # % $ ^ & * ( ) { } : ' / ` ~ * - < > + = _ | \\ \\ . . , , ; ; ? ? [ ]"

# Keyboard symbols
KEYBOARD_SYMBOLS = "`~!@#$%^&*()-_=+]}[{\\|'\";:/?.>,< "

# Sentence punctuation
SENTENCE_PUNCTUATION = "!;:?.,"

# End punctuation (space-separated, weighted by repetition)
END_PUNCTUATION = "! ! ! ! . . . . . . . . . . . . . . . ... ... ? ? ? ? ? ? ?"

# Letters in order of frequency
LETTERS = "etaoinshrdlucmfgypwbvkxjqz"

# Uppercase and lowercase letters
UCASE_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LCASE_LETTERS = "abcdefghijklmnopqrstuvwxyz"

# Numbers
NUMBERS = "0123456789"

# Smileys (space-separated)
SMILEYS = ":) :( :-) :-( :D :0 ;-) ;) :/ 8-) 8-( :-D :-0 :-p :^)"

# Vowel combinations (space-separated, weighted)
VOWELS2 = "a a a a a a a a a e e e e e e e e e e e i i i u u o o ay ea ee ia io oa oi oo er on re he ha in es io ou"

# Consonant combinations that can appear anywhere
CONSONANTS2 = "b b c d d d f g j k m m m n n p p qu r r r s s s s t t t t v w x z z th st sh ph ch th sh for has tis men"

# Consonant combinations that cannot start a word
CONSONANTS3 = "nd rt dd zz rg ng tt ss mm nn pp nt nc nl ft"

# Full keyboard character set
KEYBOARD = "1234567890`~!@#$%^&*()-_=+]}[{\\|'\";:/?.>,<abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Keyboard rows
NUMROW = "1234567890"
NUMROW_FULL = "1234567890`~!@#$%^&*()_-+="
ROW1 = "QWERTYUIOP"
ROW1_FULL = "QWERTYUIOP{[}]|\\"
ROW2 = "ASDFGHJKL"
ROW2_FULL = "ASDFGHJKL;:'\""
ROW3 = "ZXCVBNM"
ROW3_FULL = "ZXCVBNM,<.>/?"

# Hand positions
LEFT_HAND = "qwertasdfgzxcvb"
RIGHT_HAND = "yuiophjknm"

# Common letter combinations (space-separated)
DIGRAPHS = "th er on an re he in ed nd ha at en es of or nt ea ti to it st io le is ou ar as de rt ve"
TRIGRAPHS = "the and tha ent ion tio for nde has nce edt tis oft sth men"

# Common words (space-separated)
TWO_LETTER_WORDS = "of to in it is be as at so we he by or on do if me my up an go no us am"
THREE_LETTER_WORDS = "the and for are but not you all any can had her was one our out day get has him his how man new now old see two way who boy did its let put say she too use"

# Month names (space-separated)
LONG_MONTHS = "January February March April May June July August September October November December"
SHORT_MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec"

# Day names (space-separated)
LONG_DAYS = "Monday Tuesday Wednesday Thursday Friday Saturday Sunday"
SHORT_DAYS = "Mon Tue Wed Thu Fri Sat Sun"

# Escape sequences used during pattern processing
ESCAPE_SEQUENCES = {
    "\\\\": "#sla#",
    "\\+": "#pls#",
    "\\{": "#lbr#",
    "\\}": "#rbr#",
    "\\[": "#lba#",
    "\\]": "#rba#",
    "\\(": "#lpa#",
    "\\)": "#rpa#",
    "\\|": "#pip#",
}

# Reverse mapping for final output
UNESCAPE_SEQUENCES = {
    "#sla#": "\\",
    "#pls#": "+",
    "#lbr#": "{",
    "#rbr#": "}",
    "#lba#": "[",
    "#rba#": "]",
    "#lpa#": "(",
    "#rpa#": ")",
    "#pip#": "|",
}
