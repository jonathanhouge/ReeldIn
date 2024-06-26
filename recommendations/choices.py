GENRES = [
    ("", "No Preference"),
    ("Action", "Action"),
    ("Adventure", "Adventure"),
    ("Animation", "Animation"),
    ("Comedy", "Comedy"),
    ("Crime", "Crime"),
    ("Documentary", "Documentary"),
    ("Drama", "Drama"),
    ("Family", "Family"),
    ("Fantasy", "Fantasy"),
    ("History", "History"),
    ("Horror", "Horror"),
    ("Music", "Music"),
    ("Mystery", "Mystery"),
    ("Romance", "Romance"),
    ("Science Ficti", "Science Fiction"),  # odd db translation i guess?
    ("Thriller", "Thriller"),
    ("War", "War"),
    ("Western", "Western"),
]

YEAR_SPANS = [
    ("", "No Preference"),
    ("1900-1960", "1960 and before"),
    ("1960-1979", "1960-1979"),
    ("1980-1999", "1980-1999"),
    ("2000-2024", "2000 and after"),
]

RUNTIME_SPANS = [
    ("", "No Preference"),
    ("0-90", "90 or less"),
    ("90-120", "90-120"),
    ("120-150", "120-150"),
    ("150-900", "150 or more"),
]

LANGUAGES = [
    ("", "No Preference"),
    ("ab", "Abkhazian"),
    ("aa", "Afar"),
    ("af", "Afrikaans"),
    ("ak", "Akan"),
    ("sq", "Albanian"),
    ("am", "Amharic"),
    ("ar", "Arabic"),
    ("an", "Aragonese"),
    ("hy", "Armenian"),
    ("as", "Assamese"),
    ("av", "Avaric"),
    ("ae", "Avestan"),
    ("ay", "Aymara"),
    ("az", "Azerbaijani"),
    ("bm", "Bambara"),
    ("ba", "Bashkir"),
    ("eu", "Basque"),
    ("be", "Belarusian"),
    ("bn", "Bengali"),
    ("bi", "Bislama"),
    ("bs", "Bosnian"),
    ("br", "Breton"),
    ("bg", "Bulgarian"),
    ("my", "Burmese"),
    ("cn", "Cantonese"),
    ("ca", "Catalan"),
    ("ch", "Chamorro"),
    ("ce", "Chechen"),
    ("ny", "Chichewa; Nyanja"),
    ("cv", "Chuvash"),
    ("kw", "Cornish"),
    ("co", "Corsican"),
    ("cr", "Cree"),
    ("hr", "Croatian"),
    ("cs", "Czech"),
    ("da", "Danish"),
    ("dv", "Divehi"),
    ("nl", "Dutch"),
    ("dz", "Dzongkha"),
    ("en", "English"),
    ("eo", "Esperanto"),
    ("et", "Estonian"),
    ("ee", "Ewe"),
    ("fo", "Faroese"),
    ("fj", "Fijian"),
    ("fi", "Finnish"),
    ("fr", "French"),
    ("fy", "Frisian"),
    ("ff", "Fulah"),
    ("gd", "Gaelic"),
    ("gl", "Galician"),
    ("lg", "Ganda"),
    ("ka", "Georgian"),
    ("de", "German"),
    ("el", "Greek"),
    ("gn", "Guarani"),
    ("gu", "Gujarati"),
    ("ht", "Haitian; Haitian Creole"),
    ("ha", "Hausa"),
    ("he", "Hebrew"),
    ("hz", "Herero"),
    ("hi", "Hindi"),
    ("ho", "Hiri Motu"),
    ("hu", "Hungarian"),
    ("is", "Icelandic"),
    ("io", "Ido"),
    ("ig", "Igbo"),
    ("id", "Indonesian"),
    ("ia", "Interlingua"),
    ("ie", "Interlingue"),
    ("iu", "Inuktitut"),
    ("ik", "Inupiaq"),
    ("ga", "Irish"),
    ("it", "Italian"),
    ("ja", "Japanese"),
    ("jv", "Javanese"),
    ("kl", "Kalaallisut"),
    ("kn", "Kannada"),
    ("kr", "Kanuri"),
    ("ks", "Kashmiri"),
    ("kk", "Kazakh"),
    ("km", "Khmer"),
    ("ki", "Kikuyu"),
    ("rw", "Kinyarwanda"),
    ("ky", "Kirghiz"),
    ("kv", "Komi"),
    ("kg", "Kongo"),
    ("ko", "Korean"),
    ("kj", "Kuanyama"),
    ("ku", "Kurdish"),
    ("lo", "Lao"),
    ("la", "Latin"),
    ("lv", "Latvian"),
    ("lb", "Letzeburgesch"),
    ("li", "Limburgish"),
    ("ln", "Lingala"),
    ("lt", "Lithuanian"),
    ("lu", "Luba-Katanga"),
    ("mk", "Macedonian"),
    ("mg", "Malagasy"),
    ("ms", "Malay"),
    ("ml", "Malayalam"),
    ("mt", "Maltese"),
    ("zh", "Mandarin"),
    ("gv", "Manx"),
    ("mi", "Maori"),
    ("mr", "Marathi"),
    ("mh", "Marshall"),
    ("mo", "Moldavian"),
    ("mn", "Mongolian"),
    ("na", "Nauru"),
    ("nv", "Navajo"),
    ("nr", "Ndebele"),
    ("nd", "Ndebele"),
    ("ng", "Ndonga"),
    ("ne", "Nepali"),
    ("xx", "No Language"),
    ("se", "Northern Sami"),
    ("no", "Norwegian"),
    ("nb", "Norwegian Bokmål"),
    ("nn", "Norwegian Nynorsk"),
    ("oc", "Occitan"),
    ("oj", "Ojibwa"),
    ("or", "Oriya"),
    ("om", "Oromo"),
    ("os", "Ossetian; Ossetic"),
    ("pi", "Pali"),
    ("fa", "Persian"),
    ("pl", "Polish"),
    ("pt", "Portuguese"),
    ("pa", "Punjabi"),
    ("ps", "Pushto"),
    ("qu", "Quechua"),
    ("rm", "Raeto-Romance"),
    ("ro", "Romanian"),
    ("rn", "Rundi"),
    ("ru", "Russian"),
    ("sm", "Samoan"),
    ("sg", "Sango"),
    ("sa", "Sanskrit"),
    ("sc", "Sardinian"),
    ("sr", "Serbian"),
    ("sh", "Serbo-Croatian"),
    ("sn", "Shona"),
    ("sd", "Sindhi"),
    ("si", "Sinhalese"),
    ("cu", "Slavic"),
    ("sk", "Slovak"),
    ("sl", "Slovenian"),
    ("so", "Somali"),
    ("st", "Sotho"),
    ("es", "Spanish"),
    ("su", "Sundanese"),
    ("sw", "Swahili"),
    ("ss", "Swati"),
    ("sv", "Swedish"),
    ("tl", "Tagalog"),
    ("ty", "Tahitian"),
    ("tg", "Tajik"),
    ("ta", "Tamil"),
    ("tt", "Tatar"),
    ("te", "Telugu"),
    ("th", "Thai"),
    ("bo", "Tibetan"),
    ("ti", "Tigrinya"),
    ("to", "Tonga"),
    ("ts", "Tsonga"),
    ("tn", "Tswana"),
    ("tr", "Turkish"),
    ("tk", "Turkmen"),
    ("tw", "Twi"),
    ("ug", "Uighur"),
    ("uk", "Ukrainian"),
    ("ur", "Urdu"),
    ("uz", "Uzbek"),
    ("ve", "Venda"),
    ("vi", "Vietnamese"),
    ("vo", "Volapük"),
    ("wa", "Walloon"),
    ("cy", "Welsh"),
    ("wo", "Wolof"),
    ("xh", "Xhosa"),
    ("ii", "Yi"),
    ("yi", "Yiddish"),
    ("yo", "Yoruba"),
    ("za", "Zhuang"),
    ("zu", "Zulu"),
]

