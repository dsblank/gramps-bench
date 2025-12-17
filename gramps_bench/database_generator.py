#
# Gramps - a GTK+/GNOME based genealogy program
#
# Copyright (C) 2024  Gramps contributors
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, see <https://www.gnu.org/licenses/>.
#

"""
Stand-alone function to generate Gramps databases for testing.

This module provides a function to create family tree databases
with various characteristics useful for testing filters and performance.
"""

import random
import os
import glob
from typing import Optional

GENERATOR_VERSION = 1

gramps_resources = os.environ.get("GRAMPS_RESOURCES")

if gramps_resources is None:
    raise Exception(
        "Warning: Could not find Gramps resource files. "
        "Set GRAMPS_RESOURCES environment variable."
    )

from gramps.gen.lib import (
    Person,
    Family,
    Name,
    Surname,
    Event,
    EventRef,
    EventType,
    Attribute,
    AttributeType,
    Note,
    NoteType,
    Date,
    Place,
    PlaceName,
    PlaceRef,
    PlaceType,
    Tag,
    ChildRef,
    ChildRefType,
    Source,
    Citation,
    Repository,
    RepoRef,
    RepositoryType,
    Media,
    MediaRef,
    Address,
    Location,
    PersonRef,
    FamilyRelType,
    NameOriginType,
    NameType,
)
from gramps.gen.db.utils import make_database
from gramps.gen.db.txn import DbTxn
from gramps.gen.db.dbconst import DBBACKEND
from gramps.cli.clidbman import CLIDbManager, NAME_FILE
from gramps.gen.dbstate import DbState


# Sample data for variety - Western names (expanded significantly)
FIRST_NAMES_MALE = [
    "James",
    "John",
    "Robert",
    "Michael",
    "William",
    "David",
    "Richard",
    "Joseph",
    "Thomas",
    "Charles",
    "Daniel",
    "Matthew",
    "Anthony",
    "Mark",
    "Donald",
    "Steven",
    "Paul",
    "Andrew",
    "Joshua",
    "Kenneth",
    "Kevin",
    "Brian",
    "George",
    "Edward",
    "Ronald",
    "Timothy",
    "Jason",
    "Jeffrey",
    "Ryan",
    "Jacob",
    "Gary",
    "Nicholas",
    "Eric",
    "Jonathan",
    "Stephen",
    "Larry",
    "Justin",
    "Scott",
    "Brandon",
    "Benjamin",
    "Samuel",
    "Frank",
    "Gregory",
    "Raymond",
    "Alexander",
    "Patrick",
    "Jack",
    "Dennis",
    "Jerry",
    "Tyler",
    "Aaron",
    "Jose",
    "Henry",
    "Adam",
    "Douglas",
    "Nathan",
    "Zachary",
    "Kyle",
    "Noah",
    "Ethan",
    "Jeremy",
    "Walter",
    "Christian",
    "Hunter",
    "Austin",
    "Sean",
    "Connor",
    "Mason",
    "Lucas",
    "Logan",
    "Owen",
    "Caleb",
    "Isaac",
    "Luke",
    "Wyatt",
    "Gavin",
    "Carter",
    "Julian",
    "Miles",
    "Eli",
    "Levi",
    "Nolan",
    "Colin",
    "Bennett",
    "Felix",
    "Jasper",
    "Theo",
    "Oscar",
]

FIRST_NAMES_FEMALE = [
    "Mary",
    "Patricia",
    "Jennifer",
    "Linda",
    "Elizabeth",
    "Barbara",
    "Susan",
    "Jessica",
    "Sarah",
    "Karen",
    "Nancy",
    "Lisa",
    "Betty",
    "Margaret",
    "Sandra",
    "Ashley",
    "Kimberly",
    "Emily",
    "Donna",
    "Michelle",
    "Carol",
    "Amanda",
    "Dorothy",
    "Melissa",
    "Deborah",
    "Stephanie",
    "Rebecca",
    "Sharon",
    "Laura",
    "Cynthia",
    "Kathleen",
    "Amy",
    "Angela",
    "Shirley",
    "Anna",
    "Brenda",
    "Pamela",
    "Emma",
    "Nicole",
    "Helen",
    "Samantha",
    "Katherine",
    "Christine",
    "Debra",
    "Rachel",
    "Carolyn",
    "Janet",
    "Virginia",
    "Maria",
    "Heather",
    "Diane",
    "Julie",
    "Joyce",
    "Victoria",
    "Kelly",
    "Christina",
    "Joan",
    "Evelyn",
    "Judith",
    "Megan",
    "Cheryl",
    "Andrea",
    "Hannah",
    "Jacqueline",
    "Martha",
    "Gloria",
    "Teresa",
    "Sara",
    "Janice",
    "Marie",
    "Julia",
    "Grace",
    "Judy",
    "Theresa",
    "Madison",
    "Beverly",
    "Denise",
    "Marilyn",
    "Amber",
    "Danielle",
    "Brittany",
    "Diana",
    "Abigail",
    "Jane",
    "Lori",
    "Olivia",
    "Lily",
    "Sophia",
    "Ava",
    "Isabella",
    "Mia",
    "Charlotte",
    "Amelia",
    "Harper",
    "Evelyn",
    "Aria",
    "Chloe",
    "Luna",
    "Zoe",
    "Stella",
    "Hazel",
    "Ellie",
    "Paisley",
]

SURNAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
    "Hernandez",
    "Lopez",
    "Wilson",
    "Anderson",
    "Thomas",
    "Taylor",
    "Moore",
    "Jackson",
    "Martin",
    "Lee",
    "Thompson",
    "White",
    "Harris",
    "Sanchez",
    "Clark",
    "Lewis",
    "Robinson",
    "Walker",
    "Young",
    "Allen",
    "King",
    "Wright",
    "Scott",
    "Torres",
    "Nguyen",
    "Hill",
    "Flores",
    "Green",
    "Adams",
    "Nelson",
    "Baker",
    "Hall",
    "Rivera",
    "Campbell",
    "Mitchell",
    "Carter",
    "Roberts",
    "Gomez",
    "Phillips",
    "Evans",
    "Turner",
    "Diaz",
    "Parker",
    "Cruz",
    "Edwards",
    "Collins",
    "Reyes",
    "Stewart",
    "Morris",
    "Rogers",
    "Reed",
    "Cook",
    "Morgan",
    "Bell",
    "Murphy",
    "Bailey",
    "Rivera",
    "Cooper",
    "Richardson",
    "Cox",
    "Howard",
    "Ward",
    "Torres",
    "Peterson",
    "Gray",
    "Ramirez",
    "James",
    "Watson",
    "Brooks",
    "Kelly",
    "Sanders",
    "Price",
    "Bennett",
    "Wood",
    "Barnes",
    "Ross",
    "Henderson",
    "Coleman",
    "Jenkins",
    "Perry",
    "Powell",
    "Long",
    "Patterson",
    "Hughes",
    "Flores",
    "Washington",
    "Butler",
    "Simmons",
    "Foster",
    "Gonzales",
    "Bryant",
    "Alexander",
    "Russell",
    "Griffin",
]

# Names from other cultures - Chinese (expanded)
CHINESE_FIRST_NAMES_MALE = [
    "Wei",
    "Ming",
    "Jian",
    "Hao",
    "Lei",
    "Jun",
    "Feng",
    "Tao",
    "Yong",
    "Bin",
    "Qiang",
    "Peng",
    "Xin",
    "Kai",
    "Yuan",
    "Bo",
    "Dong",
    "Hui",
    "Jie",
    "Long",
    "Xiang",
    "Yan",
    "Zhi",
    "Jie",
    "Kang",
    "Liang",
    "Ning",
    "Qing",
    "Rui",
    "Sheng",
    "Tian",
    "Wei",
    "Xing",
    "Yan",
    "Zhen",
    "An",
    "Bao",
    "Cheng",
    "De",
    "En",
    "Fu",
    "Gang",
    "Hong",
    "Jin",
    "Kun",
    "Ling",
    "Ming",
    "Ning",
    "Ping",
    "Qi",
]

CHINESE_FIRST_NAMES_FEMALE = [
    "Mei",
    "Li",
    "Xia",
    "Yan",
    "Fang",
    "Hui",
    "Jing",
    "Lan",
    "Min",
    "Ping",
    "Qing",
    "Rong",
    "Shan",
    "Ting",
    "Wen",
    "Xin",
    "Ying",
    "Zhen",
    "Ai",
    "Bing",
    "Chun",
    "Dan",
    "Fen",
    "Hong",
    "Jia",
    "Ling",
    "Na",
    "Qi",
    "Rui",
    "Shu",
    "Tao",
    "Wei",
    "Xia",
    "Yan",
    "Zhen",
    "An",
    "Bao",
    "Chun",
    "Dan",
    "Fang",
    "Hua",
    "Jing",
    "Lan",
    "Mei",
    "Na",
    "Ping",
    "Qing",
    "Rong",
    "Shan",
    "Ting",
]

CHINESE_SURNAMES = [
    "Wang",
    "Li",
    "Zhang",
    "Liu",
    "Chen",
    "Yang",
    "Huang",
    "Zhao",
    "Wu",
    "Zhou",
    "Xu",
    "Sun",
    "Ma",
    "Zhu",
    "Hu",
    "Guo",
    "He",
    "Gao",
    "Lin",
    "Luo",
    "Zhou",
    "Zheng",
    "Xie",
    "Han",
    "Tang",
    "Feng",
    "Yu",
    "Dong",
    "Xiao",
    "Cheng",
    "Cao",
    "Yuan",
    "Deng",
    "Xu",
    "Gu",
    "Lu",
    "Jiang",
    "Qian",
    "Pan",
    "Du",
    "Peng",
    "Jiang",
    "Jiang",
    "Wei",
    "Tao",
    "Jiang",
    "Jiang",
    "Jiang",
    "Jiang",
    "Jiang",
]

JAPANESE_FIRST_NAMES_MALE = [
    "Hiroshi",
    "Takeshi",
    "Kenji",
    "Yuki",
    "Satoshi",
    "Makoto",
    "Akira",
    "Daisuke",
    "Kenta",
    "Ryota",
    "Shota",
    "Yuto",
    "Riku",
    "Haruto",
    "Sota",
    "Ren",
    "Yuma",
    "Kaito",
    "Daiki",
    "Sho",
    "Kazuki",
    "Ryo",
    "Taro",
    "Jiro",
    "Ichiro",
    "Masato",
    "Tatsuya",
    "Naoki",
    "Koji",
    "Toshi",
    "Hiro",
    "Masa",
    "Taka",
    "Nobu",
    "Yoshi",
    "Kazu",
    "Shin",
    "Tomo",
]

JAPANESE_FIRST_NAMES_FEMALE = [
    "Yuki",
    "Sakura",
    "Aoi",
    "Hana",
    "Mei",
    "Akari",
    "Rin",
    "Yui",
    "Mio",
    "Emi",
    "Kana",
    "Mika",
    "Nana",
    "Rika",
    "Saya",
    "Maya",
    "Nozomi",
    "Ayaka",
    "Akiko",
    "Chie",
    "Eri",
    "Fumi",
    "Haru",
    "Kaori",
    "Keiko",
    "Michiko",
    "Naomi",
    "Rei",
    "Sachiko",
]

JAPANESE_SURNAMES = [
    "Tanaka",
    "Sato",
    "Suzuki",
    "Takahashi",
    "Watanabe",
    "Ito",
    "Yamamoto",
    "Nakamura",
    "Kobayashi",
    "Kato",
    "Yoshida",
    "Yamada",
    "Sasaki",
    "Yamaguchi",
    "Matsumoto",
    "Inoue",
    "Kimura",
    "Hayashi",
    "Shimizu",
    "Yamazaki",
    "Mori",
    "Abe",
    "Ikeda",
    "Hashimoto",
    "Yamashita",
    "Ishikawa",
    "Nakajima",
    "Maeda",
    "Fujita",
    "Ogawa",
    "Goto",
    "Okada",
]

ARABIC_FIRST_NAMES_MALE = [
    "Mohammed",
    "Ahmed",
    "Ali",
    "Hassan",
    "Omar",
    "Ibrahim",
    "Yusuf",
    "Khalid",
    "Abdullah",
    "Hamza",
    "Zain",
    "Tariq",
    "Rashid",
    "Malik",
    "Amir",
    "Samir",
    "Mahmoud",
    "Mustafa",
    "Hussein",
    "Karim",
    "Youssef",
    "Said",
    "Nasser",
    "Fadi",
    "Bilal",
    "Jamal",
    "Rami",
    "Tariq",
    "Waleed",
    "Zaid",
    "Adnan",
    "Farid",
]

ARABIC_FIRST_NAMES_FEMALE = [
    "Fatima",
    "Aisha",
    "Mariam",
    "Zainab",
    "Khadija",
    "Amina",
    "Layla",
    "Noor",
    "Sara",
    "Yasmin",
    "Hana",
    "Leila",
    "Salma",
    "Nadia",
    "Rania",
    "Dina",
    "Amira",
    "Nour",
    "Lina",
    "Maya",
    "Rana",
    "Sana",
    "Yara",
    "Zeinab",
    "Hala",
    "Lamia",
    "Mona",
    "Nada",
    "Rana",
    "Samira",
    "Tara",
    "Wafa",
]

ARABIC_SURNAMES = [
    "Al-Ahmad",
    "Al-Hassan",
    "Al-Mahmoud",
    "Al-Rashid",
    "Al-Zahra",
    "Ibrahim",
    "Khalil",
    "Malik",
    "Nasser",
    "Omar",
    "Qureshi",
    "Rahman",
    "Said",
    "Tariq",
    "Yusuf",
    "Abbas",
    "Al-Ali",
    "Al-Bakr",
    "Al-Farouk",
    "Al-Hakim",
    "Al-Mansour",
    "Al-Said",
    "Al-Zahrani",
    "Bashir",
    "Fahd",
    "Haddad",
    "Jamil",
    "Khalaf",
    "Mahmoud",
    "Naji",
]

# Additional cultures
INDIAN_FIRST_NAMES_MALE = [
    "Arjun",
    "Rohan",
    "Aryan",
    "Vikram",
    "Rahul",
    "Amit",
    "Raj",
    "Karan",
    "Siddharth",
    "Aditya",
    "Ankit",
    "Ravi",
    "Vishal",
    "Nikhil",
    "Pranav",
    "Krishna",
    "Shiva",
    "Dev",
    "Gaurav",
    "Harsh",
    "Ishaan",
    "Jay",
    "Kunal",
    "Laksh",
    "Manish",
    "Neel",
    "Om",
    "Parth",
    "Rishabh",
    "Sahil",
    "Tanish",
    "Utkarsh",
    "Varun",
    "Yash",
]

INDIAN_FIRST_NAMES_FEMALE = [
    "Priya",
    "Ananya",
    "Kavya",
    "Riya",
    "Sneha",
    "Aishwarya",
    "Divya",
    "Meera",
    "Pooja",
    "Radha",
    "Sita",
    "Tara",
    "Uma",
    "Vidya",
    "Anjali",
    "Bhavna",
    "Chitra",
    "Deepika",
    "Esha",
    "Gayatri",
    "Hema",
    "Isha",
    "Jyoti",
    "Kiran",
    "Lakshmi",
    "Maya",
    "Neha",
    "Ojasvi",
    "Padmini",
    "Rekha",
    "Shreya",
    "Tara",
]

INDIAN_SURNAMES = [
    "Patel",
    "Sharma",
    "Kumar",
    "Singh",
    "Gupta",
    "Reddy",
    "Rao",
    "Mehta",
    "Verma",
    "Jain",
    "Agarwal",
    "Malhotra",
    "Chopra",
    "Kapoor",
    "Shah",
    "Desai",
    "Joshi",
    "Bhatt",
    "Nair",
    "Iyer",
    "Menon",
    "Pillai",
    "Krishnan",
    "Narayanan",
    "Raman",
    "Subramanian",
    "Venkatesh",
    "Gopal",
    "Lakshman",
    "Murthy",
    "Ramesh",
    "Suresh",
]

RUSSIAN_FIRST_NAMES_MALE = [
    "Alexander",
    "Dmitri",
    "Ivan",
    "Sergei",
    "Andrei",
    "Mikhail",
    "Vladimir",
    "Nikolai",
    "Alexei",
    "Pavel",
    "Yuri",
    "Maxim",
    "Anton",
    "Roman",
    "Denis",
    "Viktor",
    "Igor",
    "Oleg",
    "Boris",
    "Anatoly",
    "Grigory",
    "Fyodor",
    "Konstantin",
    "Leonid",
    "Mikhail",
    "Nikita",
    "Pavel",
    "Ruslan",
    "Stanislav",
    "Timur",
    "Vadim",
    "Yaroslav",
]

RUSSIAN_FIRST_NAMES_FEMALE = [
    "Anna",
    "Maria",
    "Elena",
    "Olga",
    "Tatiana",
    "Natalia",
    "Svetlana",
    "Irina",
    "Ekaterina",
    "Yulia",
    "Anastasia",
    "Daria",
    "Polina",
    "Sofia",
    "Vera",
    "Ludmila",
    "Galina",
    "Larisa",
    "Marina",
    "Nina",
    "Raisa",
    "Tamara",
    "Valentina",
    "Yelena",
    "Zoya",
    "Alla",
    "Bella",
    "Diana",
    "Inna",
    "Ksenia",
    "Lilia",
    "Margarita",
]

RUSSIAN_SURNAMES = [
    "Ivanov",
    "Petrov",
    "Sidorov",
    "Smirnov",
    "Kuznetsov",
    "Popov",
    "Sokolov",
    "Lebedev",
    "Kozlov",
    "Novikov",
    "Morozov",
    "Petrov",
    "Volkov",
    "Alekseev",
    "Lebedev",
    "Semenov",
    "Egorov",
    "Pavlov",
    "Kozlov",
    "Stepanov",
    "Nikolaev",
    "Orlov",
    "Andreev",
    "Makarov",
    "Nikitin",
    "Zakharov",
    "Zaytsev",
    "Solovyov",
    "Borisov",
    "Korolev",
    "Gerasimov",
    "Ponomarev",
]

