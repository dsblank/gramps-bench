#!/usr/bin/env python3
"""
Pytest tests for verifying that each filter rule matches some items but not all items.
Each rule gets its own test function for easier debugging.
"""

import os
import sys
import importlib
import inspect
import pytest
import time
import json
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

# Set up Gramps environment
gramps_resources = os.environ.get("GRAMPS_RESOURCES")
if not gramps_resources:
    # Try to auto-detect
    for path in [
        "/snap/gramps/current/usr/share",
        "/usr/share/gramps",
        "/usr/local/share/gramps",
    ]:
        if os.path.exists(os.path.join(path, "gramps", "authors.xml")):
            gramps_resources = path
            break
    if gramps_resources:
        os.environ["GRAMPS_RESOURCES"] = gramps_resources

from gramps.gen.db.utils import make_database
from gramps.gen.user import User
from gramps.gen.filters import GenericFilter
from gramps.gen.filters.rules import Rule
from gramps.cli.clidbman import CLIDbManager
from gramps.gen.dbstate import DbState
from gramps.gen.db.dbconst import DBBACKEND

# Add Gramps source to path if needed
gramps_source = os.path.expanduser("~/gramps/gramps")
if os.path.exists(gramps_source) and gramps_source not in sys.path:
    sys.path.insert(0, gramps_source)


# Storage for timing data
_timing_data = {}


# Rules that are not supported or require complex setup
UNSUPPORTED_RULES = {
    "MatchesFilter",  # Requires filter objects
    "MatchesPersonFilter",  # Requires filter objects
    "MatchesPlaceFilter",  # Requires filter objects
    "MatchesSourceFilter",  # Requires filter objects
    "MatchesRepositoryFilter",  # Requires filter objects
    "MatchesEventFilter",  # Requires filter objects
    "ChangedSince",  # Requires change tracking which we can't easily control
    "HasReferenceCountOf",  # Complex counting logic
    "ChildHasIdOf",  # Requires specific child IDs
    "HasAttribute",  # Repositories don't support attributes in Gramps
    # FilterMatch rules require base filters to be set up in CustomFilters
    "IsChildOfFilterMatch",
    "IsParentOfFilterMatch",
    "IsSiblingOfFilterMatch",
    "IsSpouseOfFilterMatch",
    "IsAncestorOfFilterMatch",
    "IsDescendantOfFilterMatch",
    "IsDescendantFamilyOfFilterMatch",
    "HasCommonAncestorWithFilterMatch",
    # Rules that require special database setup
    "IsDefaultPerson",  # Requires default person to be set
    "IsLessThanNthGenerationAncestorOfDefaultPerson",  # Requires default person
    "IsLessThanNthGenerationAncestorOfBookmarked",  # Requires bookmarks
    "IsBookmarked",  # Requires bookmarks to be set
    "RelationshipPathBetweenBookmarks",  # Requires bookmarks
    "DeepRelationshipPathBetween",  # Complex relationship path
    "RelationshipPathBetween",  # Complex relationship path
    "HasLDS",  # Requires LDS data
}


def get_all_rules():
    """Get all filter rule classes from the rules directory."""
    rules = {}
    
    # Categories to check
    categories = ["person", "family", "event", "place", "source", "citation", 
                  "repository", "media", "note"]
    
    for category in categories:
        # Import the category module
        try:
            module_name = f"gramps.gen.filters.rules.{category}"
            module = importlib.import_module(module_name)
            
            # Get all classes from the module
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, Rule) and obj != Rule and 
                    obj.__module__.startswith(f"gramps.gen.filters.rules.{category}")):
                    rule_key = f"{category}.{name}"
                    rules[rule_key] = {
                        "category": category,
                        "name": name,
                        "class": obj
                    }
        except Exception as e:
            # Silently continue if module doesn't exist or has issues
            continue
    
    return rules


def get_sample_value(db, category, field_name):
    """Get a sample value from the database for a given field."""
    try:
        if category == "person":
            handles = db.get_person_handles()[:10]
            for handle in handles:
                obj = db.get_person_from_handle(handle)
                if field_name == "gramps_id":
                    return obj.gramps_id
                elif field_name == "tag":
                    if obj.tag_list:
                        return obj.tag_list[0]
        elif category == "family":
            handles = db.get_family_handles()[:10]
            for handle in handles:
                obj = db.get_family_from_handle(handle)
                if field_name == "gramps_id":
                    return obj.gramps_id
        elif category == "event":
            handles = db.get_event_handles()[:10]
            for handle in handles:
                obj = db.get_event_from_handle(handle)
                if field_name == "gramps_id":
                    return obj.gramps_id
        elif category == "source":
            handles = db.get_source_handles()[:10]
            for handle in handles:
                obj = db.get_source_from_handle(handle)
                if field_name == "gramps_id":
                    return obj.gramps_id
        elif category == "citation":
            handles = db.get_citation_handles()[:10]
            for handle in handles:
                obj = db.get_citation_from_handle(handle)
                if field_name == "gramps_id":
                    return obj.gramps_id
    except:
        pass
    return ""