TRIGGERS = [
    # categorical (check out TRIGGERS_DICT)
    ("", "No Triggers"),
    ("Animal Harm / Death", "Animal Harm / Death"),
    ("Child Abuse", "Child Abuse"),
    ("Drug Usage / Abuse", "Drug Usage / Abuse"),
    (
        "Abuse and Manipulation (including sexual)",
        "Abuse and Manipulation (including sexual)",
    ),
    ("Violence", "Violence"),
    ("Excessive Violence", "Excessive Violence"),
    ("Human Death", "Human Death"),
    ("Bodily Functions", "Bodily Functions"),
    ("LGBT Issues & Problematic Depictions", "LGBT Issues & Problematic Depictions"),
    (
        "Depiction of Medical Issues: Diseases and Phobias",
        "Depiction of Medical Issues: Diseases and Phobias",
    ),
    (
        "Potentially Harmful Filmmaking (flashing lights, shaky cam, etc.)",
        "Potentially Harmful Filmmaking (flashing lights, shaky cam, etc.)",
    ),
    ("Pregnancy Issues", "Pregnancy Issues"),
    ("Sexual Content", "Sexual Content"),
    ("Bigotry", "Bigotry"),
    ("Potentially Scary Animals", "Potentially Scary Animals"),
    # singular
    ("there's an alligator/crocodile", "There's an Alligator/Crocodile"),
    ("someone's mouth is covered", "Someone's Mouth Is Covered"),
    ("there's shaving/cutting", "There's Shaving/Cutting"),
    ("Someone becomes unconscious", "Someone Becomes Unconscious"),
    (
        "someone disabled played by able-bodied",
        "Someone Disabled Played by Able-Bodied",
    ),
    ("there are jumpscares", "There Are Jumpscares"),
    ("there are clowns", "There Are Clowns"),
    ("someone is possessed", "Someone Is Possessed"),
    ("there's ghosts", "There's Ghosts"),
    ("there are razors", "There Are Razors"),
    ("there are 9/11 depictions", "There Are 9/11 Depictions"),
    ("there is copaganda", "There Is Copaganda"),
    ("there's incarceration", "There's Incarceration"),
    ("reality is unstable or unhinged", "Reality Is Unstable or Unhinged"),
    ("there's screaming", "There's Screaming"),
    ("there's fat jokes", "There's Fat Jokes"),
    (
        "there's ableist language or behavior",
        "There's Ableist Language or Behavior",
    ),
    ("there's a large age gap", "There's a Large Age Gap"),
    ("there's demons or Hell", "There's Demons or Hell"),
    ("religion is discussed", "Religion Is Discussed"),
    ("Santa (et al) is spoiled", "Santa (et al) Is Spoiled"),
]

