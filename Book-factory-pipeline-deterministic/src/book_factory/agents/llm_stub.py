from __future__ import annotations
import hashlib
from multiprocessing import pool
import random

def _rng(seed: str) -> random.Random:
    h = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    return random.Random(int(h[:16], 16))

def plan_outline_stub(book_input: dict) -> dict:
    n = int(book_input["chapter_count"])
    topic = book_input["topic"].strip()
    tone = book_input["tone_profile"].strip()
    title = book_input["title"].strip()

    rng = _rng(book_input["book_id"] + "|" + title)

    # Deterministic “chapter hooks”
    hooks = [
        "a missing object that matters more than it seems",
        "a small misunderstanding that becomes a clever opportunity",
        "a promise made too quickly in public",
        "a quiet rivalry between two skilled workers",
        "an unexpected visitor with a simple request",
    ]
    settings = [
        "near the palace offices where scribes keep records",
        "by a busy riverside market along the Nile",
        "inside a temple courtyard at dusk",
        "on a small boat drifting between villages",
        "in a workshop where craftspeople trade favors",
    ]

    chapters = []
    for i in range(1, n + 1):
        chapter_id = f"ch{i}"
        hook = rng.choice(hooks)
        place = rng.choice(settings)
        ch_title = f"{topic}: Tale {i}"
        objective = f"Tell a distinct {tone} story set {place}, driven by {hook}."
        key_points = [
            f"Keep tone: {tone}.",
            f"Use vivid, accessible details about {topic}.",
            "Clear beginning, middle, and end.",
            "No bullets, no separators, plain paragraphs."
        ]
        chapters.append({"chapter_id": chapter_id, "title": ch_title, "objective": objective, "key_points": key_points})

    return {
        "book_id": book_input["book_id"],
        "title": title,
        "tone_profile": tone,
        "chapters": chapters
    }

