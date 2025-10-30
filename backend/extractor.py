"""
PDF text extraction and deadline parsing module.

This module handles the extraction of text from PDF files and the parsing
of academic deadlines from syllabus text using advanced regex patterns.
"""

import re
from typing import List, Dict, Any
from dateutil import parser

# Constants for text processing
IGNORE_SECTIONS_RE = re.compile(
    r"\b(Course Description|Learning Outcomes|Late Policy|Office Hours|Resources|Academic Integrity)\b",
    re.IGNORECASE,
)

# Date and time regex patterns
MONTH_RE = r"(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)"
DAY_RE = r"\d{1,2}(?:st|nd|rd|th)?"
YEAR_RE = r"\d{4}"
DATE_RE = re.compile(rf"{MONTH_RE}\s+{DAY_RE},?\s+{YEAR_RE}", re.IGNORECASE)
TIME_RE = r"\d{1,2}:\d{2}\s?(?:AM|PM)"
RANGE_RE = re.compile(rf"{TIME_RE}\s*[\-\u2013\u2014]\s*{TIME_RE}", re.IGNORECASE)
SINGLE_TIME_RE = re.compile(TIME_RE, re.IGNORECASE)

def clean_text(raw: str) -> str:
    """
    Clean and normalize text extracted from PDF.
    
    This function:
    - Replaces various dash types with standard dashes
    - Removes emojis and special Unicode characters
    - Normalizes whitespace
    
    Args:
        raw: Raw text extracted from PDF
        
    Returns:
        str: Cleaned and normalized text
    """
    txt = raw.replace("\u2013", "-").replace("\u2014", "-")
    # Remove emojis and symbols (Unicode ranges for emojis)
    txt = re.sub(r"[\u2600-\u27BF\U0001F300-\U0001FAFF]", " ", txt)
    # Normalize whitespace
    txt = re.sub(r"\s+", " ", txt)
    return txt.strip()

def guess_event_type(title: str) -> str:
    """
    Determine the event type based on keywords in the title.
    
    Args:
        title: The event title to analyze
        
    Returns:
        str: One of the allowed event types
    """
    title_lower = title.lower()
    
    if re.search(r"\bmidterm\b", title_lower):
        return "Midterm"
    elif re.search(r"\b(final|exam|test)\b", title_lower):
        return "Exam"
    elif re.search(r"\bquiz\b", title_lower):
        return "Quiz"
    elif re.search(r"\blab\b", title_lower):
        return "Lab"
    elif re.search(r"\bassignment\b|\bhw\b|\bhomework\b", title_lower):
        return "Assignment"
    elif re.search(r"\bproject|presentation|report\b", title_lower):
        return "Project"
    else:
        return "Other"

def extract_deadlines_from_text(text: str) -> List[Dict[str, Any]]:
    """
    Extract academic events from syllabus text using advanced pattern matching.
    
    This function implements a sophisticated algorithm that:
    1. Cleans the input text
    2. Finds date patterns with year requirements
    3. Extracts titles from text preceding dates
    4. Detects time ranges for timed events
    5. Categorizes events by type
    6. Deduplicates events
    
    Args:
        text: Raw text extracted from PDF syllabus
        
    Returns:
        List[Dict]: List of extracted events with title, type, start, end, allDay, extracted_from
    """
    # Clean the input text
    cleaned = clean_text(text)
    # Remove non-academic sections
    cleaned = IGNORE_SECTIONS_RE.sub(" ", cleaned)

    results = []
    seen = set()  # Track seen events to prevent duplicates

    # Find all date patterns in the text
    for date_match in DATE_RE.finditer(cleaned):
        date_text = date_match.group(0)
        
        try:
            # Parse the date to ensure it's valid
            date_base = parser.parse(date_text)
        except Exception:
            # Skip dates that can't be parsed
            continue

        # Create a context window around the date for title extraction
        start_idx = max(0, date_match.start() - 120)
        end_idx = min(len(cleaned), date_match.end() + 120)
        snippet = cleaned[start_idx:end_idx].strip()

        # Extract title from text before the date
        before_text = cleaned[start_idx:date_match.start()].strip()
        
        # Split on common delimiters and take the last segment
        segments = re.split(r"[.;|]\s*|\(\s*\d+%\s*\)", before_text)
        title_raw = (segments[-1] if segments else before_text).strip()
        
        # Clean up the title
        title_raw = re.sub(r"\b\d+%\b", "", title_raw).strip()  # Remove percentage weights
        title_raw = re.sub(
            r"\b(Component|Weight|Date\s*/?\s*Deadline|Important Dates)\b", 
            "", 
            title_raw, 
            flags=re.IGNORECASE
        ).strip()
        
        # Default title if none found
        if not title_raw:
            title_raw = "Assignment"

        # Check for time information after the date
        after_text = cleaned[date_match.end():end_idx]
        time_range_match = RANGE_RE.search(after_text)
        single_time_match = SINGLE_TIME_RE.search(after_text) if not time_range_match else None

        # Determine start/end times and all-day status
        if time_range_match:
            # Time range found (e.g., "7:00 PM – 9:00 PM")
            range_text = time_range_match.group(0)
            time_parts = re.split(r"[\-\u2013\u2014]", range_text)
            start_time = parser.parse(f"{date_text} {time_parts[0].strip()}")
            end_time = parser.parse(f"{date_text} {time_parts[1].strip()}")
            start_iso = start_time.isoformat()
            end_iso = end_time.isoformat()
            all_day = False
        elif single_time_match:
            # Single time found (e.g., "7:00 PM")
            start_time = parser.parse(f"{date_text} {single_time_match.group(0)}")
            start_iso = start_time.isoformat()
            end_iso = start_time.isoformat()
            all_day = False
        else:
            # No time specified - all day event
            date_only = date_base.replace(hour=0, minute=0, second=0, microsecond=0)
            start_iso = end_iso = date_only.isoformat()
            all_day = True

        # Handle multiple events on the same line (comma/semicolon separated)
        event_titles = [
            t.strip(" -:") 
            for t in re.split(r",|;", title_raw) 
            if len(t.strip()) > 2
        ]
        
        if not event_titles:
            event_titles = [title_raw]

        # Create an event for each title
        for title in event_titles:
            title = re.sub(r"\s+", " ", title)  # Normalize whitespace
            event_type = guess_event_type(title)
            
            # Create unique key for duplicate detection
            event_key = f"{title.lower()}_{start_iso[:10]}"
            
            if event_key in seen:
                continue
                
            results.append({
                'title': title,
                'type': event_type,
                'start': start_iso,
                'end': end_iso,
                'allDay': all_day,
                'extracted_from': snippet
            })
            seen.add(event_key)

    return results