SPANISH_FIRST_NAMES_MALE = [
    "Carlos",
    "Jose",
    "Miguel",
    "Juan",
    "Francisco",
    "Antonio",
    "Manuel",
    "Pedro",
    "Luis",
    "Rafael",
    "Javier",
    "Fernando",
    "Diego",
    "Sergio",
    "Ricardo",
    "Alberto",
    "Roberto",
    "Eduardo",
    "Daniel",
    "Alejandro",
    "Andres",
    "Gabriel",
    "Hector",
    "Jorge",
    "Mario",
    "Oscar",
    "Pablo",
    "Ramon",
    "Victor",
    "Adrian",
    "Cesar",
    "Enrique",
]

SPANISH_FIRST_NAMES_FEMALE = [
    "Maria",
    "Carmen",
    "Ana",
    "Laura",
    "Isabel",
    "Patricia",
    "Monica",
    "Sandra",
    "Andrea",
    "Elena",
    "Rosa",
    "Marta",
    "Cristina",
    "Lucia",
    "Paula",
    "Sofia",
    "Beatriz",
    "Dolores",
    "Esperanza",
    "Francisca",
    "Gloria",
    "Ines",
    "Juana",
    "Lourdes",
    "Margarita",
    "Natalia",
    "Olga",
    "Pilar",
    "Raquel",
    "Teresa",
    "Victoria",
    "Yolanda",
]

SPANISH_SURNAMES = [
    "Garcia",
    "Rodriguez",
    "Gonzalez",
    "Fernandez",
    "Lopez",
    "Martinez",
    "Sanchez",
    "Perez",
    "Gomez",
    "Martin",
    "Jimenez",
    "Ruiz",
    "Hernandez",
    "Diaz",
    "Moreno",
    "Alvarez",
    "Munoz",
    "Romero",
    "Alonso",
    "Gutierrez",
    "Navarro",
    "Torres",
    "Dominguez",
    "Vazquez",
    "Ramos",
    "Gil",
    "Ramirez",
    "Serrano",
    "Blanco",
    "Suarez",
    "Molina",
    "Morales",
]

GERMAN_FIRST_NAMES_MALE = [
    "Hans",
    "Peter",
    "Klaus",
    "Wolfgang",
    "Michael",
    "Thomas",
    "Andreas",
    "Stefan",
    "Markus",
    "Christian",
    "Matthias",
    "Martin",
    "Frank",
    "Uwe",
    "Jens",
    "Oliver",
    "Daniel",
    "Sebastian",
    "Florian",
    "Alexander",
    "Maximilian",
    "Felix",
    "Lukas",
    "Jonas",
    "Noah",
    "Ben",
    "Paul",
    "Leon",
    "Finn",
    "Emil",
    "Anton",
    "Theo",
]

GERMAN_FIRST_NAMES_FEMALE = [
    "Anna",
    "Maria",
    "Elisabeth",
    "Ursula",
    "Monika",
    "Petra",
    "Sabine",
    "Andrea",
    "Nicole",
    "Stephanie",
    "Julia",
    "Katharina",
    "Lisa",
    "Sarah",
    "Laura",
    "Hannah",
    "Emma",
    "Mia",
    "Sophia",
    "Emilia",
    "Lina",
    "Clara",
    "Lea",
    "Marie",
    "Ella",
    "Mila",
    "Frieda",
    "Luise",
    "Amelie",
    "Ida",
    "Leni",
    "Mathilda",
    "Charlotte",
]

GERMAN_SURNAMES = [
    "Muller",
    "Schmidt",
    "Schneider",
    "Fischer",
    "Weber",
    "Meyer",
    "Wagner",
    "Becker",
    "Schulz",
    "Hoffmann",
    "Schafer",
    "Koch",
    "Bauer",
    "Richter",
    "Klein",
    "Wolf",
    "Schroder",
    "Neumann",
    "Schwarz",
    "Zimmermann",
    "Braun",
    "Kruger",
    "Hofmann",
    "Hartmann",
    "Lange",
    "Schmitt",
    "Werner",
    "Schmitz",
    "Krause",
    "Meier",
    "Lehmann",
    "Schmid",
]

KOREAN_FIRST_NAMES_MALE = [
    "Min-jun",
    "Seo-jun",
    "Do-yoon",
    "Ji-ho",
    "Jun-seo",
    "Si-woo",
    "Ha-joon",
    "Yoon-seo",
    "Jin-woo",
    "Eun-woo",
    "Hyun-woo",
    "Min-ho",
    "Seung-ho",
    "Tae-hyun",
    "Woo-jin",
    "Ye-jun",
    "Jae-hyun",
    "Sang-min",
    "Ki-tae",
    "Dong-hyun",
    "Young-min",
    "Hyeon-jun",
    "Seung-min",
    "Jun-ho",
]

KOREAN_FIRST_NAMES_FEMALE = [
    "Seo-yeon",
    "Ji-woo",
    "Seo-yun",
    "Chae-won",
    "Ha-yoon",
    "Soo-ah",
    "Min-seo",
    "Yoo-na",
    "Eun-ji",
    "Hae-won",
    "Ji-min",
    "So-min",
    "Ye-rin",
    "Da-eun",
    "Na-yoon",
    "Seo-hyun",
    "Ji-yu",
    "Hye-won",
    "Min-ju",
    "Yeon-woo",
    "Seo-jin",
    "Ha-rin",
    "So-yeon",
    "Ji-ah",
]

KOREAN_SURNAMES = [
    "Kim",
    "Lee",
    "Park",
    "Choi",
    "Jung",
    "Kang",
    "Cho",
    "Yoon",
    "Jang",
    "Lim",
    "Han",
    "Shin",
    "Oh",
    "Hwang",
    "Moon",
    "Song",
    "Bae",
    "Kwon",
    "Ryu",
    "Baek",
    "Ahn",
    "Seo",
    "Yoo",
    "Jeong",
    "Hong",
    "Nam",
    "Son",
    "Woo",
    "Chung",
    "Koo",
]

# Syllable-based name generator components (expanded significantly)
FIRST_NAME_SYLLABLES_START = [
    "Al",
    "Ben",
    "Cal",
    "Dan",
    "Ed",
    "Fran",
    "Gar",
    "Hen",
    "Ian",
    "Jan",
    "Ken",
    "Len",
    "Mar",
    "Nan",
    "Oli",
    "Pat",
    "Quin",
    "Rob",
    "Sam",
    "Tom",
    "Val",
    "Wes",
    "Xan",
    "Yor",
    "Zac",
    "Bri",
    "Chr",
    "Dav",
    "Eli",
    "Fel",
    "Gav",
    "Hal",
    "Ivo",
    "Jax",
    "Kai",
    "Leo",
    "Max",
    "Ned",
    "Owen",
    "Pax",
    "Quin",
    "Ray",
    "Sid",
    "Tad",
    "Ugo",
    "Van",
    "Wyn",
    "Xav",
    "Yan",
    "Zed",
    "Abe",
    "Bev",
    "Cam",
    "Del",
    "Eve",
    "Fay",
    "Gus",
    "Hal",
    "Ira",
    "Jay",
    "Kit",
    "Lou",
    "Mae",
    "Ned",
    "Ora",
    "Pam",
    "Quo",
    "Rex",
    "Sue",
    "Ted",
    "Uma",
    "Vic",
    "Wes",
    "Xia",
    "Yve",
    "Zoe",
    "Ace",
    "Bea",
    "Coy",
    "Dax",
]

FIRST_NAME_SYLLABLES_MID = [
    "an",
    "el",
    "in",
    "on",
    "er",
    "ar",
    "or",
    "en",
    "al",
    "il",
    "ab",
    "ad",
    "am",
    "at",
    "ed",
    "em",
    "et",
    "id",
    "im",
    "it",
    "ac",
    "ag",
    "ak",
    "ap",
    "as",
    "ax",
    "ay",
    "az",
    "eb",
    "ec",
    "ef",
    "eg",
    "ek",
    "ep",
    "es",
    "ex",
    "ey",
    "ez",
    "ib",
    "ic",
    "if",
    "ig",
    "ik",
    "ip",
    "is",
    "ix",
    "iy",
    "iz",
    "ob",
    "oc",
    "of",
    "og",
    "ok",
    "op",
    "os",
    "ox",
    "oy",
    "oz",
    "ub",
    "uc",
    "uf",
    "ug",
    "uk",
    "up",
    "us",
    "ux",
    "uy",
    "uz",
    "la",
    "le",
    "li",
    "lo",
    "lu",
    "ly",
    "ma",
    "me",
    "mi",
    "mo",
    "mu",
    "my",
]

FIRST_NAME_SYLLABLES_END = [
    "a",
    "e",
    "i",
    "o",
    "y",
    "an",
    "en",
    "in",
    "on",
    "er",
    "ar",
    "or",
    "el",
    "al",
    "ie",
    "ey",
    "ly",
    "ny",
    "ry",
    "ty",
    "ah",
    "eh",
    "ih",
    "oh",
    "uh",
    "ia",
    "ea",
    "ua",
    "ae",
    "oe",
    "ay",
    "ey",
    "oy",
    "uy",
    "aw",
    "ew",
    "ow",
    "as",
    "es",
    "is",
    "os",
    "us",
    "at",
    "et",
    "it",
    "ot",
    "ut",
    "ak",
    "ek",
    "ik",
    "ok",
    "uk",
    "am",
    "em",
    "im",
    "om",
    "um",
    "ap",
    "ep",
    "ip",
]

SURNAME_SYLLABLES_START = [
    "And",
    "Bar",
    "Car",
    "Dav",
    "Edw",
    "Fis",
    "Gar",
    "Har",
    "Irv",
    "Jac",
    "Kel",
    "Law",
    "Mac",
    "Nor",
    "Owe",
    "Par",
    "Qui",
    "Rob",
    "Smi",
    "Tay",
    "Und",
    "Vil",
    "Wal",
    "Xan",
    "Yor",
    "Zim",
    "Bak",
    "Cla",
    "Dra",
    "Eve",
    "Fal",
    "Gol",
    "Hal",
    "Ive",
    "Jol",
    "Kal",
    "Lal",
    "Mal",
    "Nal",
    "Oal",
    "Pal",
    "Qal",
    "Ral",
    "Sal",
    "Tal",
    "Ual",
    "Val",
    "Wal",
    "Xal",
    "Yal",
    "Zal",
    "Abr",
    "Bac",
    "Cad",
    "Daf",
    "Eag",
    "Fah",
    "Gai",
    "Haj",
    "Iak",
    "Jak",
    "Kak",
    "Lak",
    "Mak",
    "Nak",
    "Oak",
    "Pak",
    "Qak",
    "Rak",
    "Sak",
]

SURNAME_SYLLABLES_MID = [
    "er",
    "son",
    "ton",
    "man",
    "ing",
    "ell",
    "all",
    "ock",
    "ick",
    "ett",
    "ard",
    "art",
    "ort",
    "ert",
    "elt",
    "ald",
    "old",
    "olt",
    "ult",
    "ist",
    "est",
    "ast",
    "ost",
    "ust",
    "aft",
    "eft",
    "ift",
    "oft",
    "ant",
    "ent",
    "int",
    "ont",
    "unt",
    "and",
    "end",
    "ind",
    "ond",
    "und",
    "ang",
    "eng",
    "ing",
    "ong",
    "ung",
    "ank",
    "enk",
    "ink",
    "onk",
    "unk",
    "ash",
    "esh",
    "ish",
    "osh",
    "ush",
    "ath",
    "eth",
    "ith",
    "oth",
    "uth",
    "ach",
    "ech",
]

SURNAME_SYLLABLES_END = [
    "er",
    "son",
    "ton",
    "man",
    "ing",
    "ell",
    "all",
    "ock",
    "ick",
    "ett",
    "ard",
    "art",
    "ort",
    "ert",
    "elt",
    "ald",
    "old",
    "olt",
    "ult",
    "ist",
    "s",
    "es",
    "y",
    "ey",
    "ly",
    "ny",
    "ry",
    "ty",
    "le",
    "ne",
    "ge",
    "ke",
    "me",
    "pe",
    "re",
    "se",
    "te",
    "ve",
    "we",
    "ze",
    "an",
    "en",
    "in",
    "on",
    "un",
    "al",
    "el",
    "il",
    "ol",
    "ul",
    "am",
    "em",
    "im",
    "om",
    "um",
    "ap",
    "ep",
    "ip",
    "op",
    "up",
]


def generate_random_first_name(gender: int) -> str:
    """
    Generate a random first name using syllables or from various cultures.

    Args:
        gender: Person.MALE, Person.FEMALE, Person.UNKNOWN, or Person.OTHER

    Returns:
        A randomly generated first name
    """
    # 70% chance of using syllable-based generation for more variation, 30% chance of using real names
    if random.random() < 0.7:
        # Generate using syllables
        if gender == Person.MALE:
            # 2-3 syllables for male names
            num_syllables = random.choice([2, 3])
            name = random.choice(FIRST_NAME_SYLLABLES_START)
            for _ in range(num_syllables - 2):
                name += random.choice(FIRST_NAME_SYLLABLES_MID)
            name += random.choice(FIRST_NAME_SYLLABLES_END)
            return name.capitalize()
        elif gender == Person.FEMALE:
            # 2-3 syllables for female names, often ending in 'a' or 'e'
            num_syllables = random.choice([2, 3])
            name = random.choice(FIRST_NAME_SYLLABLES_START)
            for _ in range(num_syllables - 2):
                name += random.choice(FIRST_NAME_SYLLABLES_MID)
            # Female names often end with softer sounds
            female_endings = [
                "a",
                "e",
                "ia",
                "ie",
                "ey",
                "ly",
                "ny",
            ] + FIRST_NAME_SYLLABLES_END
            name += random.choice(female_endings)
            return name.capitalize()
        else:
            # For UNKNOWN or OTHER, use either pattern
            return generate_random_first_name(
                random.choice([Person.MALE, Person.FEMALE])
            )
    else:
        # Use real names from various cultures (expanded to 8 cultures)
        culture = random.choice(
            [
                "western",
                "chinese",
                "japanese",
                "arabic",
                "indian",
                "russian",
                "spanish",
                "german",
                "korean",
            ]
        )

        if culture == "western":
            if gender == Person.MALE:
                return random.choice(FIRST_NAMES_MALE)
            elif gender == Person.FEMALE:
                return random.choice(FIRST_NAMES_FEMALE)
            else:
                return random.choice(FIRST_NAMES_MALE + FIRST_NAMES_FEMALE)
        elif culture == "chinese":
            if gender == Person.MALE:
                return random.choice(CHINESE_FIRST_NAMES_MALE)
            elif gender == Person.FEMALE:
                return random.choice(CHINESE_FIRST_NAMES_FEMALE)
            else:
                return random.choice(
                    CHINESE_FIRST_NAMES_MALE + CHINESE_FIRST_NAMES_FEMALE
                )
        elif culture == "japanese":
            if gender == Person.MALE:
                return random.choice(JAPANESE_FIRST_NAMES_MALE)
            elif gender == Person.FEMALE:
                return random.choice(JAPANESE_FIRST_NAMES_FEMALE)
            else:
                return random.choice(
                    JAPANESE_FIRST_NAMES_MALE + JAPANESE_FIRST_NAMES_FEMALE
                )
        elif culture == "arabic":
            if gender == Person.MALE:
                return random.choice(ARABIC_FIRST_NAMES_MALE)
            elif gender == Person.FEMALE:
                return random.choice(ARABIC_FIRST_NAMES_FEMALE)
            else:
                return random.choice(
                    ARABIC_FIRST_NAMES_MALE + ARABIC_FIRST_NAMES_FEMALE
                )
        elif culture == "indian":
            if gender == Person.MALE:
                return random.choice(INDIAN_FIRST_NAMES_MALE)
            elif gender == Person.FEMALE:
                return random.choice(INDIAN_FIRST_NAMES_FEMALE)
            else:
                return random.choice(
                    INDIAN_FIRST_NAMES_MALE + INDIAN_FIRST_NAMES_FEMALE
                )
        elif culture == "russian":
            if gender == Person.MALE:
                return random.choice(RUSSIAN_FIRST_NAMES_MALE)
            elif gender == Person.FEMALE:
                return random.choice(RUSSIAN_FIRST_NAMES_FEMALE)
            else:
                return random.choice(
                    RUSSIAN_FIRST_NAMES_MALE + RUSSIAN_FIRST_NAMES_FEMALE
                )
        elif culture == "spanish":
            if gender == Person.MALE:
                return random.choice(SPANISH_FIRST_NAMES_MALE)
            elif gender == Person.FEMALE:
                return random.choice(SPANISH_FIRST_NAMES_FEMALE)
            else:
                return random.choice(
                    SPANISH_FIRST_NAMES_MALE + SPANISH_FIRST_NAMES_FEMALE
                )
        elif culture == "german":
            if gender == Person.MALE:
                return random.choice(GERMAN_FIRST_NAMES_MALE)
            elif gender == Person.FEMALE:
                return random.choice(GERMAN_FIRST_NAMES_FEMALE)
            else:
                return random.choice(
                    GERMAN_FIRST_NAMES_MALE + GERMAN_FIRST_NAMES_FEMALE
                )
        else:  # korean
            if gender == Person.MALE:
                return random.choice(KOREAN_FIRST_NAMES_MALE)
            elif gender == Person.FEMALE:
                return random.choice(KOREAN_FIRST_NAMES_FEMALE)
            else:
                return random.choice(
                    KOREAN_FIRST_NAMES_MALE + KOREAN_FIRST_NAMES_FEMALE
                )