def write_chapter_stub(book_input: dict, chapter_spec: dict, used_phrases: dict | None = None) -> dict:
    used_phrases = used_phrases or {"openers": set(), "closers": set()}
    tone = book_input["tone_profile"].strip()
    topic = book_input["topic"].strip()

    chapter_id = chapter_spec["chapter_id"]
    ch_title = chapter_spec["title"]
    objective = chapter_spec.get("objective", "").strip()

    rng = _rng(book_input["book_id"] + "|" + chapter_id + "|" + ch_title)

    tone_templates = {
        "bedtime": {
            "headings": ["A Quiet Opening", "A Gentle Turn", "A Soft Landing"],
            "openers": [
                "The night air was calm, and the world felt smaller in a good way.",
                "Everything moved slowly, as if time had decided to be kind.",
                "A quiet moment arrived without announcement."
            ],
            "closers": [
                "When the lamps were lit, the worry had already softened.",
                "Before sleep could catch up, the problem was no longer sharp.",
                "The ending felt like a deep breath."
            ],
            "verbs": ["drifted", "settled", "softened", "rested"]
        },
        "educational": {
            "headings": ["Context", "Key Idea", "Example", "Takeaway"],
            "openers": [
                "To understand what happened, it helps to start with the setting.",
                "The situation makes sense once you know the system around it.",
                "Here is the context that shapes the story."
            ],
            "closers": [
                "The takeaway is practical and easy to reuse.",
                "The story ends with a clear lesson.",
                "That is the simple rule underneath the moment."
            ],
            "verbs": ["observed", "explained", "compared", "confirmed"]
        },
        "entertaining": {
            "headings": ["The Setup", "The Twist", "The Close"],
            "openers": [
                "It started as an ordinary day, which is how trouble prefers to arrive.",
                "No one planned for a story that morning, but a story showed up anyway.",
                "The city was busy, loud, and completely unaware it was about to be funny."
            ],
            "closers": [
                "By the time everyone laughed, the problem had already been solved.",
                "It ended with relief, a small grin, and a reason to tell it again.",
                "The last detail clicked into place, and the day returned to normal."
            ],
            "verbs": ["darted", "laughed", "whispered", "bargained", "stepped"]
        },
    }
    tpl = tone_templates.get(tone, tone_templates["educational"])

    # Deterministic “chapter index”
    ch_num = int(chapter_id.replace("ch", ""))

    # Pools (deterministic selection by chapter number)
    objects = ["seal", "papyrus roll", "ink stone", "small amulet", "copper ring", "woven pouch", "ledger tablet"]
    roles = ["scribe", "boatman", "market seller", "apprentice", "guard", "priest", "courier"]
    settings = [
        "on a small boat drifting between villages",
        "by a busy riverside market",
        "inside a temple courtyard at dusk",
        "near the record rooms where scribes keep accounts",
        "in a workshop where craftspeople trade favors"
    ]
    conflicts = [
        "a message delivered to the wrong person",
        "a missing item that matters more than it seems",
        "a misunderstanding caused by a rushed promise",
        "a rumor that spreads faster than the truth",
        "a delayed delivery that threatens someone’s reputation"
    ]
    resolutions = [
        "a clever trade that saves face for everyone",
        "a quiet swap made at the right moment",
        "a small favor repaid with perfect timing",
        "a public apology that turns into laughter",
        "a simple explanation that dissolves the tension"
    ]

    obj = objects[(ch_num - 1) % len(objects)]
    role = roles[(ch_num * 2) % len(roles)]
    place = settings[(ch_num - 1) % len(settings)]
    conflict = conflicts[(ch_num - 1) % len(conflicts)]
    resolution = resolutions[(ch_num - 1) % len(resolutions)]

    names = ["Nefru", "Kheti", "Merit", "Hori", "Sabu", "Tia"]
    name = names[(ch_num - 1) % len(names)]

    # Skeleton rotation
    skeleton = (ch_num - 1) % 3  # 0,1,2

    def p(*sentences: str) -> str:
        return " ".join([s.strip() for s in sentences if s.strip()])

    def pick_unique(pool: list[str], used: set[str]) -> str:
        # deterministic-ish: shuffle a copy with rng, take first unused, else fallback
        candidates = pool[:]
        rng.shuffle(candidates)
        for c in candidates:
            if c not in used:
                used.add(c)
                return c
        # if all used, allow reuse
        c = candidates[0] if candidates else ""
        used.add(c)
        return c

    opener = pick_unique(tpl["openers"], used_phrases["openers"])
    closer = pick_unique(tpl["closers"], used_phrases["closers"])
    verb = rng.choice(tpl["verbs"])


    # Build sections with different shapes per skeleton
    sections = []
    headings = tpl["headings"]

    if skeleton == 0:
        # Character-first
        s1 = [
            p(opener),
            p(f"{name} was a {role} in {topic}, and that day they {verb} into a small problem that refused to stay small."),
            p(f"The scene unfolded {place}, where ordinary errands can turn into memorable moments."),
        ]
        s2 = [
            p(f"It began with {conflict}."),
            p(f"The {obj} became the center of attention, not because it was expensive, but because it was symbolic."),
            p(f"{name} followed a trail of small clues—glances, pauses, and one conversation that sounded innocent until it wasn’t."),
        ]
        s3 = [
            p(f"In the end, the solution was {resolution}."),
            p(closer),
        ]

    elif skeleton == 1:
        # Object-first
        s1 = [
            p(opener),
            p(f"The {obj} should have been exactly where it belonged. It wasn’t."),
            p(f"{name}, a {role}, noticed the gap first {place}."),
        ]
        s2 = [
            p(f"The trouble grew from {conflict}."),
            p("What looked like a mistake started to feel like a pattern."),
            p(f"When {name} finally understood the motive, it was almost funny how small the cause was."),
        ]
        s3 = [
            p(f"The ending came through {resolution}."),
            p(closer),
        ]

    else:
        # Environment-first
        # Make the misunderstanding grammar safer (keep your existing logic if you prefer)
        if conflict.startswith("a misunderstanding"):
            conflict_text = f"{conflict} took hold"
        else:
            conflict_text = conflict

        s1 = [
            p(opener),
            p(f"{place.capitalize()}, the smallest delay can look like disrespect, even when no one intends it."),
            p(f"{name}—a {role}—got caught in the middle when {conflict_text}."),
        ]
        s2 = [
            p(f"The {obj} became a convenient excuse for blame."),
            p("Two people insisted they were right, and both sounded convincing."),
            p(f"{name} chose a third path: ask one careful question, then wait for the answer to reveal itself."),
        ]
        s3 = [
            p(f"Everything settled with {resolution}."),
            p(closer),
        ]
        
    # Use headings according to tone (truncate/extend safely)
    if len(headings) == 3:
        section_paras = [s1, s2, s3]
    else:
        # educational has 4 headings; split content
        section_paras = [s1, [p(objective or "A key idea emerged as the situation unfolded.")], s2, s3]

    for heading, paras in zip(headings, section_paras):
        sections.append({"heading": heading, "paragraphs": paras})

    return {
        "chapter_id": chapter_id,
        "title": ch_title,
        "tone_profile": tone,
        "sections": sections,
    }