TRIGGER_DICT = {
    "Potentially Scary Animals": [
        "there are spiders",
        "there are bugs",
        "there are snakes",
        "there are sharks",
        "there's an alligator/crocodile",
    ],
    "Bigotry": [
        "someone speaks hate speech",
        "someone says the n-word",
        "there's antisemitism",
        "a minority is misrepresented",
        "the black guy dies first",
        "there's blackface",
        "the r-slur is used",
    ],
    "Sexual Content": [
        "there is obscene language/gestures",
        "there is sexual content",
        "someone is sexually objectified",
        "there are nude scenes",
        "someone loses their virginity",
        "there are shower scenes",
        "rape is mentioned",
        "there's BDSM",
    ],
    "Pregnancy Issues": [
        "someone miscarries",
        "a baby is stillborn",
        "someone has an abortion",
        "a pregnant person dies",
        "there's anti-abortion themes",
    ],
    "Potentially Harmful Filmmaking (flashing lights, shaky cam, etc.)": [
        "shaky cam is used",
        "there's flashing lights or images",
        "there's misophonia",
    ],
    "Depiction of Medical Issues: Diseases and Phobias": [
        "needles/syringes are used",
        "there's a mental institution scene",
        "electro-therapy is used",
        "someone has cancer",
        "there's a hospital scene",
        "someone suffers from PTSD",
        "someone has an eating disorder",
        "autism is misrepresented",
        "someone has an anxiety attack",
        "there's body dysmorphia",
        "there's body dysphoria",
        "there's a claustrophobic scene",
        "a mentally ill person is violent",
        "there's ABA therapy",
        "someone has a mental illness",
        "D.I.D. Misrepresentation",
        "there's dissociation, depersonalization, or derealization",
        "someone has a meltdown",
        "someone has dementia/Alzheimer's",
        "someone is terminally ill",
        "someone has a chronic illness",
        "someone has a stroke",
        "somone has a seizure",
    ],
    "LGBT Issues & Problematic Depictions": [
        "a trans person is depicted predatorily",
        "there are transphobic slurs",
        "there's deadnaming or birthnaming",
        "an LGBT+ person is outed",
        "someone is misgendered",
        "there are homophobic slurs",
        "an LGBT person dies",
        "there's aphobia",
        "there's bisexual cheating",
    ],
    "Bodily Functions": [
        "someone poops on-screen",
        "someone vomits",
        "someone wets/soils themselves",
        "there's spitting",
        "there's farting",
        "there's menstruation",
    ],
    "Human Death": [
        "someone dies",
        "someone sacrifices themselves",
        "a family member dies",
        "a parent dies",
    ],
    "Excessive Violence": [
        "a woman is brutalized for spectacle",
        "someone is held under water",
        "there's torture",
        "there's eye mutilation",
        "there's excessive gore",
        "there's genital trauma/mutilation",
        "heads get squashed",
        "there's finger/toe mutilation",
        "there's body horror",
        "there's cannibalism",
        "someone is eaten",
        "someone is burned alive",
        "there are hangings",
        "there's decapitation",
        "someone is crushed to death",
        "there's amputation",
        "someone is buried alive",
        "someone's throat is mutilated",
        "someone falls to their death",
        "someone is stabbed",
        "someone dies by suicide",
        "someone drowns",
        "a car crashes",
        "a plane crashes",
        "there's blood/gore",
        "there's gun violence",
        "a person is hit by a car",
        "someone asphyxiates",
        "someone is kidnapped",
        "Someone attempts suicide",
        "someone self harms",
        "There's audio gore",
    ],
    "Violence": [
        "a woman gets slapped",
        "someone is beaten up by a bully",
        "teeth are damaged",
        "someone struggles to breathe",
        "someone breaks a bone",
        "there's Achilles Tendon injury",
        "hands are damaged",
        "someone dislocates something",
        "someone falls down stairs",
        "somebody is choked",
    ],
    "Abuse and Manipulation (including sexual)": [
        "Autism specific abuse",
        "there's domestic violence",
        "someone cheats",
        "the abused forgives their abuser",
        "someone gets gaslighted",
        "someone is stalked",
        "someone is abused with a belt",
        "someone is sexually assaulted",
        "someone is raped onscreen",
        "someone is restrained",
        "someone is drugged",
        "there are incestuous relationships",
    ],
    "Drug Usage / Abuse": [
        "there's addiction",
        "alcohol abuse",
        "someone uses drugs",
        "someone overdoses",
    ],
    "Child Abuse": [
        "a child is abandoned by a parent",
        "there's child abuse",
        "there's abusive parents",
        "there's pedophilia",
        "a minor is sexualized",
        "an infant is abducted",
    ],
    "Animal Harm / Death": [
        "animals are abused",
        "an animal dies",
        "animals were harmed in the making",
        "there's dog fighting",
        "there's a dead animal",
        "a pet dies",
        "there's bestiality",
    ],
}

STREAMING = [
    ("", "No Preference"),
    ("Amazon Prime Video", "Amazon Prime Video"),
    ("Apple TV Plus", "Apple TV Plus"),
    ("Criterion Channel", "Criterion Channel"),
    ("Crunchyroll", "Crunchyroll"),
    ("Disney Plus", "Disney Plus"),
    ("Max", "Max"),
    ("Hulu", "Hulu"),
    ("MUBI", "MUBI"),
    ("Netflix", "Netflix"),
    ("Paramount Plus", "Paramount Plus"),
    ("Peacock Premium", "Peacock Premium"),
    ("Shudder", "Shudder"),
]
