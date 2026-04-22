import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Built-in English stopwords — no NLTK download required
STOP_WORDS = {
    "i","me","my","myself","we","our","ours","ourselves","you","your","yours",
    "yourself","yourselves","he","him","his","himself","she","her","hers",
    "herself","it","its","itself","they","them","their","theirs","themselves",
    "what","which","who","whom","this","that","these","those","am","is","are",
    "was","were","be","been","being","have","has","had","having","do","does",
    "did","doing","a","an","the","and","but","if","or","because","as","until",
    "while","of","at","by","for","with","about","against","between","into",
    "through","during","before","after","above","below","to","from","up","down",
    "in","out","on","off","over","under","again","further","then","once","here",
    "there","when","where","why","how","all","both","each","few","more","most",
    "other","some","such","no","nor","not","only","own","same","so","than",
    "too","very","s","t","can","will","just","don","should","now","d","ll","m",
    "o","re","ve","y","ain","aren","couldn","didn","doesn","hadn","hasn",
    "haven","isn","ma","mightn","mustn","needn","shan","shouldn","wasn",
    "weren","won","wouldn","also","would","could","may","might","shall",
    "across","along","around","near","within","without","per","via","etc",
    "ie","eg","vs","role","work","working","experience","years","year",
    "responsibilities","requirements","qualification","ability","strong",
    "good","excellent","great","looking","seeking","join","team","company",
    "opportunity","position","candidate","applicant","please","apply",
}


def _simple_lemmatize(word: str) -> str:
    """Minimal rule-based lemmatizer (no NLTK required)."""
    if word.endswith("ing") and len(word) > 5:
        return word[:-3]
    if word.endswith("tion") and len(word) > 6:
        return word[:-4]
    if word.endswith("ed") and len(word) > 4:
        return word[:-2]
    if word.endswith("ly") and len(word) > 4:
        return word[:-2]
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith("s") and not word.endswith("ss") and len(word) > 3:
        return word[:-1]
    return word

# ── Master skill list with Aliases ─────────────────────────────────────────────
# Key = Primary Skill Name, Value = List of synonyms/variations
TECH_SKILLS_DICT = {
    "python": ["python", "py"],
    "java": ["java"],
    "javascript": ["javascript", "js", "node.js", "nodejs"],
    "typescript": ["typescript", "ts"],
    "c++": ["c++", "cpp"],
    "c#": ["c#", "csharp", ".net"],
    "golang": ["golang", "go programming"],
    "rust": ["rust"],
    "sql": ["sql", "mysql", "postgresql", "sql server"],
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl", "neural networks"],
    "nlp": ["nlp", "natural language processing"],
    "computer vision": ["computer vision", "cv", "opencv"],
    "cuda": ["cuda"],
    "transformer": ["transformer", "bert", "gpt", "llm", "large language models"],
    "aws": ["aws", "amazon web services"],
    "gcp": ["gcp", "google cloud"],
    "azure": ["azure"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "terraform": ["terraform"],
    "ci/cd": ["ci/cd", "continuous integration", "github actions", "jenkins"],
    "fastapi": ["fastapi"],
    "flask": ["flask"],
    "django": ["django"],
    "oop": ["oop", "object oriented programming"],
    "data structures": ["data structures", "dsa", "algorithms"],
    "git": ["git", "github", "gitlab", "bitbucket"],
    "react": ["react", "reactjs"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "pytorch": ["pytorch"],
    "tensorflow": ["tensorflow"],
    "communication": ["communication", "presenting"],
    "leadership": ["leadership", "management"],
    "agile": ["agile", "scrum"],
}


def preprocess_text(text: str) -> str:
    """Lowercase, remove punctuation, lemmatize, remove stopwords."""
    text = text.lower()
    # Keep +, # for skills like C++, C#
    text = re.sub(r"[^a-z0-9\s\+#]", " ", text)
    tokens = text.split()
    tokens = [_simple_lemmatize(t) for t in tokens if t not in STOP_WORDS and len(t) > 1]
    return " ".join(tokens)


def extract_skills(text: str) -> set:
    """Extract skills from raw text using aliases and regex."""
    text_lower = text.lower()
    found = set()
    for primary_skill, aliases in TECH_SKILLS_DICT.items():
        for alias in aliases:
            # Use regex for word boundaries
            pattern = rf"\b{re.escape(alias)}\b"
            if re.search(pattern, text_lower):
                found.add(primary_skill)
                break # Move to next primary skill once one alias matches
    return found


def compute_tfidf_similarity(resume_text: str, jd_text: str) -> float:
    """Return cosine similarity score (0–100) between resume and JD."""
    resume_clean = preprocess_text(resume_text)
    jd_clean = preprocess_text(jd_text)
    vectorizer = TfidfVectorizer(ngram_range=(1, 2))
    try:
        tfidf_matrix = vectorizer.fit_transform([resume_clean, jd_clean])
        score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(float(score) * 100, 2)
    except Exception:
        return 0.0


def get_skill_analysis(resume_text: str, jd_text: str) -> dict:
    """Return matched, missing, and extra skills using requested set logic."""
    resume_skills = extract_skills(resume_text)
    jd_skills = extract_skills(jd_text)
    
    # Use explicit set logic as requested by user
    matched = set(resume_skills).intersection(set(jd_skills))
    missing = set(jd_skills) - set(resume_skills)
    extra = set(resume_skills) - set(jd_skills)
    
    # Requested formula: (matched / total_job_skills) * 100
    total_jd = len(jd_skills)
    coverage = round((len(matched) / total_jd * 100), 1) if total_jd > 0 else 0.0
    
    return {
        "resume_skills": resume_skills,
        "jd_skills": jd_skills,
        "matched": sorted(list(matched)),
        "missing": sorted(list(missing)),
        "extra": sorted(list(extra)),
        "coverage": coverage,
    }


def simulate_score_boost(current_score: float, missing_skills: list) -> float:
    """Simulate new skill score after adding missing skills with capped logic."""
    # Requested formula: min(90, current_score + len(missing_skills)*7)
    new_score = current_score + (len(missing_skills) * 7)
    return round(min(90.0, new_score), 1)
