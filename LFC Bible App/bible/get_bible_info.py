"""
This has code that is relevant to the core and proper functioning
of the bible to provide an accurate and inclusive experience for
all, with all te versions the testaments the xml parsings, verse
retrieval is all here.

"""


import xml.etree.ElementTree as ET

OLD_TESTAMENT = [
    "Genesis",
    "Exodus",
    "Leviticus",
    "Numbers",
    "Deuteronomy",
    "Joshua",
    "Judges",
    "Ruth",
    "1 Samuel",
    "2 Samuel",
    "1 Kings",
    "2 Kings",
    "1 Chronicles",
    "2 Chronicles",
    "Ezra",
    "Nehemiah",
    "Esther",
    "Job",
    "Psalms",
    "Proverbs",
    "Ecclesiastes",
    "Song of Solomon",
    "Isaiah",
    "Jeremiah",
    "Lamentations",
    "Ezekiel",
    "Daniel",
    "Hosea",
    "Joel",
    "Amos",
    "Obadiah",
    "Jonah",
    "Micah",
    "Nahum",
    "Habakkuk",
    "Zephaniah",
    "Haggai",
    "Zechariah",
    "Malachi"
 ]

NEW_TESTAMENT = [
    "Matthew",
    "Mark",
    "Luke",
    "John",
    "Acts",
    "Romans",
    "1 Corinthians",
    "2 Corinthians",
    "Galatians",
    "Ephesians",
    "Philippians",
    "Colossians",
    "1 Thessalonians",
    "2 Thessalonians",
    "1 Timothy",
    "2 Timothy",
    "Titus",
    "Philemon",
    "Hebrews",
    "James",
    "1 Peter",
    "2 Peter",
    "1 John",
    "2 John",
    "3 John",
    "Jude",
    "Revelation"
]

BIBLE_VERSION_MAP = {
    "English (King James Version)": "bible/en_kjv.xml",
    "English (Basic English)": "bible/en_bbe.xml",
    "French (Le Bible de I'Épée)": "bible/fr_apee.xml",
    "Spanish (Reina Valera)": "bible/es_rvr.xml",
    "Russian (Синодальный перевод)": "bible/ru_synodal.xml",
    "Arabic": "bible/ar_svd.xml",
    "German": "bible/de_schlachter.xml",
    "Greek (Modern)": "bible/el_greek.xml",
    "Chinese (Chinese Union Version)": "bible/zh_cuv.xml",
    "Chinese (New Chinese Version)": "bible/zh_ncv.xml",
    "Finnish": "bible/fi_finnish.xml",
    "Finnish (Pyhä Raamattu)": "bible/fi_pr.xml",
    "Vietnamese (Tiếng Việt)": "bible/vi_vietnamese.xml"
}

def find_verse(book_name, chapter_number, verse_number, xml_file):
    # Load and parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Construct XPath query
    query = f"./b[@n='{book_name}']/c[@n='{chapter_number}']/v[@n='{verse_number}']"

    # Find the verse
    verse = root.find(query)
    if verse is not None:
        return verse.text.replace('{', '(').replace('}', ')')

def parse_books_and_chapters(xml_path):
    # Load and parse the XML file
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Data structure to hold the count of chapters and verses
    books_info = {}

    # Iterate through each book in the XML
    for book in root.findall('b'):
        book_name = book.attrib.get('n', 'Genesis')
        chapters_info = {}

        # Iterate through each chapter in the book
        for chapter in book.findall('c'):
            chapter_number = chapter.attrib.get('number', len(chapters_info) + 1)
            # Count the number of verses in the chapter
            verses_count = len(chapter.findall('v'))
            chapters_info[chapter_number] = verses_count

        books_info[book_name] = chapters_info

    return books_info