@pytest.fixture(scope="module")
def database():
    """
    Load the database once for all tests.
    
    Expects a database with 500 people generated by database_generator.py.
    To regenerate: python database_generator.py --path <GRAMPS_DATABASE_PATH> 500
    
    If GRAMPS_DATABASE environment variable is set, loads that database by name.
    If GRAMPS_DATABASE_PATH is set, loads the database from that path.
    Otherwise, creates a temporary empty database for testing.
    """
    user = User()
    db = None
    temp_dir = None
    
    db_name = os.environ.get("GRAMPS_DATABASE")
    db_path = os.environ.get("GRAMPS_DATABASE_PATH")
    
    if db_name:
        # Load database by name
        dbstate = DbState()
        dbman = CLIDbManager(dbstate)
        
        # Get list of databases and find the one with matching name
        db_list = dbman.family_tree_list()
        found_path = None
        
        for db_info in db_list:
            if db_info[0] == db_name:  # db_info is (name, path)
                found_path = db_info[1]
                break
        
        if not found_path:
            pytest.skip(f"Database '{db_name}' not found")
        
        # Read backend from database directory
        backend_path = os.path.join(found_path, DBBACKEND)
        backend_id = "sqlite"  # default
        if os.path.exists(backend_path):
            with open(backend_path, "r", encoding="utf-8") as f:
                backend_id = f.read().strip()
        
        db = make_database(backend_id)
        db.load(found_path)
    elif db_path:
        # Load database from path (original behavior)
        db = make_database("sqlite")
        db.load(db_path)
    else:
        # Create a temporary database
        temp_dir = tempfile.mkdtemp()
        db = make_database("sqlite")
        db.load(temp_dir)
    
    yield db
    
    # Cleanup
    if db:
        db.close()
    if temp_dir and os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


def get_handles_for_category(db, category):
    """Get all handles for a given category."""
    if category == "person":
        return db.get_person_handles()
    elif category == "family":
        return db.get_family_handles()
    elif category == "event":
        return db.get_event_handles()
    elif category == "place":
        return db.get_place_handles()
    elif category == "source":
        return db.get_source_handles()
    elif category == "citation":
        return db.get_citation_handles()
    elif category == "repository":
        return db.get_repository_handles()
    elif category == "media":
        return db.get_media_handles()
    elif category == "note":
        return db.get_note_handles()
    else:
        return []


def get_object_from_handle(db, category, handle):
    """Get an object from a handle for a given category."""
    if category == "person":
        return db.get_person_from_handle(handle)
    elif category == "family":
        return db.get_family_from_handle(handle)
    elif category == "event":
        return db.get_event_from_handle(handle)
    elif category == "place":
        return db.get_place_from_handle(handle)
    elif category == "source":
        return db.get_source_from_handle(handle)
    elif category == "citation":
        return db.get_citation_from_handle(handle)
    elif category == "repository":
        return db.get_repository_from_handle(handle)
    elif category == "media":
        return db.get_media_from_handle(handle)
    elif category == "note":
        return db.get_note_from_handle(handle)
    else:
        return None


