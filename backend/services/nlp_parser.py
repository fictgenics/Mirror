import re
import spacy
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import nltk
from textblob import TextBlob

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

@dataclass
class ParsedQuery:
    """Structured representation of a parsed natural language query"""
    base_query: str
    min_stars: Optional[int] = None
    max_stars: Optional[int] = None
    min_forks: Optional[int] = None
    max_forks: Optional[int] = None
    min_contributors: Optional[int] = None
    max_contributors: Optional[int] = None
    language: Optional[str] = None
    created_after: Optional[str] = None
    created_before: Optional[str] = None
    updated_after: Optional[str] = None
    topics: List[str] = None
    has_issues: Optional[bool] = None
    has_wiki: Optional[bool] = None
    is_archived: Optional[bool] = None
    is_fork: Optional[bool] = None
    search_in: List[str] = None  # name, description, readme, topics
    
    def __post_init__(self):
        if self.topics is None:
            self.topics = []
        if self.search_in is None:
            self.search_in = ['name', 'description', 'readme', 'topics']

class NLPQueryParser:
    """Parse natural language queries into structured GitHub search parameters"""
    
    def __init__(self):
        # Load spaCy model (use smaller model for faster processing)
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # If model not available, use basic text processing
            self.nlp = None
            print("Warning: spaCy model not available. Using basic text processing.")
        
        # Common patterns for GitHub search
        self.star_patterns = [
            r'more than (\d+)\s*stars?',
            r'(\d+)\s*\+?\s*stars?',
            r'at least (\d+)\s*stars?',
            r'minimum (\d+)\s*stars?',
            r'(\d+)\s*stars? or more'
        ]
        
        self.fork_patterns = [
            r'more than (\d+)\s*forks?',
            r'(\d+)\s*\+?\s*forks?',
            r'at least (\d+)\s*forks?',
            r'minimum (\d+)\s*forks?',
            r'(\d+)\s*forks? or more'
        ]
        
        self.contributor_patterns = [
            r'more than (\d+)\s*contributors?',
            r'(\d+)\s*\+?\s*contributors?',
            r'at least (\d+)\s*contributors?',
            r'minimum (\d+)\s*contributors?',
            r'(\d+)\s*contributors? or more'
        ]
        
        self.language_patterns = [
            r'in (\w+)',
            r'(\w+) projects?',
            r'(\w+) repositories?',
            r'(\w+) code',
            r'(\w+) language'
        ]
        
        self.date_patterns = [
            r'created (?:in|after|since) (\d{4})',
            r'created (?:in|after|since) (\w+ \d{4})',
            r'updated (?:in|after|since) (\d{4})',
            r'updated (?:in|after|since) (\w+ \d{4})',
            r'from (\d{4})',
            r'since (\d{4})'
        ]
        
        self.topic_patterns = [
            r'with (\w+(?:-\w+)*)',
            r'using (\w+(?:-\w+)*)',
            r'(\w+(?:-\w+)*) integration',
            r'(\w+(?:-\w+)*) support',
            r'(\w+(?:-\w+)*) plugin'
        ]
        
        self.boolean_patterns = [
            (r'with issues?', 'has_issues', True),
            (r'without issues?', 'has_issues', False),
            (r'with wiki', 'has_wiki', True),
            (r'without wiki', 'has_wiki', False),
            (r'archived', 'is_archived', True),
            (r'not archived', 'is_archived', False),
            (r'forked', 'is_fork', True),
            (r'not forked', 'is_fork', False),
            (r'original', 'is_fork', False)
        ]

    def parse_query(self, query: str) -> ParsedQuery:
        """Parse natural language query into structured parameters"""
        query = query.lower().strip()
        
        # Initialize parsed query
        parsed = ParsedQuery(base_query=query)
        
        # Extract base query (remove all the structured parts)
        base_query = self._extract_base_query(query)
        parsed.base_query = base_query
        
        # Extract numeric constraints
        parsed.min_stars = self._extract_min_stars(query)
        parsed.min_forks = self._extract_min_forks(query)
        parsed.min_contributors = self._extract_min_contributors(query)
        
        # Extract language
        parsed.language = self._extract_language(query)
        
        # Extract dates
        parsed.created_after = self._extract_created_date(query)
        parsed.updated_after = self._extract_updated_date(query)
        
        # Extract topics
        parsed.topics = self._extract_topics(query)
        
        # Extract boolean flags
        for pattern, field, value in self.boolean_patterns:
            if re.search(pattern, query):
                setattr(parsed, field, value)
        
        # Extract search scope
        parsed.search_in = self._extract_search_scope(query)
        
        return parsed
    
    def _extract_base_query(self, query: str) -> str:
        """Extract the main search query by removing structured parts"""
        # Remove all the pattern matches to get the base query
        query = re.sub(r'more than \d+\s*stars?', '', query)
        query = re.sub(r'\d+\s*\+?\s*stars?', '', query)
        query = re.sub(r'at least \d+\s*stars?', '', query)
        query = re.sub(r'minimum \d+\s*stars?', '', query)
        query = re.sub(r'\d+\s*stars? or more', '', query)
        
        query = re.sub(r'more than \d+\s*forks?', '', query)
        query = re.sub(r'\d+\s*\+?\s*forks?', '', query)
        query = re.sub(r'at least \d+\s*forks?', '', query)
        query = re.sub(r'minimum \d+\s*forks?', '', query)
        query = re.sub(r'\d+\s*forks? or more', '', query)
        
        query = re.sub(r'more than \d+\s*contributors?', '', query)
        query = re.sub(r'\d+\s*\+?\s*contributors?', '', query)
        query = re.sub(r'at least \d+\s*contributors?', '', query)
        query = re.sub(r'minimum \d+\s*contributors?', '', query)
        query = re.sub(r'\d+\s*contributors? or more', '', query)
        
        query = re.sub(r'in \w+', '', query)
        query = re.sub(r'\w+ projects?', '', query)
        query = re.sub(r'\w+ repositories?', '', query)
        query = re.sub(r'\w+ code', '', query)
        query = re.sub(r'\w+ language', '', query)
        
        query = re.sub(r'created (?:in|after|since) \d{4}', '', query)
        query = re.sub(r'created (?:in|after|since) \w+ \d{4}', '', query)
        query = re.sub(r'updated (?:in|after|since) \d{4}', '', query)
        query = re.sub(r'updated (?:in|after|since) \w+ \d{4}', '', query)
        query = re.sub(r'from \d{4}', '', query)
        query = re.sub(r'since \d{4}', '', query)
        
        query = re.sub(r'with \w+(?:-\w+)*', '', query)
        query = re.sub(r'using \w+(?:-\w+)*', '', query)
        query = re.sub(r'\w+(?:-\w+)* integration', '', query)
        query = re.sub(r'\w+(?:-\w+)* support', '', query)
        query = re.sub(r'\w+(?:-\w+)* plugin', '', query)
        
        query = re.sub(r'with issues?', '', query)
        query = re.sub(r'without issues?', '', query)
        query = re.sub(r'with wiki', '', query)
        query = re.sub(r'without wiki', '', query)
        query = re.sub(r'archived', '', query)
        query = re.sub(r'not archived', '', query)
        query = re.sub(r'forked', '', query)
        query = re.sub(r'not forked', '', query)
        query = re.sub(r'original', '', query)
        
        # Clean up extra whitespace and common words
        query = re.sub(r'\s+', ' ', query).strip()
        query = re.sub(r'^(repos?|repositories?|projects?|code)\s+', '', query)
        query = re.sub(r'\s+(repos?|repositories?|projects?|code)$', '', query)
        
        return query.strip()
    
    def _extract_min_stars(self, query: str) -> Optional[int]:
        """Extract minimum stars requirement"""
        for pattern in self.star_patterns:
            match = re.search(pattern, query)
            if match:
                return int(match.group(1))
        return None
    
    def _extract_min_forks(self, query: str) -> Optional[int]:
        """Extract minimum forks requirement"""
        for pattern in self.fork_patterns:
            match = re.search(pattern, query)
            if match:
                return int(match.group(1))
        return None
    
    def _extract_min_contributors(self, query: str) -> Optional[int]:
        """Extract minimum contributors requirement"""
        for pattern in self.contributor_patterns:
            match = re.search(pattern, query)
            if match:
                return int(match.group(1))
        return None
    
    def _extract_language(self, query: str) -> Optional[str]:
        """Extract programming language"""
        for pattern in self.language_patterns:
            match = re.search(pattern, query)
            if match:
                lang = match.group(1).lower()
                # Map common language variations
                lang_map = {
                    'js': 'javascript',
                    'ts': 'typescript',
                    'py': 'python',
                    'rb': 'ruby',
                    'php': 'php',
                    'java': 'java',
                    'cpp': 'c++',
                    'csharp': 'c#',
                    'go': 'go',
                    'rust': 'rust',
                    'swift': 'swift',
                    'kotlin': 'kotlin',
                    'scala': 'scala'
                }
                return lang_map.get(lang, lang)
        return None
    
    def _extract_created_date(self, query: str) -> Optional[str]:
        """Extract creation date constraint"""
        for pattern in self.date_patterns:
            match = re.search(pattern, query)
            if match:
                date_str = match.group(1)
                # Convert to GitHub date format
                if re.match(r'\d{4}', date_str):
                    return f"{date_str}-01-01"
                # Handle month-year format
                elif re.match(r'\w+ \d{4}', date_str):
                    # Simple month parsing
                    month_map = {
                        'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04',
                        'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
                        'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
                    }
                    parts = date_str.split()
                    if len(parts) == 2:
                        month, year = parts
                        month_num = month_map.get(month[:3].lower(), '01')
                        return f"{year}-{month_num}-01"
        return None
    
    def _extract_updated_date(self, query: str) -> Optional[str]:
        """Extract update date constraint"""
        # Similar to created date but for updates
        return self._extract_created_date(query.replace('created', 'updated'))
    
    def _extract_topics(self, query: str) -> List[str]:
        """Extract topics/technologies mentioned"""
        topics = []
        for pattern in self.topic_patterns:
            matches = re.findall(pattern, query)
            for match in matches:
                if match not in topics:
                    topics.append(match)
        return topics
    
    def _extract_search_scope(self, query: str) -> List[str]:
        """Extract where to search (name, description, readme, topics)"""
        scope = ['name', 'description', 'readme', 'topics']
        
        if 'name only' in query or 'title only' in query:
            return ['name']
        elif 'description only' in query:
            return ['description']
        elif 'readme only' in query:
            return ['readme']
        elif 'topics only' in query:
            return ['topics']
        
        return scope
    
    def build_github_query(self, parsed: ParsedQuery) -> str:
        """Build GitHub search query from parsed parameters"""
        query_parts = []
        
        # Add base query
        if parsed.base_query:
            query_parts.append(parsed.base_query)
        
        # Add language filter
        if parsed.language:
            query_parts.append(f"language:{parsed.language}")
        
        # Add star filters
        if parsed.min_stars:
            query_parts.append(f"stars:>={parsed.min_stars}")
        if parsed.max_stars:
            query_parts.append(f"stars:<={parsed.max_stars}")
        
        # Add fork filters
        if parsed.min_forks:
            query_parts.append(f"forks:>={parsed.min_forks}")
        if parsed.max_forks:
            query_parts.append(f"forks:<={parsed.max_forks}")
        
        # Add contributor filters
        if parsed.min_contributors:
            query_parts.append(f"contributors:>={parsed.min_contributors}")
        if parsed.max_contributors:
            query_parts.append(f"contributors:<={parsed.max_contributors}")
        
        # Add date filters
        if parsed.created_after:
            query_parts.append(f"created:>={parsed.created_after}")
        if parsed.updated_after:
            query_parts.append(f"pushed:>={parsed.updated_after}")
        
        # Add boolean filters
        if parsed.has_issues is not None:
            query_parts.append(f"has:issues" if parsed.has_issues else "no:issues")
        if parsed.has_wiki is not None:
            query_parts.append(f"has:wiki" if parsed.has_wiki else "no:wiki")
        if parsed.is_archived is not None:
            query_parts.append(f"archived:{'true' if parsed.is_archived else 'false'}")
        if parsed.is_fork is not None:
            query_parts.append(f"fork:{'true' if parsed.is_fork else 'false'}")
        
        # Add topic filters
        for topic in parsed.topics:
            query_parts.append(f"topic:{topic}")
        
        return " ".join(query_parts)
    
    def get_query_explanation(self, parsed: ParsedQuery) -> Dict[str, any]:
        """Get human-readable explanation of the parsed query"""
        explanation = {
            "original_query": parsed.base_query,
            "parsed_filters": {},
            "github_query": self.build_github_query(parsed),
            "search_scope": parsed.search_in
        }
        
        if parsed.min_stars:
            explanation["parsed_filters"]["min_stars"] = parsed.min_stars
        if parsed.min_forks:
            explanation["parsed_filters"]["min_forks"] = parsed.min_forks
        if parsed.min_contributors:
            explanation["parsed_filters"]["min_contributors"] = parsed.min_contributors
        if parsed.language:
            explanation["parsed_filters"]["language"] = parsed.language
        if parsed.created_after:
            explanation["parsed_filters"]["created_after"] = parsed.created_after
        if parsed.updated_after:
            explanation["parsed_filters"]["updated_after"] = parsed.updated_after
        if parsed.topics:
            explanation["parsed_filters"]["topics"] = parsed.topics
        if parsed.has_issues is not None:
            explanation["parsed_filters"]["has_issues"] = parsed.has_issues
        if parsed.has_wiki is not None:
            explanation["parsed_filters"]["has_wiki"] = parsed.has_wiki
        if parsed.is_archived is not None:
            explanation["parsed_filters"]["is_archived"] = parsed.is_archived
        if parsed.is_fork is not None:
            explanation["parsed_filters"]["is_fork"] = parsed.is_fork
        
        return explanation
