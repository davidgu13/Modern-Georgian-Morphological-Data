# Modern-Georgian-Morphological-Data
This project contains a dataset of Georgian verb paradigms, annotated by the standard Unimorph format.

Each Directory represents a Georgian conjugational class (as defined by Hewitt, 1995), and contains verbs from these classes.

Each file contains a paradigm of the verb depicted in its name (in Georgian, of course). The paradigm is formatted by the UniMorph format, and arranged by Screeves and by person (the order is 1sg-2sg-3sg-1pl-2pl-3pl). For one's convenience, the script "remove_transliteration.py" takes such file and turns it into the lemma-form-features format. Once creating the data is complete, a unified file with all verbs will also be uploaded.

Most importantly, although the paradigms seem to be automatically-generated, their correction was verified by native speakers of the language! Therefore, that data is much more accurate than the current UniMorph dataset!