def create_rule_with_args(rule_class, rule_name, category, db, handles):
    """Create a rule instance with appropriate arguments based on the rule type."""
    rule_name_lower = rule_name.lower()
    
    # Get the rule's labels to determine how many arguments it needs
    if hasattr(rule_class, "labels"):
        num_args = len(rule_class.labels)
    else:
        num_args = 0
    
    # Create rule with smart defaults
    if num_args == 0:
        args = []
    else:
        args = [""] * num_args
        
        # Set smart defaults for common rules
        # Check specific rules first before generic ones
        if "fatherhasidof" in rule_name_lower or "motherhasidof" in rule_name_lower:
            # FatherHasIdOf/MotherHasIdOf need person IDs from families
            if category == "family" and num_args > 0:
                # Find a family with a father/mother and get their ID
                # We need to find a person that actually exists as a father/mother
                person_id = None
                for handle in handles:
                    try:
                        family = get_object_from_handle(db, category, handle)
                        if family:
                            if "father" in rule_name_lower and family.get_father_handle():
                                try:
                                    person = db.get_person_from_handle(family.get_father_handle())
                                    if person:
                                        person_id = person.gramps_id
                                        break
                                except:
                                    continue
                            elif "mother" in rule_name_lower and family.get_mother_handle():
                                try:
                                    person = db.get_person_from_handle(family.get_mother_handle())
                                    if person:
                                        person_id = person.gramps_id
                                        break
                                except:
                                    continue
                    except:
                        continue
                # If still no ID found, try to get any person ID from the database
                if not person_id:
                    try:
                        person_handles = db.get_person_handles()
                        if person_handles:
                            person = db.get_person_from_handle(person_handles[0])
                            person_id = person.gramps_id
                    except:
                        pass
                args[0] = person_id or "I0000"
        elif "idof" in rule_name_lower or "hasidof" in rule_name_lower:
            if num_args > 0:
                # Get an actual gramps_id from the database
                sample_id = get_sample_value(db, category, "gramps_id")
                if not sample_id and handles:
                    # Fallback: get ID from first handle
                    try:
                        obj = get_object_from_handle(db, category, handles[0])
                        if obj:
                            sample_id = obj.gramps_id
                    except:
                        pass
                # Use category-specific default IDs if still not found
                if not sample_id:
                    id_prefixes = {
                        "person": "I",
                        "family": "F",
                        "event": "E",
                        "place": "P",
                        "source": "S",
                        "citation": "C",
                        "repository": "R",
                        "media": "O",
                        "note": "N",
                    }
                    prefix = id_prefixes.get(category, "I")
                    sample_id = f"{prefix}0000"
                args[0] = sample_id
        elif "hastag" in rule_name_lower:
            if num_args > 0:
                # Try to find a tag that's actually used by objects in this category
                tag_name = None
                # First, try to get a tag from an object
                for handle in handles[:50]:
                    try:
                        obj = get_object_from_handle(db, category, handle)
                        if obj:
                            tag_list = obj.get_tag_list()
                            if tag_list:
                                # tag_list contains tag handles, get the tag name
                                tag_handle = tag_list[0]
                                tag = db.get_tag_from_handle(tag_handle)
                                tag_name = tag.get_name()
                                break
                    except:
                        continue
                # If no tag found on objects, try to get any tag from the database
                if not tag_name:
                    try:
                        tag_handles = db.get_tag_handles()
                        if tag_handles:
                            tag = db.get_tag_from_handle(tag_handles[0])
                            tag_name = tag.get_name()
                    except:
                        pass
                args[0] = tag_name or "Important"
        elif "hasattribute" in rule_name_lower:
            if num_args > 0:
                found_attr = False
                for handle in handles[:20]:
                    try:
                        obj = get_object_from_handle(db, category, handle)
                        if obj:
                            attrs = obj.get_attribute_list()
                            if attrs:
                                attr = attrs[0]
                                attr_type = attr.get_type()
                                if isinstance(attr_type, tuple):
                                    args[0] = attr_type[1]
                                else:
                                    args[0] = str(attr_type)
                                found_attr = True
                                break
                    except:
                        continue
                if not found_attr:
                    args[0] = "TestValue_42"
        elif "hasnotematchingsubstringof" in rule_name_lower:
            # HasNoteMatchingSubstringOf needs a substring that appears in some but not all notes
            if num_args > 0:
                # Collect note texts to find a common substring
                note_texts = []
                for handle in handles[:100]:
                    try:
                        obj = get_object_from_handle(db, category, handle)
                        if obj:
                            note_list = obj.get_note_list()
                            if note_list:
                                for note_handle in note_list:
                                    note = db.get_note_from_handle(note_handle)
                                    if note and note.get():
                                        note_texts.append(note.get())
                                        if len(note_texts) >= 20:
                                            break
                            if len(note_texts) >= 20:
                                break
                    except:
                        continue
                if note_texts:
                    # Find a common word that appears in multiple notes but not all
                    from collections import Counter
                    all_words = []
                    for text in note_texts:
                        words = text.lower().split()
                        all_words.extend(words)
                    word_counts = Counter(all_words)
                    # Find a word that appears in at least 30% but not 100% of notes
                    target_min = max(2, int(len(note_texts) * 0.3))
                    target_max = int(len(note_texts) * 0.9)
                    common_word = None
                    for word, count in word_counts.most_common(20):
                        if target_min <= count <= target_max:
                            common_word = word
                            break
                    if common_word:
                        args[0] = common_word
                    else:
                        # Fallback: use a common prefix
                        if "note" in note_texts[0].lower():
                            args[0] = "note"
                        elif ":" in note_texts[0]:
                            args[0] = note_texts[0].split(":")[0].lower()
                        else:
                            args[0] = note_texts[0].split()[0].lower() if note_texts[0].split() else "test"
                else:
                    args[0] = "test"
        elif "hasnote" in rule_name_lower and "hasnotetype" not in rule_name_lower:
            # HasNote for notes needs: text, note_type
            if category == "note" and num_args >= 2:
                # Get a sample note's text and type
                if handles:
                    try:
                        note = get_object_from_handle(db, category, handles[0])
                        if note:
                            note_text = note.get()
                            if note_text:
                                # Use first few words as substring
                                words = note_text.split()[:3]
                                args[0] = " ".join(words) if words else "test"
                            else:
                                args[0] = "test"
                            note_type = note.get_type()
                            if note_type:
                                if isinstance(note_type, tuple):
                                    args[1] = note_type[1]
                                else:
                                    # Get XML string representation
                                    try:
                                        args[1] = note_type.xml_str() if hasattr(note_type, 'xml_str') else str(note_type)
                                    except:
                                        args[1] = "General"
                            else:
                                args[1] = "General"
                        else:
                            args[0] = "test"
                            args[1] = "General"
                    except:
                        args[0] = "test"
                        args[1] = "General"
                else:
                    args[0] = "test"
                    args[1] = "General"
            elif num_args >= 2:
                # HasNote for other objects checks for number of notes - needs count arguments
                # Count how many objects have notes
                with_notes = sum(1 for h in handles[:50] 
                                if get_object_from_handle(db, category, h) and 
                                get_object_from_handle(db, category, h).get_note_list())
                # Use a count that will match some but not all
                if with_notes > 0:
                    # Use "1" as the number to match (at least 1 note)
                    args[0] = "1"  # Number of instances
                    args[1] = ">="  # Number must be (>=, =, <=)
                else:
                    args[0] = "0"
                    args[1] = "="
            elif num_args > 0:
                # Fallback: try to find a note type
                found_note_type = False
                for handle in handles[:20]:
                    try:
                        obj = get_object_from_handle(db, category, handle)
                        if obj:
                            note_list = obj.get_note_list()
                            if note_list:
                                note_handle = note_list[0]
                                note = db.get_note_from_handle(note_handle)
                                note_type = note.get_type()
                                if isinstance(note_type, tuple):
                                    args[0] = note_type[1]
                                else:
                                    args[0] = str(note_type)
                                found_note_type = True
                                break
                    except:
                        continue
                if not found_note_type:
                    args[0] = "Analysis"
        elif "hasnotetype" in rule_name_lower:
            if num_args > 0:
                found_note_type = False
                for handle in handles[:20]:
                    try:
                        obj = get_object_from_handle(db, category, handle)
                        if obj:
                            note_list = obj.get_note_list()
                            if note_list:
                                note_handle = note_list[0]
                                note = db.get_note_from_handle(note_handle)
                                note_type = note.get_type()
                                if isinstance(note_type, tuple):
                                    args[0] = note_type[1]
                                else:
                                    args[0] = str(note_type)
                                found_note_type = True
                                break
                    except:
                        continue
                if not found_note_type:
                    args[0] = "Analysis"
        elif "changedsince" in rule_name_lower:
            if num_args > 0:
                from datetime import datetime, timedelta
                past_date = datetime.now() - timedelta(days=7)
                args[0] = past_date.strftime("%Y-%m-%d")
        elif "hassourceidof" in rule_name_lower or "regexpsourceidof" in rule_name_lower:
            if num_args > 0:
                source_handles = db.get_source_handles()
                if source_handles:
                    source = db.get_source_from_handle(source_handles[0])
                    args[0] = source.gramps_id
                else:
                    args[0] = "S0001"
        elif "hasdayofweek" in rule_name_lower:
            if num_args > 0:
                event_handles = db.get_event_handles()
                if event_handles:
                    for event_handle in event_handles[:50]:
                        try:
                            event = db.get_event_from_handle(event_handle)
                            date_obj = event.get_date_object()
                            if date_obj:
                                # get_dow() returns 0-6 (0=Sunday, 1=Monday, etc.)
                                dow = date_obj.get_dow()
                                if dow is not None:
                                    args[0] = str(dow)
                                    break
                        except:
                            continue
                if not args[0] or args[0] == "":
                    args[0] = "1"  # Monday (default)
        elif "hastype" in rule_name_lower:
            if num_args > 0:
                if category == "event":
                    args[0] = "Birth"
                elif category == "note":
                    args[0] = "General"
        elif "hasevent" in rule_name_lower and category == "person":
            # HasEvent for persons needs: event_type, date, place, description, main_participants, primary_role
            # Use just event type to match some but not all (leave other fields empty)
            if num_args >= 6:
                # Find a common event type from the database
                event_type = "Birth"
                event_handles = db.get_event_handles()
                for event_handle in event_handles[:100]:
                    try:
                        event = db.get_event_from_handle(event_handle)
                        if event and event.get_type():
                            event_type_obj = event.get_type()
                            if hasattr(event_type_obj, 'xml_str'):
                                event_type = event_type_obj.xml_str()
                                break
                    except:
                        continue
                args[0] = event_type  # Event type (XML string like "Birth")
                args[1] = ""  # Date (empty = match any date)
                args[2] = ""  # Place (empty = match any place)
                args[3] = ""  # Description (empty = match any description)
                args[4] = ""  # Main Participants (empty = match any)
                args[5] = "0"  # Primary Role (0 = any role, 1 = primary only)
        elif "hasevent" in rule_name_lower:
            # HasEvent for events needs: event_type, date
            if category == "event" and num_args >= 2:
                # Use a specific event type that only some events have (e.g., "Marriage")
                args[0] = "Marriage"  # Not all events are marriages
                args[1] = ""  # Leave date empty (matches any date)
        elif "hasdata" in rule_name_lower and category == "event":
            # HasData for events needs: event_type, date, place, description
            if num_args >= 4:
                # Use a specific event type
                args[0] = "Birth"  # Common but not all events
                args[1] = ""  # Leave date empty
                args[2] = ""  # Leave place empty
                args[3] = ""  # Leave description empty
        elif "matchespagesubstringof" in rule_name_lower:
            if num_args > 0:
                args[0] = "Page"
        elif "hasdata" in rule_name_lower:
            # HasData for places needs: name, place_type, code
            if category == "place" and num_args >= 3:
                # Get a sample place name
                if handles:
                    try:
                        place = get_object_from_handle(db, category, handles[0])
                        if place:
                            all_names = place.get_all_names()
                            if all_names:
                                args[0] = all_names[0].value
                            else:
                                args[0] = "New York"
                    except:
                        args[0] = "New York"
                else:
                    args[0] = "New York"
                # Leave place_type empty (matches any type)
                args[1] = ""
                # Leave code empty (matches any code)
                args[2] = ""
        elif "hastitle" in rule_name_lower:
            # HasTitle for places needs a specific title string (not empty)
            if category == "place" and num_args > 0:
                # Find a place that has a title
                title_found = False
                for handle in handles[:20]:
                    try:
                        place = get_object_from_handle(db, category, handle)
                        if place:
                            title = place.get_title()
                            if title:
                                args[0] = title
                                title_found = True
                                break
                    except:
                        continue
                # If no title found, use a default that won't match all
                if not title_found:
                    args[0] = "NonExistentTitle"
        elif "hasgallery" in rule_name_lower or "havephotos" in rule_name_lower:
            # HasGallery/HavePhotos checks for number of media references - needs count arguments
            if num_args >= 2:
                # Count how many objects have media
                with_media = sum(1 for h in handles[:50] 
                                if get_object_from_handle(db, category, h) and 
                                get_object_from_handle(db, category, h).get_media_list())
                # Use a count that will match some but not all
                if with_media > 0:
                    # Use "1" as the number to match (at least 1 media)
                    args[0] = "1"  # Number of instances
                    args[1] = ">="  # Number must be (>=, =, <=)
                else:
                    args[0] = "0"
                    args[1] = "="
            elif num_args == 0:
                # HavePhotos can be called with 0 args (upgrades to ["0", "greater than"])
                pass  # Rule handles this in __init__
        elif "hasreferencecountof" in rule_name_lower:
            if num_args > 0:
                args[0] = "1"
        elif "hassourcecount" in rule_name_lower:
            if num_args > 0:
                args[0] = "1"
        elif "matchessourceconfidence" in rule_name_lower:
            if num_args > 0:
                args[0] = "2"
        elif "hasaddress" in rule_name_lower:
            # HasAddress needs count arguments like [0, "greater than"]
            if num_args >= 2:
                # Count how many objects have addresses
                with_addresses = sum(1 for h in handles[:50] 
                                if get_object_from_handle(db, category, h) and 
                                get_object_from_handle(db, category, h).get_address_list())
                # Use a count that will match some but not all
                if with_addresses > 0:
                    # Use "0" as the number to match (at least 0 addresses, i.e., has any address)
                    args[0] = "0"  # Number of instances
                    args[1] = "greater than"  # Number must be (>=, =, <=)
                else:
                    args[0] = "0"
                    args[1] = "="
        elif "hasassociation" in rule_name_lower:
            # HasAssociation needs count arguments like [0, "greater than"]
            if num_args >= 2:
                # Count how many objects have associations
                with_associations = sum(1 for h in handles[:50] 
                                if get_object_from_handle(db, category, h) and 
                                get_object_from_handle(db, category, h).get_person_ref_list())
                # Use a count that will match some but not all
                if with_associations > 0:
                    args[0] = "0"
                    args[1] = "greater than"
                else:
                    args[0] = "0"
                    args[1] = "="
        elif "fatherhasidof" in rule_name_lower or "motherhasidof" in rule_name_lower:
            # FatherHasIdOf/MotherHasIdOf need person IDs from families
            if category == "family" and num_args > 0:
                # Find a family with a father/mother and get their ID
                # We need to find a person that actually exists as a father/mother
                person_id = None
                for handle in handles:
                    try:
                        family = get_object_from_handle(db, category, handle)
                        if family:
                            if "father" in rule_name_lower and family.get_father_handle():
                                try:
                                    person = db.get_person_from_handle(family.get_father_handle())
                                    if person:
                                        person_id = person.gramps_id
                                        break
                                except:
                                    continue
                            elif "mother" in rule_name_lower and family.get_mother_handle():
                                try:
                                    person = db.get_person_from_handle(family.get_mother_handle())
                                    if person:
                                        person_id = person.gramps_id
                                        break
                                except:
                                    continue
                    except:
                        continue
                # If still no ID found, try to get any person ID from the database
                if not person_id:
                    try:
                        person_handles = db.get_person_handles()
                        if person_handles:
                            person = db.get_person_from_handle(person_handles[0])
                            person_id = person.gramps_id
                    except:
                        pass
                args[0] = person_id or "I0000"
        elif "hasreltype" in rule_name_lower:
            # HasRelType needs a relationship type like "Married"
            if category == "family" and num_args > 0:
                # Try to find a family with a relationship type
                rel_type = None
                for handle in handles[:50]:
                    try:
                        family = get_object_from_handle(db, category, handle)
                        if family:
                            rel = family.get_relationship()
                            if rel:
                                # Get the string representation
                                rel_type = str(rel).split('.')[-1] if hasattr(rel, '__name__') else str(rel)
                                break
                    except:
                        continue
                args[0] = rel_type or "Married"
        elif "hascitation" in rule_name_lower and category == "citation":
            # HasCitation for citations needs: page, date, confidence
            if num_args >= 3:
                # Get a sample citation to extract values
                if handles:
                    try:
                        citation = get_object_from_handle(db, category, handles[0])
                        if citation:
                            args[0] = citation.get_page() or "Page 1"  # Page
                            date_obj = citation.get_date_object()
                            if date_obj:
                                args[1] = date_obj.get_text() or ""  # Date
                            else:
                                args[1] = ""
                            args[2] = str(citation.get_confidence_level())  # Confidence
                        else:
                            args[0] = "Page 1"
                            args[1] = ""
                            args[2] = "2"
                    except:
                        args[0] = "Page 1"
                        args[1] = ""
                        args[2] = "2"
                else:
                    args[0] = "Page 1"
                    args[1] = ""
                    args[2] = "2"
        elif "hassource" in rule_name_lower and category == "citation":
            # HasSource for citations needs: Title, Author, Abbreviation, Publication
            if num_args >= 4:
                # Get a sample citation's source
                if handles:
                    try:
                        citation = get_object_from_handle(db, category, handles[0])
                        if citation and citation.get_reference_handle():
                            source = db.get_source_from_handle(citation.get_reference_handle())
                            if source:
                                args[0] = source.get_title() or ""  # Title
                                args[1] = source.get_author() or ""  # Author
                                args[2] = source.get_abbreviation() or ""  # Abbreviation
                                args[3] = source.get_publication_info() or ""  # Publication
                            else:
                                args[0] = ""
                                args[1] = ""
                                args[2] = ""
                                args[3] = ""
                        else:
                            args[0] = ""
                            args[1] = ""
                            args[2] = ""
                            args[3] = ""
                    except:
                        args[0] = ""
                        args[1] = ""
                        args[2] = ""
                        args[3] = ""
                else:
                    args[0] = ""
                    args[1] = ""
                    args[2] = ""
                    args[3] = ""
        elif "isancestorof" in rule_name_lower or "isdescendantof" in rule_name_lower:
            # IsAncestorOf/IsDescendantOf for families need: family ID, inclusive flag
            if category == "family" and num_args >= 2:
                # For IsAncestorOf, we need a family that has ancestors (not the root family)
                # For IsDescendantOf, we need a family that has descendants (not a leaf family)
                # Try to find a family in the middle of the tree
                family_id = None
                if handles and len(handles) > 1:
                    # Try to find a family that has both parents and children
                    for handle in handles[1:min(100, len(handles))]:  # Skip first, check next 100
                        try:
                            family = get_object_from_handle(db, category, handle)
                            if family:
                                # Check if it has both parents and children
                                has_parents = family.get_father_handle() or family.get_mother_handle()
                                has_children = len(family.get_child_ref_list()) > 0
                                if has_parents and has_children:
                                    family_id = family.gramps_id
                                    break
                        except:
                            continue
                # Fallback to any family ID
                if not family_id and handles:
                    try:
                        family = get_object_from_handle(db, category, handles[0])
                        if family:
                            family_id = family.gramps_id
                    except:
                        pass
                args[0] = family_id or "F0000"
                args[1] = "0"  # Inclusive flag (0 = not inclusive, 1 = inclusive)
        elif "hascommonancestorwith" in rule_name_lower:
            # HasCommonAncestorWith needs a person ID
            if category == "person" and num_args > 0:
                # Get a sample person ID - but not from the first person, use a different one
                # to ensure some but not all match
                if handles and len(handles) > 1:
                    try:
                        person = get_object_from_handle(db, category, handles[1])
                        if person:
                            args[0] = person.gramps_id
                        else:
                            args[0] = "I0000"
                    except:
                        args[0] = "I0000"
                else:
                    args[0] = "I0000"
        elif "hasevent" in rule_name_lower and category == "person":
            # HasEvent for persons needs: event_type, date, place, description, main_participants, primary_role
            # Use just event type to match some but not all (leave other fields empty)
            if num_args >= 6:
                # Find a common event type from the database
                event_type = "Birth"
                event_handles = db.get_event_handles()
                for event_handle in event_handles[:100]:
                    try:
                        event = db.get_event_from_handle(event_handle)
                        if event and event.get_type():
                            event_type_obj = event.get_type()
                            if hasattr(event_type_obj, 'xml_str'):
                                event_type = event_type_obj.xml_str()
                                break
                    except:
                        continue
                args[0] = event_type  # Event type (XML string like "Birth")
                args[1] = ""  # Date (empty = match any date)
                args[2] = ""  # Place (empty = match any place)
                args[3] = ""  # Description (empty = match any description)
                args[4] = ""  # Main Participants (empty = match any)
                args[5] = "0"  # Primary Role (0 = any role, 1 = primary only)
        elif "hasfamilyattribute" in rule_name_lower:
            # HasFamilyAttribute needs: attribute type, value
            if num_args >= 2:
                # Try to find a family attribute
                found_attr = False
                person_handles = db.get_person_handles()
                for person_handle in person_handles[:50]:
                    try:
                        person = db.get_person_from_handle(person_handle)
                        if person:
                            for family_handle in person.get_family_handle_list():
                                family = db.get_family_from_handle(family_handle)
                                if family:
                                    attrs = family.get_attribute_list()
                                    if attrs:
                                        attr = attrs[0]
                                        attr_type = attr.get_type()
                                        if isinstance(attr_type, tuple):
                                            args[0] = attr_type[1]
                                        else:
                                            args[0] = str(attr_type)
                                        args[1] = attr.get_value() or "FamilyValue_42"
                                        found_attr = True
                                        break
                        if found_attr:
                            break
                    except:
                        continue
                if not found_attr:
                    args[0] = "FamilyAttr"
                    args[1] = "FamilyValue_42"
        elif "hasnameorigintype" in rule_name_lower:
            # HasNameOriginType needs: surname origin type (e.g., "Patrilineal")
            if num_args > 0:
                # Try to find a person with a name origin type
                origin_type = None
                person_handles = db.get_person_handles()
                for person_handle in person_handles[:100]:
                    try:
                        person = db.get_person_from_handle(person_handle)
                        if person:
                            for name in [person.get_primary_name()] + person.get_alternate_names():
                                if name:
                                    for surname in name.get_surname_list():
                                        if surname.get_origintype():
                                            origin_type_obj = surname.get_origintype()
                                            # Get the XML string representation (what the rule expects)
                                            origin_type = origin_type_obj.xml_str()
                                            break
                                    if origin_type:
                                        break
                        if origin_type:
                            break
                    except:
                        continue
                args[0] = origin_type or "Patrilineal"  # Fallback to common origin type
        elif "hasnametype" in rule_name_lower:
            # HasNameType needs: name type (e.g., "Married", "Birth")
            if num_args > 0:
                # Try to find a person with a name type
                name_type = None
                person_handles = db.get_person_handles()
                for person_handle in person_handles[:100]:
                    try:
                        person = db.get_person_from_handle(person_handle)
                        if person:
                            primary_name = person.get_primary_name()
                            if primary_name and primary_name.get_type():
                                name_type_obj = primary_name.get_type()
                                # Get the XML string representation (what the rule expects)
                                name_type = name_type_obj.xml_str()
                                break
                            # Check alternate names
                            for alt_name in person.get_alternate_names():
                                if alt_name and alt_name.get_type():
                                    name_type_obj = alt_name.get_type()
                                    name_type = name_type_obj.xml_str()
                                    break
                                if name_type:
                                    break
                        if name_type:
                            break
                    except:
                        continue
                args[0] = name_type or "Birth"  # Fallback to common name type
        elif "hassoundexname" in rule_name_lower:
            # HasSoundexName needs: name string (first name or surname)
            if num_args > 0:
                # Get a sample name from a person - use first name or surname
                name_found = False
                for handle in handles[:50]:
                    try:
                        person = get_object_from_handle(db, category, handle)
                        if person:
                            name = person.get_primary_name()
                            if name:
                                first_name = name.get_first_name()
                                if first_name:
                                    args[0] = first_name  # Use first name for soundex matching
                                    name_found = True
                                    break
                                surname_list = name.get_surname_list()
                                if surname_list and surname_list[0].get_surname():
                                    args[0] = surname_list[0].get_surname()  # Use surname as fallback
                                    name_found = True
                                    break
                    except:
                        continue
                if not name_found:
                    args[0] = "John"  # Default name
        elif "hasnameof" in rule_name_lower:
            # HasNameOf needs: given name, family name, title, suffix
            if num_args >= 4:
                # Get a sample name from a person
                if handles:
                    try:
                        person = get_object_from_handle(db, category, handles[0])
                        if person:
                            name = person.get_primary_name()
                            if name:
                                args[0] = name.get_first_name() or ""  # Given name
                                surname_list = name.get_surname_list()
                                if surname_list:
                                    args[1] = surname_list[0].get_surname() or ""  # Family name
                                else:
                                    args[1] = ""
                                args[2] = ""  # Title
                                args[3] = ""  # Suffix
                            else:
                                args[0] = ""
                                args[1] = ""
                                args[2] = ""
                                args[3] = ""
                        else:
                            args[0] = ""
                            args[1] = ""
                            args[2] = ""
                            args[3] = ""
                    except:
                        args[0] = ""
                        args[1] = ""
                        args[2] = ""
                        args[3] = ""
                else:
                    args[0] = ""
                    args[1] = ""
                    args[2] = ""
                    args[3] = ""
        elif "hasrelationship" in rule_name_lower:
            # HasRelationship needs: number of relationships, relationship type, number of children
            # Find a person with a family relationship type "Married"
            if num_args >= 3:
                from gramps.gen.lib import FamilyRelType
                # Try to find a person with a "Married" relationship type
                rel_type_str = "Married"
                person_handles = db.get_person_handles()
                for person_handle in person_handles[:100]:
                    try:
                        person = db.get_person_from_handle(person_handle)
                        if person and person.get_family_handle_list():
                            for family_handle in person.get_family_handle_list():
                                family = db.get_family_from_handle(family_handle)
                                if family and family.get_relationship():
                                    rel_type = family.get_relationship()
                                    # Convert to XML string
                                    if hasattr(rel_type, 'xml_str'):
                                        rel_type_str = rel_type.xml_str()
                                        break
                                    # Fallback: try to get string representation
                                    elif hasattr(rel_type, '__name__'):
                                        rel_type_str = rel_type.__name__
                                        break
                            if rel_type_str != "Married":
                                break
                    except:
                        continue
                args[0] = ""  # Number of relationships (empty = any)
                args[1] = rel_type_str  # Relationship type (XML string like "Married")
                args[2] = ""  # Number of children (empty = any)
        elif "matchessubstringof" in rule_name_lower or "matchespagesubstringof" in rule_name_lower:
            # MatchesSubstringOf for notes needs substring
            if category == "note" and num_args > 0:
                # Get a sample note's text
                if handles:
                    try:
                        note = get_object_from_handle(db, category, handles[0])
                        if note:
                            note_text = note.get()
                            if note_text:
                                # Use first few words as substring
                                words = note_text.split()[:3]
                                args[0] = " ".join(words) if words else "test"
                            else:
                                args[0] = "test"
                        else:
                            args[0] = "test"
                    except:
                        args[0] = "test"
                else:
                    args[0] = "test"
        elif "matchesregexpof" in rule_name_lower and category == "note":
            # MatchesRegexpOf for notes needs regex pattern
            if num_args > 0:
                args[0] = ".*"  # Match any text
        elif "hassourceof" in rule_name_lower and category == "media":
            # HasSourceOf for media needs source ID
            # Since database generator ensures media have citations with sources, just use any source ID
            if num_args > 0:
                source_handles = db.get_source_handles()
                if source_handles:
                    source = db.get_source_from_handle(source_handles[0])
                    args[0] = source.gramps_id
                else:
                    args[0] = "S0000"
        elif "hascitation" in rule_name_lower and category == "media":
            # HasCitation for media needs citation details (page, date, confidence) - same as citation.HasCitation
            # Find a citation that's actually attached to a media object
            if num_args >= 3:
                citation_found = False
                media_handles = db.get_media_handles()
                # Search more media objects to find one with citations
                for media_handle in media_handles[:200]:
                    try:
                        media = db.get_media_from_handle(media_handle)
                        if media and media.get_citation_list():
                            citations = media.get_citation_list()
                            if citations:
                                citation = db.get_citation_from_handle(citations[0])
                                if citation:
                                    args[0] = citation.get_page() or ""  # Page (empty if no page)
                                    date_obj = citation.get_date_object()
                                    if date_obj:
                                        args[1] = date_obj.get_text() or ""  # Date
                                    else:
                                        args[1] = ""
                                    args[2] = str(citation.get_confidence_level())  # Confidence
                                    citation_found = True
                                    break
                    except:
                        continue
                if not citation_found:
                    # Fallback: use empty args to match any citation
                    args[0] = ""  # Page (empty = match any)
                    args[1] = ""  # Date (empty = match any)
                    args[2] = ""  # Confidence (empty = match any)
        elif "hasmedia" in rule_name_lower and category == "media":
            # HasMedia for media - this might be checking for media references
            if num_args > 0:
                # Use a sample media ID
                if handles:
                    try:
                        media = get_object_from_handle(db, category, handles[0])
                        if media:
                            args[0] = media.gramps_id
                        else:
                            args[0] = "O0000"
                    except:
                        args[0] = "O0000"
                else:
                    args[0] = "O0000"
        elif "search" in rule_name_lower and ("father" in rule_name_lower or "mother" in rule_name_lower or "child" in rule_name_lower):
            # SearchFatherName, SearchMotherName, SearchChildName need name strings
            if category == "family" and num_args > 0:
                # Get a sample name from a family member
                name_found = False
                for handle in handles[:50]:
                    try:
                        family = get_object_from_handle(db, category, handle)
                        if family:
                            person = None
                            if "father" in rule_name_lower and family.get_father_handle():
                                person = db.get_person_from_handle(family.get_father_handle())
                            elif "mother" in rule_name_lower and family.get_mother_handle():
                                person = db.get_person_from_handle(family.get_mother_handle())
                            elif "child" in rule_name_lower:
                                child_refs = family.get_child_ref_list()
                                if child_refs:
                                    person = db.get_person_from_handle(child_refs[0].ref)
                            if person:
                                name = person.get_primary_name()
                                if name:
                                    first_name = name.get_first_name()
                                    if first_name:
                                        args[0] = first_name
                                        name_found = True
                                        break
                    except:
                        continue
                if not name_found:
                    args[0] = "John"  # Default name
    
    return rule_class(args)