def generate_random_surname() -> str:
    """
    Generate a random surname using syllables or from various cultures.

    Returns:
        A randomly generated surname
    """
    # 70% chance of using syllable-based generation for more variation, 30% chance of using real names
    if random.random() < 0.7:
        # Generate using syllables (2-3 syllables)
        num_syllables = random.choice([2, 3])
        surname = random.choice(SURNAME_SYLLABLES_START)
        for _ in range(num_syllables - 2):
            surname += random.choice(SURNAME_SYLLABLES_MID)
        surname += random.choice(SURNAME_SYLLABLES_END)
        return surname.capitalize()
    else:
        # Use real surnames from various cultures (expanded to 8 cultures)
        culture = random.choice(
            [
                "western",
                "chinese",
                "japanese",
                "arabic",
                "indian",
                "russian",
                "spanish",
                "german",
                "korean",
            ]
        )

        if culture == "western":
            return random.choice(SURNAMES)
        elif culture == "chinese":
            return random.choice(CHINESE_SURNAMES)
        elif culture == "japanese":
            return random.choice(JAPANESE_SURNAMES)
        elif culture == "arabic":
            return random.choice(ARABIC_SURNAMES)
        elif culture == "indian":
            return random.choice(INDIAN_SURNAMES)
        elif culture == "russian":
            return random.choice(RUSSIAN_SURNAMES)
        elif culture == "spanish":
            return random.choice(SPANISH_SURNAMES)
        elif culture == "german":
            return random.choice(GERMAN_SURNAMES)
        else:  # korean
            return random.choice(KOREAN_SURNAMES)


EVENT_TYPES = [
    EventType.BIRTH,
    EventType.DEATH,
    EventType.MARRIAGE,
    EventType.DIVORCE,
    EventType.BAPTISM,
    EventType.BURIAL,
    EventType.CENSUS,
    EventType.OCCUPATION,
    EventType.RESIDENCE,
    EventType.EDUCATION,
    EventType.MILITARY_SERV,
    EventType.EMIGRATION,
    EventType.IMMIGRATION,
]

ATTRIBUTE_TYPES = [
    AttributeType.CUSTOM,
    AttributeType.NUM_CHILD,
    AttributeType.CASTE,
    AttributeType.DESCRIPTION,
    AttributeType.ID,
    AttributeType.NATIONAL,
    AttributeType.OCCUPATION,
    AttributeType.SSN,
    AttributeType.AGE,
    AttributeType.FATHER_AGE,
    AttributeType.MOTHER_AGE,
    AttributeType.NICKNAME,
    AttributeType.TIME,
]

NOTE_TYPES = [
    NoteType.GENERAL,
    NoteType.ADDRESS,
    NoteType.ASSOCIATION,
    NoteType.CUSTOM,
    NoteType.EVENT,
    NoteType.FAMILY,
    NoteType.LDS,
    NoteType.MEDIA,
    NoteType.PERSON,
    NoteType.PLACE,
    NoteType.RESEARCH,
    NoteType.SOURCE_TEXT,
    NoteType.TRANSCRIPT,
    NoteType.ANALYSIS,
    NoteType.ATTRIBUTE,
    NoteType.CITATION,
    NoteType.HTML_CODE,
    NoteType.REPO,
    NoteType.REPORT_TEXT,
    NoteType.SOURCE,
    NoteType.TODO,
]


def _get_canonical_tag_handle(db, tag_name, tags_dict, trans=None):
    """Get the canonical tag handle that get_tag_from_name would return."""
    canonical_tag = db.get_tag_from_name(tag_name)
    if canonical_tag:
        return canonical_tag.handle
    # Fallback to the tag from our dict if get_tag_from_name doesn't find it
    if tag_name in tags_dict:
        return tags_dict[tag_name]
    # Create new tag if it doesn't exist
    if trans is not None:
        tag = Tag()
        tag.set_name(tag_name)
        tag_handle = db.add_tag(tag, trans)
        tags_dict[tag_name] = tag_handle
        return tag_handle
    return None


def _create_note_with_tags_and_privacy(
    db, trans, note_text, note_type, tags, tag_chance=0.3, privacy_chance=0.1
):
    """Create a note with optional tags and privacy, then return its handle."""
    note = Note()
    note.set_type(note_type)
    note.set(note_text)
    note_handle = db.add_note(note, trans)
    # Reload note and add tags/privacy after adding to database
    note = db.get_note_from_handle(note_handle)
    # Add tags to note - for HasTag rule
    if tags and random.random() < tag_chance:
        tag_name = random.choice(list(tags.keys()))
        tag_handle = _get_canonical_tag_handle(db, tag_name, tags, trans)
        if tag_handle:
            note.add_tag(tag_handle)
    # Add privacy flag to note - for NotePrivate rule
    if random.random() < privacy_chance:
        note.set_privacy(True)
    db.commit_note(note, trans)
    return note_handle


def generate_database(
    num_people: int,
    db_path: Optional[str] = None,
    dbid: str = "sqlite",
    seed: Optional[int] = None,
) -> str:
    """
    Generate a Gramps database with specified characteristics.

    This function creates a database with:
    - Approximately num_people people
    - ~1% of people are totally disconnected (no families, no parents)
    - Two families that are not connected to each other or the main tree
    - Variety in attributes to match filter rules:
      * Gender: MALE (1), FEMALE (0), UNKNOWN (2), OTHER (3)
      * Events: birth, death, marriage, etc.
      * Attributes: various types
      * Notes: various types
      * Addresses, tags, alternate names, etc.

    Args:
        num_people: Approximate number of people to create
        db_path: Path where to create the database (if None, uses Gramps default)
        dbid: Database backend ID (default: "sqlite")
        seed: Random seed for reproducibility. If provided, the same seed will
              generate an identical database. This is useful for creating exact
              duplicates of a tree for testing purposes.

    Returns:
        Path to the created database directory
    """
    if seed is None:
        seed = random.randint(100_000, 999_999)

    random.seed(seed)

    dbstate = DbState()
    dbman = CLIDbManager(dbstate)

    # Create database - use provided path or Gramps default
    db_name = f"gen-{num_people}, random-{seed}, version-{GENERATOR_VERSION}"
    if db_path is None:
        # Use Gramps default database directory (same as create_new_db_cli does)
        dirpath, _name = dbman.create_new_db_cli(db_name, dbid=dbid)
    else:
        # Use provided path - create directory structure manually
        os.makedirs(db_path, exist_ok=True)
        path_name = os.path.join(db_path, NAME_FILE)
        with open(path_name, "w", encoding="utf8") as name_file:
            name_file.write(db_name)

        backend_path = os.path.join(db_path, DBBACKEND)
        with open(backend_path, "w", encoding="utf8") as backend_file:
            backend_file.write(dbid)

        dirpath = db_path
    db = make_database(dbid)
    db.load(dirpath, None)

    # Calculate distribution
    num_disconnected = max(1, int(num_people * 0.01))  # ~1% disconnected
    num_connected = (
        num_people - num_disconnected - 4
    )  # Reserve 4 for unconnected families
    num_unconnected_family = 4  # 2 families of 2 people each

    people_handles = []
    families_handles = []

    try:
        with DbTxn("Generate database", db, batch=True) as trans:
            # Create tags for variety - reuse existing tags if they exist
            tags = {}
            tag_names = ["Important", "Verified", "Research", "DNA", "Private"]
            for tag_name in tag_names:
                # Check if tag already exists
                existing_tag = db.get_tag_from_name(tag_name)
                if existing_tag:
                    # Reuse existing tag
                    tags[tag_name] = existing_tag.handle
                else:
                    # Create new tag
                    tag = Tag()
                    tag.set_name(tag_name)
                    tag_handle = db.add_tag(tag, trans)
                    tags[tag_name] = tag_handle

            # Create places - increased number and add hierarchy with enclosed_by/encloses
            print("Generating places...")
            places = []
            # Create more places - cities, states, countries
            city_names = [
                # Major US cities
                "New York",
                "Los Angeles",
                "Chicago",
                "Houston",
                "Phoenix",
                "Philadelphia",
                "San Antonio",
                "San Diego",
                "Dallas",
                "San Jose",
                "Austin",
                "Jacksonville",
                "San Francisco",
                "Indianapolis",
                "Columbus",
                "Fort Worth",
                "Charlotte",
                "Seattle",
                "Denver",
                "Washington",
                "Boston",
                "El Paso",
                "Detroit",
                "Nashville",
                "Memphis",
                "Portland",
                "Oklahoma City",
                "Las Vegas",
                "Louisville",
                "Baltimore",
                "Milwaukee",
                "Albuquerque",
                "Tucson",
                "Fresno",
                "Sacramento",
                "Kansas City",
                "Mesa",
                "Atlanta",
                "Omaha",
                "Colorado Springs",
                "Raleigh",
                "Virginia Beach",
                "Miami",
                "Oakland",
                "Minneapolis",
                "Tulsa",
                "Cleveland",
                "Wichita",
                "Arlington",
                "Tampa",
                "New Orleans",
                # Major European cities
                "London",
                "Paris",
                "Berlin",
                "Madrid",
                "Rome",
                "Amsterdam",
                "Vienna",
                "Prague",
                "Stockholm",
                "Oslo",
                "Copenhagen",
                "Helsinki",
                "Warsaw",
                "Budapest",
                "Lisbon",
                "Dublin",
                "Brussels",
                "Zurich",
                "Geneva",
                "Luxembourg",
                "Monaco",
                "Vatican",
                "San Marino",
                "Andorra",
                "Liechtenstein",
                "Barcelona",
                "Munich",
                "Milan",
                "Naples",
                "Turin",
                "Florence",
                "Venice",
                "Marseille",
                "Lyon",
                "Toulouse",
                "Nice",
                "Bordeaux",
                "Hamburg",
                "Frankfurt",
                "Cologne",
                "Stuttgart",
                "Düsseldorf",
                "Dortmund",
                "Essen",
                "Leipzig",
                "Bremen",
                "Dresden",
                "Manchester",
                "Birmingham",
                "Liverpool",
                "Leeds",
                "Glasgow",
                "Edinburgh",
                "Belfast",
                "Cardiff",
                "Rotterdam",
                "The Hague",
                "Utrecht",
                "Eindhoven",
                "Groningen",
                "Antwerp",
                "Ghent",
                "Bruges",
                "Brussels",
                "Zurich",
                "Geneva",
                "Basel",
                "Bern",
                "Lausanne",
                "Vienna",
                "Graz",
                "Linz",
                "Salzburg",
                "Innsbruck",
                "Prague",
                "Brno",
                "Ostrava",
                "Budapest",
                "Debrecen",
                "Szeged",
                "Warsaw",
                "Krakow",
                "Gdansk",
                "Wroclaw",
                "Poznan",
                "Stockholm",
                "Gothenburg",
                "Malmö",
                "Uppsala",
                "Oslo",
                "Bergen",
                "Trondheim",
                "Stavanger",
                "Copenhagen",
                "Aarhus",
                "Odense",
                "Aalborg",
                "Helsinki",
                "Tampere",
                "Turku",
                "Oulu",
                # Major Asian cities
                "Tokyo",
                "Osaka",
                "Yokohama",
                "Nagoya",
                "Sapporo",
                "Fukuoka",
                "Kobe",
                "Kyoto",
                "Seoul",
                "Busan",
                "Incheon",
                "Daegu",
                "Daejeon",
                "Gwangju",
                "Shanghai",
                "Beijing",
                "Guangzhou",
                "Shenzhen",
                "Chengdu",
                "Chongqing",
                "Hangzhou",
                "Wuhan",
                "Xi'an",
                "Nanjing",
                "Tianjin",
                "Suzhou",
                "Dongguan",
                "Foshan",
                "Shenyang",
                "Qingdao",
                "Mumbai",
                "Delhi",
                "Bangalore",
                "Hyderabad",
                "Ahmedabad",
                "Chennai",
                "Kolkata",
                "Surat",
                "Pune",
                "Jaipur",
                "Lucknow",
                "Kanpur",
                "Nagpur",
                "Indore",
                "Thane",
                "Bhopal",
                "Visakhapatnam",
                "Patna",
                "Vadodara",
                "Ghaziabad",
                "Ludhiana",
                "Agra",
                "Bangkok",
                "Chiang Mai",
                "Phuket",
                "Pattaya",
                "Singapore",
                "Kuala Lumpur",
                "Penang",
                "Jakarta",
                "Surabaya",
                "Bandung",
                "Medan",
                "Manila",
                "Quezon City",
                "Cebu",
                "Davao",
                "Caloocan",
                "Ho Chi Minh City",
                "Hanoi",
                "Da Nang",
                "Hai Phong",
                "Dhaka",
                "Chittagong",
                "Karachi",
                "Lahore",
                "Islamabad",
                "Rawalpindi",
                "Faisalabad",
                # Middle Eastern cities
                "Dubai",
                "Abu Dhabi",
                "Doha",
                "Kuwait City",
                "Riyadh",
                "Jeddah",
                "Mecca",
                "Medina",
                "Tehran",
                "Isfahan",
                "Mashhad",
                "Shiraz",
                "Tabriz",
                "Istanbul",
                "Ankara",
                "Izmir",
                "Bursa",
                "Antalya",
                "Adana",
                "Gaziantep",
                "Beirut",
                "Damascus",
                "Baghdad",
                "Basra",
                "Amman",
                "Jerusalem",
                "Tel Aviv",
                "Haifa",
                "Cairo",
                "Alexandria",
                "Giza",
                "Luxor",
                # African cities
                "Lagos",
                "Kano",
                "Ibadan",
                "Abuja",
                "Cape Town",
                "Johannesburg",
                "Durban",
                "Pretoria",
                "Port Elizabeth",
                "Nairobi",
                "Mombasa",
                "Kisumu",
                "Addis Ababa",
                "Dar es Salaam",
                "Khartoum",
                "Casablanca",
                "Rabat",
                "Marrakech",
                "Fez",
                "Tunis",
                "Algiers",
                "Accra",
                "Kumasi",
                "Dakar",
                "Abidjan",
                "Kinshasa",
                "Lubumbashi",
                "Kampala",
                "Kigali",
                "Maputo",
                "Luanda",
                "Harare",
                "Lusaka",
                # South American cities
                "São Paulo",
                "Rio de Janeiro",
                "Brasília",
                "Salvador",
                "Fortaleza",
                "Belo Horizonte",
                "Manaus",
                "Curitiba",
                "Recife",
                "Porto Alegre",
                "Belém",
                "Goiânia",
                "Guarulhos",
                "Buenos Aires",
                "Córdoba",
                "Rosario",
                "Mendoza",
                "La Plata",
                "Santiago",
                "Valparaíso",
                "Concepción",
                "Lima",
                "Arequipa",
                "Trujillo",
                "Bogotá",
                "Medellín",
                "Cali",
                "Barranquilla",
                "Caracas",
                "Maracaibo",
                "Valencia",
                "Quito",
                "Guayaquil",
                "Montevideo",
                "Asunción",
                # Oceania cities
                "Sydney",
                "Melbourne",
                "Brisbane",
                "Perth",
                "Adelaide",
                "Gold Coast",
                "Newcastle",
                "Canberra",
                "Auckland",
                "Wellington",
                "Christchurch",
                "Hamilton",
                "Dunedin",
                # Canadian cities
                "Toronto",
                "Montreal",
                "Vancouver",
                "Calgary",
                "Edmonton",
                "Ottawa",
                "Winnipeg",
                "Quebec City",
                "Hamilton",
                "Kitchener",
                "London",
                "Halifax",
                "Victoria",
                "Saskatoon",
                "Regina",
                "St. John's",
                "Thunder Bay",
                "Windsor",
                "Sherbrooke",
                "Oshawa",
            ]
            state_names = [
                # US States
                "Alabama",
                "Alaska",
                "Arizona",
                "Arkansas",
                "California",
                "Colorado",
                "Connecticut",
                "Delaware",
                "Florida",
                "Georgia",
                "Hawaii",
                "Idaho",
                "Illinois",
                "Indiana",
                "Iowa",
                "Kansas",
                "Kentucky",
                "Louisiana",
                "Maine",
                "Maryland",
                "Massachusetts",
                "Michigan",
                "Minnesota",
                "Mississippi",
                "Missouri",
                "Montana",
                "Nebraska",
                "Nevada",
                "New Hampshire",
                "New Jersey",
                "New Mexico",
                "New York",
                "North Carolina",
                "North Dakota",
                "Ohio",
                "Oklahoma",
                "Oregon",
                "Pennsylvania",
                "Rhode Island",
                "South Carolina",
                "South Dakota",
                "Tennessee",
                "Texas",
                "Utah",
                "Vermont",
                "Virginia",
                "Washington",
                "West Virginia",
                "Wisconsin",
                "Wyoming",
                "District of Columbia",
                # Canadian Provinces
                "Ontario",
                "Quebec",
                "British Columbia",
                "Alberta",
                "Manitoba",
                "Saskatchewan",
                "Nova Scotia",
                "New Brunswick",
                "Newfoundland and Labrador",
                "Prince Edward Island",
                "Northwest Territories",
                "Yukon",
                "Nunavut",
                # Australian States
                "New South Wales",
                "Victoria",
                "Queensland",
                "Western Australia",
                "South Australia",
                "Tasmania",
                "Australian Capital Territory",
                "Northern Territory",
            ]
            country_names = [
                # Major countries
                "United States",
                "United Kingdom",
                "France",
                "Germany",
                "Italy",
                "Spain",
                "Canada",
                "Australia",
                "Japan",
                "China",
                "India",
                "Brazil",
                "Russia",
                "Mexico",
                "Netherlands",
                "Belgium",
                "Switzerland",
                "Austria",
                "Sweden",
                "Norway",
                "Denmark",
                "Finland",
                "Poland",
                "Greece",
                "Portugal",
                "Ireland",
                # Additional European countries
                "Czech Republic",
                "Hungary",
                "Romania",
                "Bulgaria",
                "Croatia",
                "Slovakia",
                "Slovenia",
                "Estonia",
                "Latvia",
                "Lithuania",
                "Luxembourg",
                "Malta",
                "Cyprus",
                "Iceland",
                "Liechtenstein",
                "Monaco",
                "San Marino",
                "Vatican City",
                "Andorra",
                # Asian countries
                "South Korea",
                "North Korea",
                "Thailand",
                "Vietnam",
                "Indonesia",
                "Malaysia",
                "Singapore",
                "Philippines",
                "Myanmar",
                "Cambodia",
                "Laos",
                "Bangladesh",
                "Pakistan",
                "Afghanistan",
                "Sri Lanka",
                "Nepal",
                "Bhutan",
                "Maldives",
                "Mongolia",
                "Kazakhstan",
                "Uzbekistan",
                "Kyrgyzstan",
                "Tajikistan",
                "Turkmenistan",
                "Azerbaijan",
                "Armenia",
                "Georgia",
                "Turkey",
                "Iran",
                "Iraq",
                "Saudi Arabia",
                "United Arab Emirates",
                "Kuwait",
                "Qatar",
                "Bahrain",
                "Oman",
                "Yemen",
                "Jordan",
                "Lebanon",
                "Syria",
                "Israel",
                "Palestine",
                # African countries
                "South Africa",
                "Egypt",
                "Nigeria",
                "Kenya",
                "Ethiopia",
                "Tanzania",
                "Ghana",
                "Morocco",
                "Algeria",
                "Tunisia",
                "Libya",
                "Sudan",
                "Uganda",
                "Angola",
                "Mozambique",
                "Madagascar",
                "Cameroon",
                "Ivory Coast",
                "Niger",
                "Burkina Faso",
                "Mali",
                "Malawi",
                "Zambia",
                "Zimbabwe",
                "Senegal",
                "Chad",
                "Somalia",
                "Guinea",
                "Rwanda",
                "Benin",
                "Burundi",
                "Tunisia",
                "Togo",
                "Sierra Leone",
                "Libya",
                "Liberia",
                "Central African Republic",
                "Mauritania",
                "Eritrea",
                "Gambia",
                "Botswana",
                "Namibia",
                "Gabon",
                "Lesotho",
                "Guinea-Bissau",
                "Equatorial Guinea",
                "Mauritius",
                "Eswatini",
                "Djibouti",
                "Comoros",
                # South American countries
                "Argentina",
                "Chile",
                "Colombia",
                "Peru",
                "Venezuela",
                "Ecuador",
                "Uruguay",
                "Paraguay",
                "Bolivia",
                "Guyana",
                "Suriname",
                "French Guiana",
                # Central American and Caribbean countries
                "Guatemala",
                "Honduras",
                "El Salvador",
                "Nicaragua",
                "Costa Rica",
                "Panama",
                "Belize",
                "Jamaica",
                "Haiti",
                "Dominican Republic",
                "Cuba",
                "Trinidad and Tobago",
                "Barbados",
                "Bahamas",
                "Puerto Rico",
                # Oceania countries
                "New Zealand",
                "Fiji",
                "Papua New Guinea",
                "Solomon Islands",
                "Vanuatu",
                "New Caledonia",
                "French Polynesia",
                "Samoa",
                "Tonga",
                "Micronesia",
                "Palau",
                "Marshall Islands",
                "Kiribati",
                "Tuvalu",
                "Nauru",
            ]

            # Helper function to generate unique place names with variations
            def _generate_place_variations(
                base_names, num_needed, place_type_prefix=""
            ):
                """Generate unique place names by combining base names with variations."""
                variations = []
                used_names = set()

                # First, use all base names
                for base_name in base_names:
                    if len(variations) >= num_needed:
                        break
                    if base_name not in used_names:
                        variations.append(base_name)
                        used_names.add(base_name)

                # Then create variations by combining base names with suffixes/prefixes
                suffixes = [
                    "",
                    " North",
                    " South",
                    " East",
                    " West",
                    " Central",
                    " Upper",
                    " Lower",
                    " New",
                    " Old",
                    " Port",
                    " Bay",
                    " Valley",
                    " Hills",
                    " Springs",
                    " Beach",
                    " Lake",
                    " River",
                    " Creek",
                    " Park",
                    " Grove",
                    " Heights",
                ]
                prefixes = [
                    "",
                    "New ",
                    "Old ",
                    "Upper ",
                    "Lower ",
                    "East ",
                    "West ",
                    "North ",
                    "South ",
                    "Port ",
                    "Fort ",
                    "Saint ",
                    "Mount ",
                    "Lake ",
                    "River ",
                ]

                # Generate combinations with a safety limit to prevent infinite loops
                max_attempts_without_new = 1000  # Exit if we can't find a new unique name after this many tries
                attempts_without_new = 0

                while (
                    len(variations) < num_needed
                    and attempts_without_new < max_attempts_without_new
                ):
                    found_new = False
                    base = random.choice(base_names)
                    if random.random() < 0.5:
                        # Use prefix
                        prefix = random.choice(prefixes)
                        if prefix:
                            variant = f"{prefix}{base}"
                        else:
                            variant = base
                    else:
                        # Use suffix
                        suffix = random.choice(suffixes)
                        variant = f"{base}{suffix}"

                    # Also try numbered variations
                    if random.random() < 0.3 and len(variations) < num_needed:
                        variant2 = f"{variant} {random.randint(1, 5)}"
                        if variant2 not in used_names:
                            variations.append(variant2)
                            used_names.add(variant2)
                            found_new = True

                    if variant not in used_names:
                        variations.append(variant)
                        used_names.add(variant)
                        found_new = True

                    if found_new:
                        attempts_without_new = 0
                    else:
                        attempts_without_new += 1

                return variations[:num_needed]

            # Create countries first (top level)
            country_places = []
            num_countries = max(
                len(country_names), int(num_people * 0.001)
            )  # 0.1% of people or all base countries
            country_variations = _generate_place_variations(
                country_names, num_countries
            )
            for country_name in country_variations:
                place = Place()
                pname = PlaceName()
                pname.set_value(country_name)
                place.set_name(pname)
                place.set_type(PlaceType.COUNTRY)
                if random.random() < 0.6:
                    place.set_title(country_name)
                if random.random() < 0.4:
                    place.set_code(
                        f"{country_name[:3].upper()}{random.randint(100, 999)}"
                    )
                # Add notes, citations, media to some countries (60% chance)
                if random.random() < 0.6:
                    note_text = f"Country note: {random.choice(['Major country', 'Historical significance', 'Research location'])}"
                    note_type = random.choice(
                        [NoteType.PLACE, NoteType.GENERAL, NoteType.RESEARCH]
                    )
                    note_handle = _create_note_with_tags_and_privacy(
                        db,
                        trans,
                        note_text,
                        note_type,
                        tags,
                        tag_chance=0.4,
                        privacy_chance=0.1,
                    )
                    place.add_note(note_handle)
                if tags and random.random() < 0.5:
                    tag_name = random.choice(list(tags.keys()))
                    tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
                    if tag_handle:
                        place.add_tag(tag_handle)
                if random.random() < 0.1:
                    place.set_privacy(True)
                place_handle = db.add_place(place, trans)
                places.append(place_handle)
                country_places.append(place_handle)

            # Create states/regions (enclosed by countries)
            state_places = []
            num_states = max(
                len(state_names), int(num_people * 0.002)
            )  # 0.2% of people or all base states
            state_variations = _generate_place_variations(state_names, num_states)
            for state_name in state_variations:
                place = Place()
                pname = PlaceName()
                pname.set_value(state_name)
                place.set_name(pname)
                place.set_type(PlaceType.STATE)
                if random.random() < 0.6:
                    place.set_title(state_name)
                if random.random() < 0.4:
                    place.set_code(
                        f"{state_name[:3].upper()}{random.randint(100, 999)}"
                    )
                # Add enclosed_by relationship (reference to a country)
                if country_places:
                    placeref = PlaceRef()
                    placeref.set_reference_handle(random.choice(country_places))
                    place.add_placeref(placeref)
                # Add notes, citations, media to some states (50% chance)
                if random.random() < 0.5:
                    note_text = f"State note: {random.choice(['Major state', 'Historical significance', 'Research location'])}"
                    note_type = random.choice(
                        [NoteType.PLACE, NoteType.GENERAL, NoteType.RESEARCH]
                    )
                    note_handle = _create_note_with_tags_and_privacy(
                        db,
                        trans,
                        note_text,
                        note_type,
                        tags,
                        tag_chance=0.4,
                        privacy_chance=0.1,
                    )
                    place.add_note(note_handle)
                if tags and random.random() < 0.4:
                    tag_name = random.choice(list(tags.keys()))
                    tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
                    if tag_handle:
                        place.add_tag(tag_handle)
                if random.random() < 0.1:
                    place.set_privacy(True)
                place_handle = db.add_place(place, trans)
                places.append(place_handle)
                state_places.append(place_handle)

            # Create cities (enclosed by states or countries)
            num_cities = max(
                len(city_names), int(num_people * 0.005)
            )  # 0.5% of people or all base cities
            city_variations = _generate_place_variations(city_names, num_cities)
            for city_name in city_variations:
                place = Place()
                pname = PlaceName()
                pname.set_value(city_name)
                place.set_name(pname)
                place.set_type(PlaceType.CITY)
                if random.random() < 0.6:
                    place.set_title(city_name)
                if random.random() < 0.4:
                    place.set_code(f"{city_name[:3].upper()}{random.randint(100, 999)}")
                # Add enclosed_by relationship (reference to a state or country)
                if state_places and random.random() < 0.7:
                    # 70% chance to be enclosed by a state
                    placeref = PlaceRef()
                    placeref.set_reference_handle(random.choice(state_places))
                    place.add_placeref(placeref)
                elif country_places:
                    # Otherwise enclosed by a country
                    placeref = PlaceRef()
                    placeref.set_reference_handle(random.choice(country_places))
                    place.add_placeref(placeref)
                # Add notes, citations, media to some cities (50% chance)
                if random.random() < 0.5:
                    note_text = f"City note: {random.choice(['Major city', 'Historical significance', 'Research location'])}"
                    note_type = random.choice(
                        [NoteType.PLACE, NoteType.GENERAL, NoteType.RESEARCH]
                    )
                    note_handle = _create_note_with_tags_and_privacy(
                        db,
                        trans,
                        note_text,
                        note_type,
                        tags,
                        tag_chance=0.4,
                        privacy_chance=0.1,
                    )
                    place.add_note(note_handle)
                if tags and random.random() < 0.4:
                    tag_name = random.choice(list(tags.keys()))
                    tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
                    if tag_handle:
                        place.add_tag(tag_handle)
                if random.random() < 0.1:
                    place.set_privacy(True)
                place_handle = db.add_place(place, trans)
                places.append(place_handle)

            # Generate additional smaller places (towns, villages, neighborhoods) for more variety
            # Use city names as base but create smaller place variations
            num_towns = int(num_people * 0.003)  # 0.3% additional towns/villages
            town_prefixes = [
                "",
                "New ",
                "Old ",
                "Little ",
                "Great ",
                "Upper ",
                "Lower ",
                "East ",
                "West ",
            ]
            town_suffixes = [
                "",
                " Town",
                " Village",
                " Township",
                " Borough",
                " Hamlet",
                " Settlement",
            ]
            for _ in range(num_towns):
                base_city = random.choice(city_names)
                prefix = random.choice(town_prefixes)
                suffix = random.choice(town_suffixes)
                town_name = f"{prefix}{base_city}{suffix}"

                place = Place()
                pname = PlaceName()
                pname.set_value(town_name)
                place.set_name(pname)
                place.set_type(PlaceType.CITY)  # Use CITY type for towns too
                if random.random() < 0.5:
                    place.set_title(town_name)
                if random.random() < 0.3:
                    place.set_code(f"{town_name[:3].upper()}{random.randint(100, 999)}")
                # Add enclosed_by relationship
                if state_places and random.random() < 0.6:
                    placeref = PlaceRef()
                    placeref.set_reference_handle(random.choice(state_places))
                    place.add_placeref(placeref)
                elif country_places:
                    placeref = PlaceRef()
                    placeref.set_reference_handle(random.choice(country_places))
                    place.add_placeref(placeref)
                if random.random() < 0.3:
                    note_text = f"Town note: {random.choice(['Small town', 'Rural area', 'Historical location'])}"
                    note_type = random.choice(
                        [NoteType.PLACE, NoteType.GENERAL, NoteType.RESEARCH]
                    )
                    note_handle = _create_note_with_tags_and_privacy(
                        db,
                        trans,
                        note_text,
                        note_type,
                        tags,
                        tag_chance=0.3,
                        privacy_chance=0.05,
                    )
                    place.add_note(note_handle)
                if tags and random.random() < 0.3:
                    tag_name = random.choice(list(tags.keys()))
                    tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
                    if tag_handle:
                        place.add_tag(tag_handle)
                place_handle = db.add_place(place, trans)
                places.append(place_handle)

            # Create repositories FIRST (they're independent)
            print("Generating repositories...")
            repositories = []
            num_repos = int(num_people * 0.04)  # 4% of people
            for _ in range(num_repos):
                repo_handle = _create_repository(db, trans, tags)
                repositories.append(repo_handle)

            # Create sources (they reference repositories)
            print("Generating sources...")
            sources = []
            num_sources = int(num_people * 0.10)  # 10% of people
            for _ in range(num_sources):
                source_handle = _create_source(db, trans, repositories, tags)
                sources.append(source_handle)

            # Create media objects first (they can be referenced by citations)
            print("Generating media objects...")
            media_objects = []
            num_media = int(num_people * 0.20)  # 20% of people
            for _ in range(num_media):
                media_handle = _create_media(
                    db, trans, [], sources, tags
                )  # Empty citations list for now
                media_objects.append(media_handle)

            # Add citations and sources to media objects will be done after citations are created

            # Create citations (they reference sources and can reference media)
            print("Generating citations...")
            citations = []
            num_citations = int(num_people * 0.30)  # 30% of people
            for _ in range(num_citations):
                citation_handle = _create_citation(
                    db, trans, sources, tags, media_objects
                )
                citations.append(citation_handle)

            # Attach media to some sources and citations
            print("Linking media to sources and citations...")
            for source_handle in random.sample(
                sources, min(len(sources), len(sources) // 3)
            ):
                if media_objects and random.random() < 0.3:
                    source = db.get_source_from_handle(source_handle)
                    media_ref = MediaRef()
                    media_ref.set_reference_handle(random.choice(media_objects))
                    source.add_media_reference(media_ref)
                    db.commit_source(source, trans)

            # Ensure more citations have media for HasGallery rule
            for citation_handle in random.sample(
                citations, min(len(citations), len(citations) // 2)
            ):
                citation = db.get_citation_from_handle(citation_handle)
                # Only add if it doesn't already have media
                if not citation.get_media_list() and media_objects:
                    media_ref = MediaRef()
                    media_ref.set_reference_handle(random.choice(media_objects))
                    citation.add_media_reference(media_ref)
                    db.commit_citation(citation, trans)

            # Add citations to media objects (for HasCitation and HasSourceOf rules)
            print("Linking citations to media...")
            # Ensure at least 50% of media have citations
            # For HasSourceOf rule, we need citations that have sources attached
            # Since all citations now have sources (required in _create_citation), we can use all citations
            # But let's verify and filter to be safe
            citations_with_sources = []
            for citation_handle in citations:
                try:
                    citation = db.get_citation_from_handle(citation_handle)
                    if citation and citation.get_reference_handle():
                        citations_with_sources.append(citation_handle)
                except:
                    continue

            # Ensure we have citations with sources (should be all of them now)
            if not citations_with_sources:
                # Fallback: if somehow no citations have sources, create one that does
                if sources:
                    citation = Citation()
                    citation.set_reference_handle(sources[0])
                    citation.set_page("Page 1")
                    citation_handle = db.add_citation(citation, trans)
                    citations_with_sources.append(citation_handle)

            num_media_to_link = max(1, len(media_objects) // 2)
            # Use citations with sources (should be all citations now)
            citations_to_use = (
                citations_with_sources if citations_with_sources else citations
            )

            # For media.HasSourceOf rule: ensure at least one media has a citation with the first source
            # Find or create a citation with the first source
            first_source_citation = None
            if sources and citations_to_use:
                first_source_handle = sources[0]
                for citation_handle in citations_to_use:
                    try:
                        citation = db.get_citation_from_handle(citation_handle)
                        if (
                            citation
                            and citation.get_reference_handle() == first_source_handle
                        ):
                            first_source_citation = citation_handle
                            break
                    except:
                        continue
                # If no citation found with first source, create one
                if not first_source_citation:
                    from gramps.gen.lib import Citation

                    citation = Citation()
                    citation.set_reference_handle(first_source_handle)
                    citation.set_page("TestPage")
                    citation_handle = db.add_citation(citation, trans)
                    first_source_citation = citation_handle
                    citations_to_use.append(citation_handle)

            # First, ensure at least one media has citation with first source (for HasSourceOf rule)
            if first_source_citation and media_objects:
                # Always add to the first media object to ensure it exists
                target_media_handle = media_objects[0]
                try:
                    target_media = db.get_media_from_handle(target_media_handle)
                    # Only add if not already present
                    if first_source_citation not in target_media.get_citation_list():
                        target_media.add_citation(first_source_citation)
                        db.commit_media(target_media, trans)
                except Exception as e:
                    # If this fails, try another media object
                    if len(media_objects) > 1:
                        try:
                            target_media = db.get_media_from_handle(media_objects[1])
                            if (
                                first_source_citation
                                not in target_media.get_citation_list()
                            ):
                                target_media.add_citation(first_source_citation)
                                db.commit_media(target_media, trans)
                        except:
                            pass

            # Then add citations to other media
            media_samples = random.sample(
                media_objects, min(num_media_to_link, len(media_objects))
            )
            for media_handle in media_samples:
                media = db.get_media_from_handle(media_handle)
                # Add citations to media - for HasCitation rule
                if citations_to_use:
                    # Add 1-3 citations to this media
                    num_citations_to_add = random.randint(
                        1, min(3, len(citations_to_use))
                    )
                    citations_to_add = random.sample(
                        citations_to_use, num_citations_to_add
                    )
                    for citation_handle in citations_to_add:
                        current_citations = media.get_citation_list()
                        if citation_handle not in current_citations:
                            media.add_citation(citation_handle)
                db.commit_media(media, trans)

            # Add citations and media to places (now that citations exist)
            print("Enhancing places with citations and media...")
            # Ensure at least 40% of places have citations and 30% have media
            places_to_enhance = random.sample(
                places, min(len(places), int(len(places) * 0.6))
            )
            for place_handle in places_to_enhance:
                place = db.get_place_from_handle(place_handle)
                # Add citations to places (40% chance)
                if citations and random.random() < 0.4:
                    # Add 1-2 citations
                    num_cits = random.randint(1, 2)
                    for _ in range(num_cits):
                        place.add_citation(random.choice(citations))
                # Add media to places (30% chance)
                if media_objects and random.random() < 0.3:
                    # Add 1-2 media references
                    num_media = random.randint(1, 2)
                    for _ in range(num_media):
                        media_ref = MediaRef()
                        media_ref.set_reference_handle(random.choice(media_objects))
                        place.add_media_reference(media_ref)
                db.commit_place(place, trans)

            # Generate main connected family tree (with citations and media)
            print(f"Generating {num_connected} connected people...")
            _generate_connected_tree(
                db,
                trans,
                num_connected,
                people_handles,
                families_handles,
                tags,
                places,
                sources,
                citations,
                media_objects,
            )

            # Generate disconnected people (~1%)
            print(f"Generating {num_disconnected} disconnected people...")
            _generate_disconnected_people(
                db,
                trans,
                num_disconnected,
                people_handles,
                tags,
                places,
                sources,
                citations,
                media_objects,
            )

            # Generate two unconnected families
            print("Generating 2 unconnected families...")
            _generate_unconnected_families(
                db,
                trans,
                num_unconnected_family,
                people_handles,
                families_handles,
                tags,
                places,
                sources,
                citations,
                media_objects,
            )

            # Add special cases for filter rules that need specific arguments
            print("Adding special cases for filter rules...")
            _add_special_filter_cases(
                db,
                trans,
                people_handles,
                families_handles,
                citations,
                sources,
                media_objects,
                tags,
            )

            # Set default person to I0000 (first person)
            print("Setting default person to I0000...")
            default_person_handle = None
            person_handles = db.get_person_handles()
            for person_handle in person_handles:
                try:
                    person = db.get_person_from_handle(person_handle)
                    if person and person.gramps_id == "I0000":
                        default_person_handle = person_handle
                        break
                except:
                    continue
            if default_person_handle:
                db.set_default_person_handle(default_person_handle)
                print(f"Default person set to I0000")
            else:
                print(f"Warning: Could not find person with gramps_id I0000")

        # Read database name
        db_name = "Unknown"
        name_file_path = os.path.join(dirpath, NAME_FILE)
        if os.path.exists(name_file_path):
            with open(name_file_path, "r", encoding="utf8") as name_file:
                db_name = name_file.read().strip()

        print(f"Database: {db_name}")
        print(f"Total people: {len(people_handles)}")
        print(f"Total families: {len(families_handles)}")
        print(f"Total places: {len(places) if 'places' in locals() else 0}")
        print(
            f"Total repositories: {len(repositories) if 'repositories' in locals() else 0}"
        )
        print(f"Total sources: {len(sources) if 'sources' in locals() else 0}")
        print(f"Total citations: {len(citations) if 'citations' in locals() else 0}")
        print(
            f"Total media objects: {len(media_objects) if 'media_objects' in locals() else 0}"
        )

        db.close()
        return dirpath

    except Exception as e:
        db.close()
        raise e


def _generate_connected_tree(
    db,
    trans,
    num_people,
    people_handles,
    families_handles,
    tags,
    places,
    sources=None,
    citations=None,
    media_objects=None,
):
    """Generate a connected family tree."""
    # Start with a root couple
    root_father = _create_person_with_variety(
        db,
        trans,
        Person.MALE,
        "Root",
        "Ancestor",
        tags,
        places,
        sources,
        citations,
        media_objects,
    )
    root_mother = _create_person_with_variety(
        db,
        trans,
        Person.FEMALE,
        "Root",
        "Ancestor",
        tags,
        places,
        sources,
        citations,
        media_objects,
    )
    people_handles.append(root_father.handle)
    people_handles.append(root_mother.handle)

    # Create root family
    root_family = Family()
    root_family.set_father_handle(root_father.handle)
    root_family.set_mother_handle(root_mother.handle)
    # Add citations to family (30% chance)
    if citations and random.random() < 0.3:
        root_family.add_citation(random.choice(citations))
    # Add media to family (20% chance)
    if media_objects and random.random() < 0.2:
        media_ref = MediaRef()
        media_ref.set_reference_handle(random.choice(media_objects))
        root_family.add_media_reference(media_ref)
    # Private flag (10% chance)
    if random.random() < 0.1:
        root_family.set_privacy(True)
    root_fam_handle = db.add_family(root_family, trans)
    # Reload family from database and add attributes/tags/notes
    root_family = db.get_family_from_handle(root_fam_handle)
    # Add tags to family (60% chance) - use canonical tag handle
    if tags and random.random() < 0.6:
        tag_name = random.choice(list(tags.keys()))
        tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
        if tag_handle:
            root_family.add_tag(tag_handle)
    # Add notes to family (60% chance)
    if random.random() < 0.6:
        note = Note()
        note.set_type(
            random.choice([NoteType.FAMILY, NoteType.GENERAL, NoteType.RESEARCH])
        )
        note.set(
            f"Family note: {random.choice(['Important', 'Verified', 'Needs verification', 'Research'])}"
        )
        note_handle = db.add_note(note, trans)
        root_family.add_note(note_handle)
    # Add attributes to family (50% chance)
    if random.random() < 0.5:
        attr = Attribute()
        attr_type = random.choice(ATTRIBUTE_TYPES)
        if attr_type == AttributeType.CUSTOM:
            attr.set_type((AttributeType.CUSTOM, "FamilyAttr"))
            attr.set_value("FamilyValue_42")
        else:
            attr.set_type(attr_type)
            attr.set_value(f"FamilyValue_{random.randint(1, 100)}")
        root_family.add_attribute(attr)
    # Add relationship type (80% chance) - increase for HasRelType rule
    if random.random() < 0.8:
        rel_types = [
            FamilyRelType.MARRIED,
            FamilyRelType.UNMARRIED,
            FamilyRelType.UNKNOWN,
            FamilyRelType.CIVIL_UNION,
        ]
        root_family.set_relationship(random.choice(rel_types))

    # Add marriage event to root family (70% chance)
    marriage_date = None
    if random.random() < 0.7:
        marriage_event = Event()
        marriage_event.set_type(EventType.MARRIAGE)
        marriage_date = Date()
        marriage_date.set_yr_mon_day(
            random.randint(1800, 2000), random.randint(1, 12), random.randint(1, 28)
        )
        marriage_event.set_date_object(marriage_date)
        if (
            places and random.random() < 0.95
        ):  # 95% chance - almost every marriage has a place
            marriage_event.set_place_handle(random.choice(places))
        if random.random() < 0.5:
            marriage_event.set_description(
                f"Marriage of {root_father.get_primary_name().get_first_name()} and {root_mother.get_primary_name().get_first_name()}"
            )
        marriage_handle = db.add_event(marriage_event, trans)
        event_ref = EventRef()
        event_ref.set_reference_handle(marriage_handle)
        root_family.add_event_ref(event_ref)

    # Add divorce event - 15% chance (only if there was a marriage)
    if marriage_date and random.random() < 0.15:
        divorce_event = Event()
        divorce_event.set_type(EventType.DIVORCE)
        # Divorce date should be after marriage date (1-30 years later)
        marriage_year = marriage_date.get_year()
        if marriage_year:
            years_married = random.randint(1, 30)
            divorce_year = min(marriage_year + years_married, 2020)
            divorce_date = Date()
            divorce_date.set_yr_mon_day(
                divorce_year, random.randint(1, 12), random.randint(1, 28)
            )
            divorce_event.set_date_object(divorce_date)
            if (
                places and random.random() < 0.95
            ):  # 95% chance - almost every divorce has a place
                divorce_event.set_place_handle(random.choice(places))
            if random.random() < 0.5:
                divorce_event.set_description(
                    f"Divorce of {root_father.get_primary_name().get_first_name()} and {root_mother.get_primary_name().get_first_name()}"
                )
            divorce_handle = db.add_event(divorce_event, trans)
            event_ref = EventRef()
            event_ref.set_reference_handle(divorce_handle)
            root_family.add_event_ref(event_ref)

    # Commit family after adding all attributes/tags/notes
    db.commit_family(root_family, trans)
    root_father.add_family_handle(root_fam_handle)
    root_mother.add_family_handle(root_fam_handle)
    db.commit_person(root_father, trans)
    db.commit_person(root_mother, trans)
    families_handles.append(root_fam_handle)

    # Generate descendants
    # Store people who can have children (both couples and single parents)
    # Format: (person1, person2 or None, family_handle or None)
    current_parents = [(root_father, root_mother, root_fam_handle)]
    people_created = 2

    while people_created < num_people and current_parents:
        next_parents = []
        for parent1, parent2, parent_fam_handle in current_parents:
            if people_created >= num_people:
                break

            # Get the family object if it exists
            if parent_fam_handle:
                parent_family = db.get_family_from_handle(parent_fam_handle)
            else:
                # Create a new family for single parent
                parent_family = Family()
                if parent1.gender == Person.MALE:
                    parent_family.set_father_handle(parent1.handle)
                else:
                    parent_family.set_mother_handle(parent1.handle)
                parent_fam_handle = db.add_family(parent_family, trans)
                parent1.add_family_handle(parent_fam_handle)
                db.commit_person(parent1, trans)
                families_handles.append(parent_fam_handle)

            # Create more children per couple to reach target faster
            # Calculate how many children we need to create
            remaining = num_people - people_created
            # Create 2-8 children per couple, but don't exceed remaining
            max_children = min(8, remaining)
            if max_children >= 2:
                num_children = random.randint(2, max_children)
            elif max_children == 1:
                num_children = 1
            else:
                num_children = 0

            children = []
            # Create twins for some families (5% chance) - for HasTwins rule
            create_twins = random.random() < 0.05 and num_children >= 2

            for i in range(num_children):
                if people_created >= num_people:
                    break

                # Random gender
                gender = random.choice(
                    [Person.MALE, Person.FEMALE, Person.UNKNOWN, Person.OTHER]
                )
                first_name = generate_random_first_name(gender)
                surname = generate_random_surname()

                # If creating twins and this is the second child, use same birth date as first
                if create_twins and i == 1 and children:
                    # Get birth date from first twin
                    first_twin = children[0]
                    birth_ref = first_twin.get_birth_ref()
                    if birth_ref:
                        birth_event = db.get_event_from_handle(birth_ref.ref)
                        birth_date = birth_event.get_date_object()
                        # Create child with same birth date
                        child = _create_person_with_variety(
                            db,
                            trans,
                            gender,
                            first_name,
                            surname,
                            tags,
                            places,
                            sources,
                            citations,
                            media_objects,
                            birth_date=birth_date,  # Pass the birth date
                        )
                    else:
                        child = _create_person_with_variety(
                            db,
                            trans,
                            gender,
                            first_name,
                            surname,
                            tags,
                            places,
                            sources,
                            citations,
                            media_objects,
                        )
                else:
                    child = _create_person_with_variety(
                        db,
                        trans,
                        gender,
                        first_name,
                        surname,
                        tags,
                        places,
                        sources,
                        citations,
                        media_objects,
                    )
                people_handles.append(child.handle)
                # Add child with relationship type (BIRTH for most, ADOPTED for some)
                childref = ChildRef()
                childref.set_reference_handle(child.handle)
                # 10% chance of adoption, otherwise birth
                if random.random() < 0.1:
                    childref.set_mother_relation(ChildRefType.ADOPTED)
                    childref.set_father_relation(ChildRefType.ADOPTED)
                else:
                    childref.set_mother_relation(ChildRefType.BIRTH)
                    childref.set_father_relation(ChildRefType.BIRTH)
                parent_family.add_child_ref(childref)
                # IMPORTANT: Set parent family handle on child for HaveAltFamilies rule
                child.add_parent_family_handle(parent_fam_handle)
                db.commit_person(child, trans)
                children.append(child)
                people_created += 1

            # Commit family after adding all children (needed for HasTwins rule)
            if children:
                db.commit_family(parent_family, trans)

            # Create families for next generation - pair up children and also allow singles
            if children:
                random.shuffle(children)
                paired = set()

                # Pair up children
                for i in range(0, len(children) - 1, 2):
                    if people_created >= num_people:
                        break
                    child1 = children[i]
                    child2 = children[i + 1]
                    paired.add(i)
                    paired.add(i + 1)

                    # Ensure opposite genders for pairing (mostly)
                    if child1.gender == Person.MALE and child2.gender == Person.FEMALE:
                        new_father, new_mother = child1, child2
                    elif (
                        child1.gender == Person.FEMALE and child2.gender == Person.MALE
                    ):
                        new_father, new_mother = child2, child1
                    else:
                        # Random assignment if genders don't match
                        new_father, new_mother = child1, child2
                        new_father.gender = Person.MALE
                        new_mother.gender = Person.FEMALE
                        db.commit_person(new_father, trans)
                        db.commit_person(new_mother, trans)

                    # Create family for this couple
                    new_family = Family()
                    new_family.set_father_handle(new_father.handle)
                    new_family.set_mother_handle(new_mother.handle)
                    # Add citations to family (30% chance)
                    if citations and random.random() < 0.3:
                        new_family.add_citation(random.choice(citations))
                    # Add media to family (20% chance)
                    if media_objects and random.random() < 0.2:
                        media_ref = MediaRef()
                        media_ref.set_reference_handle(random.choice(media_objects))
                        new_family.add_media_reference(media_ref)
                    # Private flag (10% chance)
                    if random.random() < 0.1:
                        new_family.set_privacy(True)
                    new_fam_handle = db.add_family(new_family, trans)
                    # Reload family from database and add attributes/tags/notes
                    new_family = db.get_family_from_handle(new_fam_handle)
                    # Add tags to family (60% chance) - use canonical tag handle
                    if tags and random.random() < 0.6:
                        tag_name = random.choice(list(tags.keys()))
                        tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
                        if tag_handle:
                            new_family.add_tag(tag_handle)
                    # Add notes to family (60% chance)
                    if random.random() < 0.6:
                        note = Note()
                        note.set_type(
                            random.choice(
                                [NoteType.FAMILY, NoteType.GENERAL, NoteType.RESEARCH]
                            )
                        )
                        note.set(
                            f"Family note: {random.choice(['Important', 'Verified', 'Needs verification', 'Research'])}"
                        )
                        note_handle = db.add_note(note, trans)
                        new_family.add_note(note_handle)
                    # Add attributes to family (50% chance)
                    if random.random() < 0.5:
                        attr = Attribute()
                        attr_type = random.choice(ATTRIBUTE_TYPES)
                        if attr_type == AttributeType.CUSTOM:
                            attr.set_type((AttributeType.CUSTOM, "FamilyAttr"))
                            attr.set_value("FamilyValue_42")
                        else:
                            attr.set_type(attr_type)
                            attr.set_value(f"FamilyValue_{random.randint(1, 100)}")
                        new_family.add_attribute(attr)
                    # Add relationship type (80% chance) - increase for HasRelType rule
                    if random.random() < 0.8:
                        rel_types = [
                            FamilyRelType.MARRIED,
                            FamilyRelType.UNMARRIED,
                            FamilyRelType.UNKNOWN,
                            FamilyRelType.CIVIL_UNION,
                        ]
                        new_family.set_relationship(random.choice(rel_types))
                    # Add family event (marriage) - 70% chance for HasEvent rule
                    marriage_date = None
                    if random.random() < 0.7:
                        marriage_event = Event()
                        marriage_event.set_type(EventType.MARRIAGE)
                        marriage_date = Date()
                        marriage_date.set_yr_mon_day(
                            random.randint(1850, 2000),
                            random.randint(1, 12),
                            random.randint(1, 28),
                        )
                        marriage_event.set_date_object(marriage_date)
                        if places and random.random() < 0.7:
                            marriage_event.set_place_handle(random.choice(places))
                        if random.random() < 0.5:
                            marriage_event.set_description(
                                f"Marriage of {new_father.get_primary_name().get_first_name()} and {new_mother.get_primary_name().get_first_name()}"
                            )
                        marriage_handle = db.add_event(marriage_event, trans)
                        event_ref = EventRef()
                        event_ref.set_reference_handle(marriage_handle)
                        new_family.add_event_ref(event_ref)

                    # Add divorce event - 15% chance (only if there was a marriage)
                    if marriage_date and random.random() < 0.15:
                        divorce_event = Event()
                        divorce_event.set_type(EventType.DIVORCE)
                        # Divorce date should be after marriage date (1-30 years later)
                        marriage_year = marriage_date.get_year()
                        marriage_month = marriage_date.get_month()
                        marriage_day = marriage_date.get_day()
                        if marriage_year:
                            years_married = random.randint(1, 30)
                            divorce_year = min(marriage_year + years_married, 2020)
                            divorce_date = Date()
                            divorce_date.set_yr_mon_day(
                                divorce_year,
                                random.randint(1, 12),
                                random.randint(1, 28),
                            )
                            divorce_event.set_date_object(divorce_date)
                            if places and random.random() < 0.7:
                                divorce_event.set_place_handle(random.choice(places))
                            if random.random() < 0.5:
                                divorce_event.set_description(
                                    f"Divorce of {new_father.get_primary_name().get_first_name()} and {new_mother.get_primary_name().get_first_name()}"
                                )
                            divorce_handle = db.add_event(divorce_event, trans)
                            event_ref = EventRef()
                            event_ref.set_reference_handle(divorce_handle)
                            new_family.add_event_ref(event_ref)

                    # Commit family after adding all attributes/tags/notes
                    db.commit_family(new_family, trans)
                    new_father.add_family_handle(new_fam_handle)
                    new_mother.add_family_handle(new_fam_handle)
                    db.commit_person(new_father, trans)
                    db.commit_person(new_mother, trans)
                    families_handles.append(new_fam_handle)
                    next_parents.append((new_father, new_mother, new_fam_handle))

                # Add unpaired children as single parents (30% chance each)
                for i, child in enumerate(children):
                    if i not in paired and random.random() < 0.3:
                        next_parents.append((child, None, None))

        current_parents = next_parents


def _generate_disconnected_people(
    db,
    trans,
    num_people,
    people_handles,
    tags,
    places,
    sources=None,
    citations=None,
    media_objects=None,
):
    """Generate people with no family connections."""
    for i in range(num_people):
        gender = random.choice(
            [Person.MALE, Person.FEMALE, Person.UNKNOWN, Person.OTHER]
        )
        first_name = generate_random_first_name(gender)
        surname = generate_random_surname()

        person = _create_person_with_variety(
            db,
            trans,
            gender,
            first_name,
            surname,
            tags,
            places,
            sources,
            citations,
            media_objects,
        )
        people_handles.append(person.handle)


def _generate_unconnected_families(
    db,
    trans,
    num_people,
    people_handles,
    families_handles,
    tags,
    places,
    sources=None,
    citations=None,
    media_objects=None,
):
    """Generate two families not connected to the main tree."""
    # First unconnected family
    father1 = _create_person_with_variety(
        db,
        trans,
        Person.MALE,
        "Isolated",
        "Family1",
        tags,
        places,
        sources,
        citations,
        media_objects,
    )
    mother1 = _create_person_with_variety(
        db,
        trans,
        Person.FEMALE,
        "Isolated",
        "Family1",
        tags,
        places,
        sources,
        citations,
        media_objects,
    )
    people_handles.append(father1.handle)
    people_handles.append(mother1.handle)

    family1 = Family()
    family1.set_father_handle(father1.handle)
    family1.set_mother_handle(mother1.handle)
    # Add citations to family (30% chance)
    if citations and random.random() < 0.3:
        family1.add_citation(random.choice(citations))
    # Add media to family (20% chance)
    if media_objects and random.random() < 0.2:
        media_ref = MediaRef()
        media_ref.set_reference_handle(random.choice(media_objects))
        family1.add_media_reference(media_ref)
    # Private flag (10% chance)
    if random.random() < 0.1:
        family1.set_privacy(True)
    fam_handle1 = db.add_family(family1, trans)
    # Reload family from database and add attributes/tags/notes
    family1 = db.get_family_from_handle(fam_handle1)
    # Add tags to family (60% chance) - use canonical tag handle
    if tags and random.random() < 0.6:
        tag_name = random.choice(list(tags.keys()))
        tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
        if tag_handle:
            family1.add_tag(tag_handle)
    # Add notes to family (60% chance)
    if random.random() < 0.6:
        note = Note()
        note.set_type(
            random.choice([NoteType.FAMILY, NoteType.GENERAL, NoteType.RESEARCH])
        )
        note.set(
            f"Family note: {random.choice(['Important', 'Verified', 'Needs verification', 'Research'])}"
        )
        note_handle = db.add_note(note, trans)
        family1.add_note(note_handle)
    # Add attributes to family (50% chance)
    if random.random() < 0.5:
        attr = Attribute()
        attr_type = random.choice(ATTRIBUTE_TYPES)
        if attr_type == AttributeType.CUSTOM:
            attr.set_type((AttributeType.CUSTOM, "FamilyAttr"))
            attr.set_value("FamilyValue_42")
        else:
            attr.set_type(attr_type)
            attr.set_value(f"FamilyValue_{random.randint(1, 100)}")
        family1.add_attribute(attr)
    # Add relationship type (80% chance) - increase for HasRelType rule
    if random.random() < 0.8:
        rel_types = [
            FamilyRelType.MARRIED,
            FamilyRelType.UNMARRIED,
            FamilyRelType.UNKNOWN,
            FamilyRelType.CIVIL_UNION,
        ]
        family1.set_relationship(random.choice(rel_types))

    # Add marriage event (70% chance)
    marriage_date = None
    if random.random() < 0.7:
        marriage_event = Event()
        marriage_event.set_type(EventType.MARRIAGE)
        marriage_date = Date()
        marriage_date.set_yr_mon_day(
            random.randint(1850, 2000), random.randint(1, 12), random.randint(1, 28)
        )
        marriage_event.set_date_object(marriage_date)
        if (
            places and random.random() < 0.95
        ):  # 95% chance - almost every marriage has a place
            marriage_event.set_place_handle(random.choice(places))
        if random.random() < 0.5:
            marriage_event.set_description(
                f"Marriage of {father1.get_primary_name().get_first_name()} and {mother1.get_primary_name().get_first_name()}"
            )
        marriage_handle = db.add_event(marriage_event, trans)
        event_ref = EventRef()
        event_ref.set_reference_handle(marriage_handle)
        family1.add_event_ref(event_ref)

    # Add divorce event - 15% chance (only if there was a marriage)
    if marriage_date and random.random() < 0.15:
        divorce_event = Event()
        divorce_event.set_type(EventType.DIVORCE)
        marriage_year = marriage_date.get_year()
        if marriage_year:
            years_married = random.randint(1, 30)
            divorce_year = min(marriage_year + years_married, 2020)
            divorce_date = Date()
            divorce_date.set_yr_mon_day(
                divorce_year, random.randint(1, 12), random.randint(1, 28)
            )
            divorce_event.set_date_object(divorce_date)
            if (
                places and random.random() < 0.95
            ):  # 95% chance - almost every divorce has a place
                divorce_event.set_place_handle(random.choice(places))
            if random.random() < 0.5:
                divorce_event.set_description(
                    f"Divorce of {father1.get_primary_name().get_first_name()} and {mother1.get_primary_name().get_first_name()}"
                )
            divorce_handle = db.add_event(divorce_event, trans)
            event_ref = EventRef()
            event_ref.set_reference_handle(divorce_handle)
            family1.add_event_ref(event_ref)

    # Commit family after adding all attributes/tags/notes
    db.commit_family(family1, trans)
    father1.add_family_handle(fam_handle1)
    mother1.add_family_handle(fam_handle1)
    db.commit_person(father1, trans)
    db.commit_person(mother1, trans)
    families_handles.append(fam_handle1)

    # Second unconnected family
    father2 = _create_person_with_variety(
        db,
        trans,
        Person.MALE,
        "Isolated",
        "Family2",
        tags,
        places,
        sources,
        citations,
        media_objects,
    )
    mother2 = _create_person_with_variety(
        db,
        trans,
        Person.FEMALE,
        "Isolated",
        "Family2",
        tags,
        places,
        sources,
        citations,
        media_objects,
    )
    people_handles.append(father2.handle)
    people_handles.append(mother2.handle)

    family2 = Family()
    family2.set_father_handle(father2.handle)
    family2.set_mother_handle(mother2.handle)
    # Add citations to family (30% chance)
    if citations and random.random() < 0.3:
        family2.add_citation(random.choice(citations))
    # Add media to family (20% chance)
    if media_objects and random.random() < 0.2:
        media_ref = MediaRef()
        media_ref.set_reference_handle(random.choice(media_objects))
        family2.add_media_reference(media_ref)
    # Private flag (10% chance)
    if random.random() < 0.1:
        family2.set_privacy(True)
    fam_handle2 = db.add_family(family2, trans)
    # Reload family from database and add attributes/tags/notes
    family2 = db.get_family_from_handle(fam_handle2)
    # Add tags to family (60% chance) - use canonical tag handle
    if tags and random.random() < 0.6:
        tag_name = random.choice(list(tags.keys()))
        tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
        if tag_handle:
            family2.add_tag(tag_handle)
    # Add notes to family (60% chance)
    if random.random() < 0.6:
        note = Note()
        note.set_type(
            random.choice([NoteType.FAMILY, NoteType.GENERAL, NoteType.RESEARCH])
        )
        note.set(
            f"Family note: {random.choice(['Important', 'Verified', 'Needs verification', 'Research'])}"
        )
        note_handle = db.add_note(note, trans)
        family2.add_note(note_handle)
    # Add attributes to family (50% chance)
    if random.random() < 0.5:
        attr = Attribute()
        attr_type = random.choice(ATTRIBUTE_TYPES)
        if attr_type == AttributeType.CUSTOM:
            attr.set_type((AttributeType.CUSTOM, "FamilyAttr"))
            attr.set_value("FamilyValue_42")
        else:
            attr.set_type(attr_type)
            attr.set_value(f"FamilyValue_{random.randint(1, 100)}")
        family2.add_attribute(attr)
    # Add relationship type (80% chance) - increase for HasRelType rule
    if random.random() < 0.8:
        rel_types = [
            FamilyRelType.MARRIED,
            FamilyRelType.UNMARRIED,
            FamilyRelType.UNKNOWN,
            FamilyRelType.CIVIL_UNION,
        ]
        family2.set_relationship(random.choice(rel_types))

    # Add marriage event (70% chance)
    marriage_date = None
    if random.random() < 0.7:
        marriage_event = Event()
        marriage_event.set_type(EventType.MARRIAGE)
        marriage_date = Date()
        marriage_date.set_yr_mon_day(
            random.randint(1850, 2000), random.randint(1, 12), random.randint(1, 28)
        )
        marriage_event.set_date_object(marriage_date)
        if (
            places and random.random() < 0.95
        ):  # 95% chance - almost every marriage has a place
            marriage_event.set_place_handle(random.choice(places))
        if random.random() < 0.5:
            marriage_event.set_description(
                f"Marriage of {father2.get_primary_name().get_first_name()} and {mother2.get_primary_name().get_first_name()}"
            )
        marriage_handle = db.add_event(marriage_event, trans)
        event_ref = EventRef()
        event_ref.set_reference_handle(marriage_handle)
        family2.add_event_ref(event_ref)

    # Add divorce event - 15% chance (only if there was a marriage)
    if marriage_date and random.random() < 0.15:
        divorce_event = Event()
        divorce_event.set_type(EventType.DIVORCE)
        marriage_year = marriage_date.get_year()
        if marriage_year:
            years_married = random.randint(1, 30)
            divorce_year = min(marriage_year + years_married, 2020)
            divorce_date = Date()
            divorce_date.set_yr_mon_day(
                divorce_year, random.randint(1, 12), random.randint(1, 28)
            )
            divorce_event.set_date_object(divorce_date)
            if (
                places and random.random() < 0.95
            ):  # 95% chance - almost every divorce has a place
                divorce_event.set_place_handle(random.choice(places))
            if random.random() < 0.5:
                divorce_event.set_description(
                    f"Divorce of {father2.get_primary_name().get_first_name()} and {mother2.get_primary_name().get_first_name()}"
                )
            divorce_handle = db.add_event(divorce_event, trans)
            event_ref = EventRef()
            event_ref.set_reference_handle(divorce_handle)
            family2.add_event_ref(event_ref)

    # Commit family after adding all attributes/tags/notes
    db.commit_family(family2, trans)
    father2.add_family_handle(fam_handle2)
    mother2.add_family_handle(fam_handle2)
    db.commit_person(father2, trans)
    db.commit_person(mother2, trans)
    families_handles.append(fam_handle2)


def _create_person_with_variety(
    db,
    trans,
    gender,
    first_name,
    surname,
    tags,
    places,
    sources=None,
    citations=None,
    media_objects=None,
    birth_date=None,
):
    """Create a person with various attributes for filter testing."""
    person = Person()
    person.set_gender(gender)

    # Primary name
    name = Name()
    # For IncompleteNames rule: 10% chance of missing first name or surname
    # But always ensure at least one component is present
    if random.random() < 0.1:
        # 5% chance missing first name (but keep surname), 5% chance missing surname (but keep first name)
        if random.random() < 0.5:
            # Missing first name, but keep surname
            name.set_first_name("")  # Missing first name
            surname_obj = Surname()
            surname_obj.set_surname(surname)
            # Add name origin type (30% chance) - for HasNameOriginType rule
            if random.random() < 0.3:
                origin_types = [
                    NameOriginType.PATRILINEAL,
                    NameOriginType.MATRILINEAL,
                    NameOriginType.INHERITED,
                    NameOriginType.GIVEN,
                ]
                surname_obj.set_origintype(random.choice(origin_types))
            name.set_surname_list([surname_obj])
        else:
            # Missing surname, but keep first name
            name.set_first_name(first_name)
            # Don't add surname list - this creates an incomplete name for testing
    else:
        # Complete name with both first name and surname
        name.set_first_name(first_name)
        surname_obj = Surname()
        surname_obj.set_surname(surname)
        # Add name origin type (30% chance) - for HasNameOriginType rule
        if random.random() < 0.3:
            origin_types = [
                NameOriginType.PATRILINEAL,
                NameOriginType.MATRILINEAL,
                NameOriginType.INHERITED,
                NameOriginType.GIVEN,
            ]
            surname_obj.set_origintype(random.choice(origin_types))
        name.set_surname_list([surname_obj])
    # Add name type (40% chance) - for HasNameType rule
    if random.random() < 0.4:
        name_types = [NameType.BIRTH, NameType.MARRIED, NameType.AKA]
        name.set_type(random.choice(name_types))
    person.set_primary_name(name)

    # Alternate names (30% chance)
    if random.random() < 0.3:
        alt_name = Name()
        alt_name.set_first_name(first_name)
        alt_surname = Surname()
        alt_surname.set_surname(generate_random_surname())
        # Add name origin type to alternate name (30% chance)
        if random.random() < 0.3:
            origin_types = [
                NameOriginType.PATRILINEAL,
                NameOriginType.MATRILINEAL,
                NameOriginType.INHERITED,
                NameOriginType.GIVEN,
            ]
            alt_surname.set_origintype(random.choice(origin_types))
        alt_name.set_surname_list([alt_surname])
        # Add name type to alternate name (40% chance) - often MARRIED for alternate names
        if random.random() < 0.4:
            name_types = [NameType.MARRIED, NameType.AKA, NameType.BIRTH]
            alt_name.set_type(random.choice(name_types))
        person.add_alternate_name(alt_name)

    # Nickname (20% chance)
    if random.random() < 0.2:
        name.set_call_name(f"{first_name[:3]}")

    # Birth event (80% chance)
    birth_year = None
    birth_month = None
    birth_day = None
    if (
        random.random() < 0.8 or birth_date is not None
    ):  # Always create if birth_date provided (for twins)
        birth_event = Event()
        birth_event.set_type(EventType.BIRTH)
        if birth_date is None:
            birth_year = random.randint(1800, 2000)
            birth_month = random.randint(1, 12)
            birth_day = random.randint(1, 28)
            birth_date = Date()
            birth_date.set_yr_mon_day(birth_year, birth_month, birth_day)
        else:
            # Use provided birth_date (for twins)
            birth_year = birth_date.get_year() if birth_date else None
            birth_month = birth_date.get_month() if birth_date else None
            birth_day = birth_date.get_day() if birth_date else None
        birth_event.set_date_object(birth_date)
        if (
            places and random.random() < 0.95
        ):  # 95% chance - almost every birth has a place
            birth_event.set_place_handle(random.choice(places))
        # Description (70% chance) - needed for HasData rule - increase to ensure variety
        if random.random() < 0.7:
            birth_event.set_description(f"Birth of {first_name} {surname}")
        # Add citations to event (40% chance)
        if citations and random.random() < 0.4:
            birth_event.add_citation(random.choice(citations))
        # Add media to event (50% chance) - increase for HasGallery rule
        if media_objects and random.random() < 0.5:
            media_ref = MediaRef()
            media_ref.set_reference_handle(random.choice(media_objects))
            birth_event.add_media_reference(media_ref)
        # Private flag (15% chance)
        if random.random() < 0.15:
            birth_event.set_privacy(True)
        birth_handle = db.add_event(birth_event, trans)
        # Reload event from database and add attributes/tags/notes
        birth_event = db.get_event_from_handle(birth_handle)
        # Add attributes to event (30% chance) - use specific values for filter testing
        if random.random() < 0.3:
            attr = Attribute()
            # Use specific attribute types for better filter coverage
            attr_type = random.choice(ATTRIBUTE_TYPES)
            if attr_type == AttributeType.CUSTOM:
                attr.set_type((AttributeType.CUSTOM, "EventAttr"))
                attr.set_value("EventValue_42")  # Specific value for testing
            else:
                attr.set_type(attr_type)
                attr.set_value(f"EventValue_{random.randint(1, 100)}")
            birth_event.add_attribute(attr)
        # Add notes to event (60% chance) - increase for HasNote rule - use specific note types
        if random.random() < 0.6:
            note = Note()
            note_type = random.choice(
                [NoteType.EVENT, NoteType.GENERAL, NoteType.RESEARCH, NoteType.ANALYSIS]
            )
            note.set_type(note_type)
            note.set(
                f"Birth event note: {random.choice(['Hospital birth', 'Home birth', 'Verified', 'Needs verification'])}"
            )
            note_handle = db.add_note(note, trans)
            birth_event.add_note(note_handle)
        # Add tags to event (40% chance) - use canonical tag handle
        if tags and random.random() < 0.4:
            tag_name = random.choice(list(tags.keys()))
            tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
            if tag_handle:
                birth_event.add_tag(tag_handle)
        # Commit event after adding attributes/tags to ensure they're saved
        db.commit_event(birth_event, trans)
        birth_ref = EventRef()
        birth_ref.set_reference_handle(birth_handle)
        person.set_birth_ref(birth_ref)

    # Death event (65% chance) - increased to ensure dead people
    # If we have a birth date, ensure death is after birth with reasonable age (20-100 years)
    if random.random() < 0.65:
        death_event = Event()
        death_event.set_type(EventType.DEATH)
        death_date = Date()
        if birth_year:
            # Death should be 20-100 years after birth
            age_at_death = random.randint(20, 100)
            death_year = min(birth_year + age_at_death, 2020)
            death_month = random.randint(1, 12)
            death_day = random.randint(1, 28)
            # Ensure death date is after birth date
            if death_year == birth_year:
                if death_month < birth_month or (
                    death_month == birth_month and death_day < birth_day
                ):
                    death_month = min(12, birth_month + 1)
                    death_day = random.randint(1, 28)
            death_date.set_yr_mon_day(death_year, death_month, death_day)
        else:
            # No birth date, use random date
            death_date.set_yr_mon_day(
                random.randint(1850, 2020), random.randint(1, 12), random.randint(1, 28)
            )
        death_event.set_date_object(death_date)
        if (
            places and random.random() < 0.95
        ):  # 95% chance - almost every death has a place
            death_event.set_place_handle(random.choice(places))
        # Description (70% chance) - needed for HasData rule - increase to ensure variety
        if random.random() < 0.7:
            death_event.set_description(f"Death of {first_name} {surname}")
        # Add citations to event (40% chance)
        if citations and random.random() < 0.4:
            death_event.add_citation(random.choice(citations))
        # Add media to event (50% chance) - increase for HasGallery rule
        if media_objects and random.random() < 0.5:
            media_ref = MediaRef()
            media_ref.set_reference_handle(random.choice(media_objects))
            death_event.add_media_reference(media_ref)
        # Private flag (15% chance)
        if random.random() < 0.15:
            death_event.set_privacy(True)
        death_handle = db.add_event(death_event, trans)
        # Reload event from database and add attributes/tags/notes
        death_event = db.get_event_from_handle(death_handle)
        # Add attributes to event (30% chance) - use specific values for filter testing
        if random.random() < 0.3:
            attr = Attribute()
            attr_type = random.choice(ATTRIBUTE_TYPES)
            if attr_type == AttributeType.CUSTOM:
                attr.set_type((AttributeType.CUSTOM, "EventAttr"))
                attr.set_value("EventValue_42")  # Specific value for testing
            else:
                attr.set_type(attr_type)
                attr.set_value(f"EventValue_{random.randint(1, 100)}")
            death_event.add_attribute(attr)
        # Add notes to event (60% chance) - increase for HasNote rule - use specific note types
        if random.random() < 0.6:
            note = Note()
            note_type = random.choice(
                [NoteType.EVENT, NoteType.GENERAL, NoteType.RESEARCH, NoteType.ANALYSIS]
            )
            note.set_type(note_type)
            note.set(
                f"Death event note: {random.choice(['Natural causes', 'Accident', 'Illness', 'Verified'])}"
            )
            note_handle = db.add_note(note, trans)
            death_event.add_note(note_handle)
        # Add tags to event (40% chance) - use canonical tag handle
        if tags and random.random() < 0.4:
            tag_name = random.choice(list(tags.keys()))
            tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
            if tag_handle:
                death_event.add_tag(tag_handle)
        # Commit event after adding attributes/tags to ensure they're saved
        db.commit_event(death_event, trans)
        death_ref = EventRef()
        death_ref.set_reference_handle(death_handle)
        person.set_death_ref(death_ref)

    # Other events - use more event types for variety
    other_event_types = [
        EventType.MARRIAGE,
        EventType.OCCUPATION,
        EventType.RESIDENCE,
        EventType.EDUCATION,
        EventType.MILITARY_SERV,
        EventType.BAPTISM,
        EventType.CENSUS,
        EventType.EMIGRATION,
        EventType.IMMIGRATION,
    ]
    # Add 1-3 random events per person
    num_other_events = random.randint(0, 3)
    for _ in range(num_other_events):
        event_type = random.choice(other_event_types)
        event = Event()
        event.set_type(event_type)
        event_date = Date()
        event_date.set_yr_mon_day(
            random.randint(1850, 2000), random.randint(1, 12), random.randint(1, 28)
        )
        event.set_date_object(event_date)
        if (
            places and random.random() < 0.95
        ):  # 95% chance - almost every event has a place
            event.set_place_handle(random.choice(places))
        # Description (70% chance) - needed for HasData rule - increase to ensure variety
        if random.random() < 0.7:
            event_type_name = (
                str(event_type).split(".")[-1]
                if hasattr(event_type, "__name__")
                else "Event"
            )
            event.set_description(f"{event_type_name} event for {first_name}")
        # Add citations to event (40% chance)
        if citations and random.random() < 0.4:
            event.add_citation(random.choice(citations))
        # Add media to event (50% chance) - increase for HasGallery rule
        if media_objects and random.random() < 0.5:
            media_ref = MediaRef()
            media_ref.set_reference_handle(random.choice(media_objects))
            event.add_media_reference(media_ref)
        # Private flag (15% chance)
        if random.random() < 0.15:
            event.set_privacy(True)
        event_handle = db.add_event(event, trans)
        # Reload event from database and add attributes/tags/notes
        event = db.get_event_from_handle(event_handle)
        # Add attributes to event (30% chance) - use specific values for filter testing
        if random.random() < 0.3:
            attr = Attribute()
            attr_type = random.choice(ATTRIBUTE_TYPES)
            if attr_type == AttributeType.CUSTOM:
                attr.set_type((AttributeType.CUSTOM, "EventAttr"))
                attr.set_value("EventValue_42")  # Specific value for testing
            else:
                attr.set_type(attr_type)
                attr.set_value(f"EventValue_{random.randint(1, 100)}")
            event.add_attribute(attr)
        # Add notes to event (60% chance) - increase for HasNote rule - use specific note types
        if random.random() < 0.6:
            note = Note()
            note_type = random.choice(
                [NoteType.EVENT, NoteType.GENERAL, NoteType.RESEARCH, NoteType.ANALYSIS]
            )
            note.set_type(note_type)
            note.set(
                f"Event note: {random.choice(['Important', 'Verified', 'Needs verification', 'Research'])}"
            )
            note_handle = db.add_note(note, trans)
            event.add_note(note_handle)
        # Add tags to event (40% chance) - use canonical tag handle
        if tags and random.random() < 0.4:
            tag_name = random.choice(list(tags.keys()))
            tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
            if tag_handle:
                event.add_tag(tag_handle)
        # Commit event after adding attributes/tags to ensure they're saved
        db.commit_event(event, trans)
        event_ref = EventRef()
        event_ref.set_reference_handle(event_handle)
        person.add_event_ref(event_ref)

    # Attributes (50% chance) - increase and use specific values for filter testing
    if random.random() < 0.5:
        attr = Attribute()
        attr_type = random.choice(ATTRIBUTE_TYPES)
        if attr_type == AttributeType.CUSTOM:
            attr.set_type((AttributeType.CUSTOM, "CustomAttr"))
            attr.set_value("TestValue_42")  # Specific value for HasAttribute filter
        else:
            attr.set_type(attr_type)
            # Use some specific values for common attribute types
            if attr_type == AttributeType.OCCUPATION:
                attr.set_value(
                    random.choice(["Farmer", "Teacher", "Doctor", "Engineer", "Lawyer"])
                )
            elif attr_type == AttributeType.NATIONAL:
                attr.set_value(
                    random.choice(
                        ["American", "British", "French", "German", "Italian"]
                    )
                )
            else:
                attr.set_value(f"Value_{random.randint(1, 100)}")
        person.add_attribute(attr)

    # Notes (60% chance) - increase and use specific note types for filter testing
    if random.random() < 0.6:
        note = Note()
        # Use specific note types that filter rules might look for
        note_type = random.choice(
            [
                NoteType.GENERAL,
                NoteType.RESEARCH,
                NoteType.PERSON,
                NoteType.ANALYSIS,
                NoteType.TODO,
            ]
        )
        note.set_type(note_type)
        note.set(
            f"Note for {first_name} {surname}: {random.choice(['Important', 'Research', 'Verified', 'DNA match', 'Needs verification'])}"
        )
        note_handle = db.add_note(note, trans)
        person.add_note(note_handle)

    # Tags (60% chance) - use canonical tag handle
    if tags and random.random() < 0.6:
        tag_name = random.choice(list(tags.keys()))
        tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
        if tag_handle:
            person.add_tag(tag_handle)

    # Addresses (30% chance) - for HasAddress rule
    if random.random() < 0.3:
        address = Address()
        location = Location()
        street_num = random.randint(1, 9999)
        street_names = [
            "Main St",
            "Oak Ave",
            "Elm St",
            "Park Blvd",
            "Maple Dr",
            "Cedar Ln",
        ]
        location.set_street(f"{street_num} {random.choice(street_names)}")
        city_names = [
            "Springfield",
            "Franklin",
            "Georgetown",
            "Madison",
            "Washington",
            "Jefferson",
        ]
        location.set_city(city_names[random.randint(0, len(city_names) - 1)])
        state_names = ["IL", "NY", "CA", "TX", "FL", "PA"]
        location.set_state(state_names[random.randint(0, len(state_names) - 1)])
        location.set_country("USA")
        location.set_postal_code(f"{random.randint(10000, 99999)}")
        address.set_locality(location)
        # Date range for address (optional)
        if random.random() < 0.5:
            date = Date()
            date.set_yr_mon_day(
                random.randint(1900, 2000), random.randint(1, 12), random.randint(1, 28)
            )
            address.set_date_object(date)
        person.add_address(address)

    # Citations (40% chance - attach to person)
    if citations and random.random() < 0.4:
        person.add_citation(random.choice(citations))

    # Media (30% chance - attach to person)
    if media_objects and random.random() < 0.3:
        media_ref = MediaRef()
        media_ref.set_reference_handle(random.choice(media_objects))
        person.add_media_reference(media_ref)

    # Associations (20% chance) - for HasAssociation rule
    # Note: We'll add associations after people are created, in _add_special_filter_cases

    # Private flag (10% chance)
    if random.random() < 0.1:
        person.set_privacy(True)

    # Add person to database
    db.add_person(person, trans)
    return person


def _create_repository(db, trans, tags):
    """Create a repository with various attributes for filter testing."""
    repo = Repository()

    # Repository name
    repo_names = [
        "National Archives",
        "Library of Congress",
        "County Records Office",
        "Family History Library",
        "State Historical Society",
        "Local Church",
        "University Library",
        "Genealogical Society",
        "Public Records Office",
    ]
    repo.set_name(random.choice(repo_names))

    # Note: Repositories don't support attributes in Gramps

    # Notes (50% chance)
    if random.random() < 0.5:
        note = Note()
        note.set_type(
            random.choice([NoteType.REPO, NoteType.GENERAL, NoteType.RESEARCH])
        )
        note.set(
            f"Repository note: {random.choice(['Open to public', 'By appointment', 'Online access available'])}"
        )
        note_handle = db.add_note(note, trans)
        repo.add_note(note_handle)

    # Tags (60% chance) - use canonical tag handle
    if tags and random.random() < 0.6:
        tag_name = random.choice(list(tags.keys()))
        tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
        if tag_handle:
            repo.add_tag(tag_handle)

    # Private flag (10% chance)
    if random.random() < 0.1:
        repo.set_privacy(True)

    repo_handle = db.add_repository(repo, trans)
    return repo_handle


def _create_source(db, trans, repositories, tags):
    """Create a source with various attributes for filter testing."""
    source = Source()

    # Source title
    source_titles = [
        "Birth Certificate",
        "Death Certificate",
        "Marriage Record",
        "Census Record",
        "Military Service Record",
        "Immigration Record",
        "Passenger List",
        "Land Deed",
        "Will and Testament",
        "Newspaper Article",
    ]
    source.set_title(random.choice(source_titles))

    # Author
    if random.random() < 0.7:
        source.set_author(
            f"{generate_random_first_name(Person.MALE)} {generate_random_surname()}"
        )

    # Publication info
    if random.random() < 0.5:
        source.set_publication_info(f"Published in {random.randint(1800, 2020)}")

    # Repository reference (60% chance)
    if repositories and random.random() < 0.6:
        repo_ref = RepoRef()
        repo_ref.set_reference_handle(random.choice(repositories))
        repo_ref.set_call_number(f"Call-{random.randint(1000, 9999)}")
        source.add_repo_reference(repo_ref)

    # Attributes (40% chance)
    if random.random() < 0.4:
        attr = Attribute()
        attr_type = random.choice(ATTRIBUTE_TYPES)
        if attr_type == AttributeType.CUSTOM:
            attr.set_type((AttributeType.CUSTOM, "CustomAttr"))
        else:
            attr.set_type(attr_type)
        attr.set_value(f"Value_{random.randint(1, 100)}")
        source.add_attribute(attr)

    # Notes (50% chance)
    if random.random() < 0.5:
        note = Note()
        note.set_type(
            random.choice([NoteType.SOURCE, NoteType.SOURCE_TEXT, NoteType.GENERAL])
        )
        note.set(
            f"Source note: {random.choice(['Verified', 'Needs verification', 'Primary source', 'Secondary source'])}"
        )
        note_handle = db.add_note(note, trans)
        source.add_note(note_handle)

    # Tags (60% chance) - use canonical tag handle
    if tags and random.random() < 0.6:
        tag_name = random.choice(list(tags.keys()))
        tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
        if tag_handle:
            source.add_tag(tag_handle)

    # Private flag (10% chance)
    if random.random() < 0.1:
        source.set_privacy(True)

    source_handle = db.add_source(source, trans)
    return source_handle


def _create_citation(db, trans, sources, tags, media_objects=None):
    """Create a citation with various attributes for filter testing."""
    citation = Citation()

    # Source reference - ALWAYS set a source (required for HasSourceOf rules)
    if sources:
        citation.set_reference_handle(random.choice(sources))
    else:
        # If no sources available, this shouldn't happen, but handle gracefully
        raise ValueError("Cannot create citation without sources")

    # Page info
    if random.random() < 0.7:
        citation.set_page(f"Page {random.randint(1, 500)}")

    # Date
    if random.random() < 0.5:
        date = Date()
        date.set_yr_mon_day(
            random.randint(1800, 2020), random.randint(1, 12), random.randint(1, 28)
        )
        citation.set_date_object(date)

    # Confidence level
    confidence_levels = [0, 1, 2, 3, 4]  # Very Low to Very High
    citation.set_confidence_level(random.choice(confidence_levels))

    # Attributes (50% chance) - increase and use specific values for filter testing
    if random.random() < 0.5:
        attr = Attribute()
        attr_type = random.choice(ATTRIBUTE_TYPES)
        if attr_type == AttributeType.CUSTOM:
            attr.set_type((AttributeType.CUSTOM, "CitationAttr"))
            attr.set_value("CitationValue_42")  # Specific value for testing
        else:
            attr.set_type(attr_type)
            attr.set_value(f"CitationValue_{random.randint(1, 100)}")
        citation.add_attribute(attr)

    # Notes (80% chance) - increase for HasNote rule - use specific note types for filter testing
    if random.random() < 0.8:
        note = Note()
        # Use specific note types that filter rules might look for
        note_type = random.choice(
            [
                NoteType.CITATION,
                NoteType.GENERAL,
                NoteType.RESEARCH,
                NoteType.ANALYSIS,
                NoteType.TODO,
            ]
        )
        note.set_type(note_type)
        note.set(
            f"Citation note: {random.choice(['Direct evidence', 'Indirect evidence', 'Negative evidence', 'Primary source', 'Secondary source'])}"
        )
        note_handle = db.add_note(note, trans)
        citation.add_note(note_handle)

    # Private flag (10% chance)
    if random.random() < 0.1:
        citation.set_privacy(True)

    citation_handle = db.add_citation(citation, trans)
    # Reload citation from database and add tags
    citation = db.get_citation_from_handle(citation_handle)
    # Tags (60% chance) - use canonical tag handle
    if tags and random.random() < 0.6:
        tag_name = random.choice(list(tags.keys()))
        tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
        if tag_handle:
            citation.add_tag(tag_handle)
    # Commit citation after adding all attributes/tags/notes to ensure they're saved
    db.commit_citation(citation, trans)

    # Add media to citation AFTER adding to database (50% chance) - increase for HasGallery rule
    # This ensures the citation exists before we add media references
    if media_objects and random.random() < 0.5:
        citation = db.get_citation_from_handle(citation_handle)
        media_ref = MediaRef()
        media_ref.set_reference_handle(random.choice(media_objects))
        citation.add_media_reference(media_ref)
        db.commit_citation(citation, trans)

    return citation_handle


def _add_special_filter_cases(
    db, trans, people_handles, families_handles, citations, sources, media_objects, tags
):
    """Add special cases for filter rules that need specific arguments."""
    from datetime import datetime, timedelta

    # Ensure at least one media object has a citation with the first source (for media.HasSourceOf rule)
    # This ensures the test can use the first source ID and it will match
    if media_objects and sources and citations:
        first_source_handle = sources[0]
        # Find or create a citation that references the first source
        citation_with_first_source = None
        for citation_handle in citations:
            try:
                citation = db.get_citation_from_handle(citation_handle)
                if citation and citation.get_reference_handle() == first_source_handle:
                    citation_with_first_source = citation_handle
                    break
            except:
                continue

        if not citation_with_first_source:
            # Create a new citation with the first source
            from gramps.gen.lib import Citation

            citation = Citation()
            citation.set_reference_handle(first_source_handle)
            citation.set_page("TestPage")
            citation_handle = db.add_citation(citation, trans)
            citation_with_first_source = citation_handle

        # Find a media object that doesn't have this citation yet
        target_media_handle = None
        for media_handle in media_objects:
            try:
                media = db.get_media_from_handle(media_handle)
                if citation_with_first_source not in media.get_citation_list():
                    target_media_handle = media_handle
                    break
            except:
                continue

        if not target_media_handle:
            target_media_handle = media_objects[0]

        try:
            target_media = db.get_media_from_handle(target_media_handle)
            target_media.add_citation(citation_with_first_source)
            db.commit_media(target_media, trans)
        except Exception as e:
            # If this fails, it's not critical - we'll still have some media with citations
            pass

    # 0. Add associations to some people (for HasAssociation rule)
    if people_handles and len(people_handles) >= 2:
        # Add associations to 20% of people
        num_associations = int(len(people_handles) * 0.2)
        people_to_associate = random.sample(
            people_handles, min(num_associations, len(people_handles))
        )
        for person_handle in people_to_associate:
            person = db.get_person_from_handle(person_handle)
            # Find another person to associate with
            other_people = [h for h in people_handles if h != person_handle]
            if other_people:
                associate_handle = random.choice(other_people)
                person_ref = PersonRef()
                person_ref.set_reference_handle(associate_handle)
                # Set association type (optional)
                person_ref.set_relation("Friend")  # or "Colleague", "Neighbor", etc.
                person.add_person_ref(person_ref)
                db.commit_person(person, trans)

    # Get current date for ChangedSince rules
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)

    # 1. Ensure some events have dates with specific days of week for HasDayOfWeek rule
    # The rule uses get_dow() which returns 0-6 (0=Sunday, 1=Monday, etc.)
    # We need events with dates that have day-of-week calculated
    # Most events already have dates, but we should ensure at least some have full dates (year, month, day)
    event_handles = db.get_event_handles()
    if event_handles:
        # Check existing events - most should already have dates with day-of-week
        # The rule will work if events have dates with year, month, and day
        for event_handle in random.sample(
            event_handles, min(10, len(event_handles) // 10)
        ):
            event = db.get_event_from_handle(event_handle)
            if event.get_date_object():
                # Keep existing date but ensure it's valid
                pass
            else:
                # Add a date if missing
                date = Date()
                date.set_yr_mon_day(
                    random.randint(1900, 2000),
                    random.randint(1, 12),
                    random.randint(1, 28),
                )
                event.set_date_object(date)
                db.commit_event(event, trans)

    # 2. Add some citations with specific source IDs for HasSourceIdOf rule
    if citations and sources:
        # Get a specific source ID to use
        sample_source = db.get_source_from_handle(random.choice(sources))
        sample_source_id = sample_source.gramps_id
        # Add this source to some citations (they already have random sources, but ensure some have this one)
        for citation_handle in random.sample(citations, min(5, len(citations) // 10)):
            citation = db.get_citation_from_handle(citation_handle)
            # Set to the sample source
            citation.set_reference_handle(sample_source.handle)
            db.commit_citation(citation, trans)

    # 3. Add some events/citations with recent change dates for ChangedSince rule
    # Note: We can't directly set change dates, but we can ensure they exist
    # The ChangedSince rule typically uses the change time, which is set automatically

    # 4. Ensure some events have specific types for HasType rule
    # This is already handled in event creation, but ensure we have variety

    # 5. Add some citations with specific page strings for MatchesPageSubstringOf
    if citations:
        for citation_handle in random.sample(citations, min(10, len(citations) // 5)):
            citation = db.get_citation_from_handle(citation_handle)
            citation.set_page(f"Page {random.choice(['42', '100', '200', '300'])}")
            db.commit_citation(citation, trans)

    # 6. Add some sources with repository references for HasRepository rule
    # This is already handled, but ensure some have it

    # 7. Ensure some people have specific attribute values
    if people_handles:
        for person_handle in random.sample(
            people_handles, min(10, len(people_handles) // 10)
        ):
            person = db.get_person_from_handle(person_handle)
            # Add a specific attribute value if they don't have one
            if not person.get_attribute_list():
                attr = Attribute()
                attr.set_type(AttributeType.OCCUPATION)
                attr.set_value("Doctor")  # Specific value for testing
                person.add_attribute(attr)
                db.commit_person(person, trans)

    # 8. Ensure some events have specific note types
    event_handles = db.get_event_handles()
    if event_handles:
        for event_handle in random.sample(
            event_handles, min(10, len(event_handles) // 10)
        ):
            event = db.get_event_from_handle(event_handle)
            if not event.get_note_list():
                note = Note()
                note.set_type(NoteType.ANALYSIS)  # Specific note type
                note.set("Analysis note for filter testing")
                note_handle = db.add_note(note, trans)
                event.add_note(note_handle)
                db.commit_event(event, trans)

    # 9. Ensure some citations have tags, notes, and media for filter rules
    if citations:
        # Ensure at least 30% have tags (for HasTag rule)
        citations_without_tags = []
        for citation_handle in citations:
            citation = db.get_citation_from_handle(citation_handle)
            if not citation.get_tag_list():
                citations_without_tags.append(citation_handle)

        num_to_add_tags = max(
            0,
            int(len(citations) * 0.3) - (len(citations) - len(citations_without_tags)),
        )
        for citation_handle in random.sample(
            citations_without_tags, min(num_to_add_tags, len(citations_without_tags))
        ):
            if tags:
                citation = db.get_citation_from_handle(citation_handle)
                tag_name = random.choice(list(tags.keys()))
                tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
                if tag_handle:
                    citation.add_tag(tag_handle)
                db.commit_citation(citation, trans)

        # Ensure at least 30% have notes (for HasNote rule)
        citations_without_notes = []
        for citation_handle in citations:
            citation = db.get_citation_from_handle(citation_handle)
            if not citation.get_note_list():
                citations_without_notes.append(citation_handle)

        # Add notes to some citations that don't have them
        num_to_add_notes = max(
            0,
            int(len(citations) * 0.3) - (len(citations) - len(citations_without_notes)),
        )
        for citation_handle in random.sample(
            citations_without_notes, min(num_to_add_notes, len(citations_without_notes))
        ):
            citation = db.get_citation_from_handle(citation_handle)
            note = Note()
            note.set_type(NoteType.CITATION)  # Specific note type
            note.set("Citation analysis note")
            note_handle = db.add_note(note, trans)
            citation.add_note(note_handle)
            db.commit_citation(citation, trans)

        # Ensure at least 30% have media (for HasGallery rule)
        citations_without_media = []
        for citation_handle in citations:
            citation = db.get_citation_from_handle(citation_handle)
            if not citation.get_media_list():
                citations_without_media.append(citation_handle)

        # Add media to some citations that don't have it
        num_to_add_media = max(
            0,
            int(len(citations) * 0.3) - (len(citations) - len(citations_without_media)),
        )
        for citation_handle in random.sample(
            citations_without_media, min(num_to_add_media, len(citations_without_media))
        ):
            if media_objects:
                citation = db.get_citation_from_handle(citation_handle)
                media_ref = MediaRef()
                media_ref.set_reference_handle(random.choice(media_objects))
                citation.add_media_reference(media_ref)
                db.commit_citation(citation, trans)

    # 10. Ensure families have tags, notes, and attributes for filter rules
    if families_handles:
        # Ensure at least 30% have tags (for HasTag rule)
        families_without_tags = []
        for family_handle in families_handles:
            family = db.get_family_from_handle(family_handle)
            if not family.get_tag_list():
                families_without_tags.append(family_handle)

        num_to_add_tags = max(
            0,
            int(len(families_handles) * 0.3)
            - (len(families_handles) - len(families_without_tags)),
        )
        for family_handle in random.sample(
            families_without_tags, min(num_to_add_tags, len(families_without_tags))
        ):
            if tags:
                family = db.get_family_from_handle(family_handle)
                tag_name = random.choice(list(tags.keys()))
                tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
                if tag_handle:
                    family.add_tag(tag_handle)
                db.commit_family(family, trans)

        # Ensure at least 30% have notes (for HasNote rule)
        families_without_notes = []
        for family_handle in families_handles:
            family = db.get_family_from_handle(family_handle)
            if not family.get_note_list():
                families_without_notes.append(family_handle)

        num_to_add_notes = max(
            0,
            int(len(families_handles) * 0.3)
            - (len(families_handles) - len(families_without_notes)),
        )
        for family_handle in random.sample(
            families_without_notes, min(num_to_add_notes, len(families_without_notes))
        ):
            family = db.get_family_from_handle(family_handle)
            note = Note()
            note.set_type(NoteType.FAMILY)
            note.set("Family note for filter testing")
            note_handle = db.add_note(note, trans)
            family.add_note(note_handle)
            db.commit_family(family, trans)

        # Ensure at least 30% have attributes (for HasAttribute rule)
        families_without_attrs = []
        for family_handle in families_handles:
            family = db.get_family_from_handle(family_handle)
            if not family.get_attribute_list():
                families_without_attrs.append(family_handle)

        num_to_add_attrs = max(
            0,
            int(len(families_handles) * 0.3)
            - (len(families_handles) - len(families_without_attrs)),
        )
        for family_handle in random.sample(
            families_without_attrs, min(num_to_add_attrs, len(families_without_attrs))
        ):
            family = db.get_family_from_handle(family_handle)
            attr = Attribute()
            attr_type = random.choice(ATTRIBUTE_TYPES)
            if attr_type == AttributeType.CUSTOM:
                attr.set_type((AttributeType.CUSTOM, "FamilyAttr"))
                attr.set_value("FamilyValue_42")
            else:
                attr.set_type(attr_type)
                attr.set_value(f"FamilyValue_{random.randint(1, 100)}")
            family.add_attribute(attr)
            db.commit_family(family, trans)

    # 11. Ensure some events have attributes, tags, notes, and media for filter rules
    event_handles = db.get_event_handles()
    if event_handles:
        # Ensure at least 30% have attributes (for HasAttribute rule)
        events_without_attrs = []
        for event_handle in event_handles:
            event = db.get_event_from_handle(event_handle)
            if not event.get_attribute_list():
                events_without_attrs.append(event_handle)

        num_to_add_attrs = max(
            0,
            int(len(event_handles) * 0.3)
            - (len(event_handles) - len(events_without_attrs)),
        )
        for event_handle in random.sample(
            events_without_attrs, min(num_to_add_attrs, len(events_without_attrs))
        ):
            event = db.get_event_from_handle(event_handle)
            attr = Attribute()
            attr_type = random.choice(ATTRIBUTE_TYPES)
            if attr_type == AttributeType.CUSTOM:
                attr.set_type((AttributeType.CUSTOM, "EventAttr"))
                attr.set_value("EventValue_42")
            else:
                attr.set_type(attr_type)
                attr.set_value(f"EventValue_{random.randint(1, 100)}")
            event.add_attribute(attr)
            db.commit_event(event, trans)

        # Ensure at least 30% have tags (for HasTag rule)
        events_without_tags = []
        for event_handle in event_handles:
            event = db.get_event_from_handle(event_handle)
            if not event.get_tag_list():
                events_without_tags.append(event_handle)

        num_to_add_tags = max(
            0,
            int(len(event_handles) * 0.3)
            - (len(event_handles) - len(events_without_tags)),
        )
        for event_handle in random.sample(
            events_without_tags, min(num_to_add_tags, len(events_without_tags))
        ):
            if tags:
                event = db.get_event_from_handle(event_handle)
                tag_name = random.choice(list(tags.keys()))
                tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
                if tag_handle:
                    event.add_tag(tag_handle)
                db.commit_event(event, trans)

        # Ensure at least 40% have notes
        events_without_notes = []
        for event_handle in event_handles:
            event = db.get_event_from_handle(event_handle)
            if not event.get_note_list():
                events_without_notes.append(event_handle)

        num_to_add_notes = max(
            0,
            int(len(event_handles) * 0.4)
            - (len(event_handles) - len(events_without_notes)),
        )
        for event_handle in random.sample(
            events_without_notes, min(num_to_add_notes, len(events_without_notes))
        ):
            event = db.get_event_from_handle(event_handle)
            note = Note()
            note.set_type(NoteType.ANALYSIS)  # Specific note type
            note.set("Analysis note for filter testing")
            note_handle = db.add_note(note, trans)
            event.add_note(note_handle)
            db.commit_event(event, trans)

        # Ensure at least 30% have media
        events_without_media = []
        for event_handle in event_handles:
            event = db.get_event_from_handle(event_handle)
            if not event.get_media_list():
                events_without_media.append(event_handle)

        num_to_add_media = max(
            0,
            int(len(event_handles) * 0.3)
            - (len(event_handles) - len(events_without_media)),
        )
        for event_handle in random.sample(
            events_without_media, min(num_to_add_media, len(events_without_media))
        ):
            if media_objects:
                event = db.get_event_from_handle(event_handle)
                media_ref = MediaRef()
                media_ref.set_reference_handle(random.choice(media_objects))
                event.add_media_reference(media_ref)
                db.commit_event(event, trans)

        # Ensure at least 50% have descriptions (for HasData rule)
        events_without_desc = []
        for event_handle in event_handles:
            event = db.get_event_from_handle(event_handle)
            if not event.get_description():
                events_without_desc.append(event_handle)

        num_to_add_desc = max(
            0,
            int(len(event_handles) * 0.5)
            - (len(event_handles) - len(events_without_desc)),
        )
        for event_handle in random.sample(
            events_without_desc, min(num_to_add_desc, len(events_without_desc))
        ):
            event = db.get_event_from_handle(event_handle)
            event_type_name = "Event"
            if event.get_type():
                event_type = event.get_type()
                if hasattr(event_type, "__name__"):
                    event_type_name = event_type.__name__
                else:
                    event_type_name = str(event_type).split(".")[-1]
            event.set_description(f"{event_type_name} description for filter testing")
            db.commit_event(event, trans)


def _create_media(db, trans, citations, sources, tags):
    """Create a media object with various attributes for filter testing."""
    media = Media()

    # Media path/description
    media_paths = [
        "photos/photo001.jpg",
        "documents/certificate.pdf",
        "scans/scan001.tif",
        "images/image001.png",
        "records/record001.jpg",
        "photos/portrait.jpg",
    ]
    media.set_path(random.choice(media_paths))

    # Mime type
    mime_types = ["image/jpeg", "image/png", "image/tiff", "application/pdf"]
    media.set_mime_type(random.choice(mime_types))

    # Description
    if random.random() < 0.7:
        media.set_description(
            f"Media description: {random.choice(['Family photo', 'Document scan', 'Certificate', 'Portrait'])}"
        )

    # Date
    if random.random() < 0.5:
        date = Date()
        date.set_yr_mon_day(
            random.randint(1800, 2020), random.randint(1, 12), random.randint(1, 28)
        )
        media.set_date_object(date)

    # Note: Citations and sources will be added to media after citations are created
    # This is done in the main generate_database function

    # Attributes (40% chance)
    if random.random() < 0.4:
        attr = Attribute()
        attr_type = random.choice(ATTRIBUTE_TYPES)
        if attr_type == AttributeType.CUSTOM:
            attr.set_type((AttributeType.CUSTOM, "CustomAttr"))
        else:
            attr.set_type(attr_type)
        attr.set_value(f"Value_{random.randint(1, 100)}")
        media.add_attribute(attr)

    # Notes (50% chance)
    if random.random() < 0.5:
        note = Note()
        note.set_type(
            random.choice([NoteType.MEDIA, NoteType.GENERAL, NoteType.PERSON])
        )
        note.set(
            f"Media note: {random.choice(['High quality', 'Needs restoration', 'Original', 'Copy'])}"
        )
        note_handle = db.add_note(note, trans)
        media.add_note(note_handle)

    # Tags (60% chance) - use canonical tag handle
    if tags and random.random() < 0.6:
        tag_name = random.choice(list(tags.keys()))
        tag_handle = _get_canonical_tag_handle(db, tag_name, tags)
        if tag_handle:
            media.add_tag(tag_handle)

    # Private flag (10% chance)
    if random.random() < 0.1:
        media.set_privacy(True)

    media_handle = db.add_media(media, trans)
    return media_handle


def main():
    """Command-line interface for database generation."""
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Generate a Gramps database with specified characteristics.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a database with 1000 people
  %(prog)s 1000

  # Generate a database with 10000 people and save to specific path
  %(prog)s 10000 --path /tmp/my_database

  # Generate a database with a specific seed for reproducibility
  %(prog)s 5000 --seed 42

  # Generate a database using a different backend
  %(prog)s 2000 --dbid bsddb

  # Quiet mode (suppress progress messages)
  %(prog)s 1000 --quiet
        """,
    )

    parser.add_argument(
        "num_people",
        type=int,
        help="Approximate number of people to create in the database",
    )

    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="Path where to create the database (default: Gramps default database directory)",
    )

    parser.add_argument(
        "--dbid",
        type=str,
        default="sqlite",
        help="Database backend ID (default: sqlite). Options: sqlite, bsddb, etc.",
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility. Same seed generates identical database.",
    )

    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress progress messages during generation",
    )

    args = parser.parse_args()

    # Suppress print statements if quiet mode
    if args.quiet:
        import io
        import contextlib

        # Redirect stdout to suppress progress messages
        with contextlib.redirect_stdout(io.StringIO()):
            try:
                path = generate_database(
                    args.num_people, db_path=args.path, dbid=args.dbid, seed=args.seed
                )
            except Exception as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
        # In quiet mode, only print the path
        print(path)
    else:
        try:
            path = generate_database(
                args.num_people, db_path=args.path, dbid=args.dbid, seed=args.seed
            )
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"Database created at: {path}")


if __name__ == "__main__":
    main()