def _test_rule_generic(rule_name, rule_info, database):
    """Generic test implementation for a rule."""
    category = rule_info["category"]
    rule_class = rule_info["class"]
    rule_name_only = rule_info["name"]
    
    # Skip unsupported rules
    if rule_name_only in UNSUPPORTED_RULES:
        # Special case: HasAttribute for repositories (repositories don't support attributes)
        if rule_name_only == "HasAttribute" and category == "repository":
            pytest.skip(f"Rule {rule_name_only} is not supported for {category} (repositories don't support attributes)")
        else:
            pytest.skip(f"Rule {rule_name_only} is not supported (requires complex setup)")
    
    # Get all handles for this category
    handles = get_handles_for_category(database, category)
    
    if not handles:
        pytest.skip(f"No {category} items in database")
    
    total = len(handles)
    rule_name_lower = rule_class.__name__.lower()
    
    # Rules that are designed to match all items - only these specific rules should be skipped
    all_match_rules = {
        "AllEvents",      # event
        "AllSources",      # source
        "AllPlaces",       # place
        "AllRepos",        # repository
        "AllMedia",        # media
        "AllCitations",    # citation
        "AllNotes",        # note
        "AllFamilies",     # family
        "Everyone",        # person (matches all people)
    }
    
    # Only skip if it's one of the specific "All*" rules
    if rule_name_only in all_match_rules:
        if total > 0:
            pytest.skip(f"Rule {rule_name_only} is designed to match all items")
    
    # Try to create a rule instance with smart arguments
    try:
        rule = create_rule_with_args(rule_class, rule_name_only, category, database, handles)
        
        # Some rules need prepare to be called
        if hasattr(rule, "prepare"):
            try:
                rule.prepare(database, None)
            except:
                pass
        
        # Apply rule to all items and measure time
        matches = 0
        start_time = time.perf_counter()
        for handle in handles:
            try:
                obj = get_object_from_handle(database, category, handle)
                if obj and rule.apply_to_one(database, obj):
                    matches += 1
            except Exception:
                continue
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        
        # Assert that rule matches some but not all
        assert matches > 0, f"Rule {rule_name} matched 0/{total} items (needs data variety)"
        assert matches < total, f"Rule {rule_name} matched all {matches}/{total} items (needs data variety)"
        
        # Store timing data only if test passes (after assertions)
        _timing_data[rule_name] = {
            "category": category,
            "rule_name": rule_name_only,
            "time_seconds": elapsed_time,
            "items_tested": total,
            "matches": matches,
            "matches_percentage": (matches / total * 100) if total > 0 else 0
        }
        
    except Exception as e:
        pytest.fail(f"Error testing rule {rule_name}: {str(e)}")


# Generate individual test functions for each rule
_rules = get_all_rules()
for rule_name, rule_info in sorted(_rules.items()):
    # Create a test function for this specific rule
    # Use a closure to capture the rule_name and rule_info
    def make_test_func(name, info):
        def _inner_test(database):
            return _test_rule_generic(name, info, database)
        return _inner_test
    
    # Set a descriptive name (this is what pytest will see)
    test_name = f"test_{rule_name.replace('.', '_')}"
    # Use a variable name that doesn't start with 'test_' to avoid pytest collection
    func = make_test_func(rule_name, rule_info)
    func.__name__ = test_name
    func.__doc__ = f"Test that {rule_name} matches some but not all items"
    # Register the test function in the current module's globals
    globals()[test_name] = func




if __name__ == "__main__":
    # Allow running directly for debugging
    pytest.main([__file__, "-v"])
