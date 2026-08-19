from services.dosage import get_schedule, TIMING_ORDER, TIMING_LABELS


def generate_daily_schedule(user_supplements):
    """Generate a full daily schedule with timing labels and ordering."""
    raw_schedule = get_schedule(user_supplements)

    ordered_schedule = []
    for timing in TIMING_ORDER:
        items = raw_schedule.get(timing, [])
        ordered_schedule.append({
            "timing_key": timing,
            "timing_label": TIMING_LABELS.get(timing, timing),
            "items": items,
            "count": len(items),
        })

    return ordered_schedule


def get_timing_conflicts(user_supplements):
    """Check for timing-based conflicts (e.g., Iron + Calcium at same time)."""
    conflicts = []

    iron_calcium = {"iron", "calcium"}
    iron_zinc = {"iron", "zinc"}
    calcium_zinc = {"calcium", "zinc"}

    sup_names = set()
    for us in user_supplements:
        if us.supplement:
            sup_names.add(us.supplement.name.lower().strip())

    if iron_calcium.issubset(sup_names):
        conflicts.append({
            "substances": ["الحديد", "الكالسيوم"],
            "severity": "moderate",
            "description": "الكالسيوم يُقلل بشكل كبير من امتصاص الحديد.",
            "recommendation": "تناول الحديد في الصباح على معدة فارغة، والكالسيوم بعد ساعتين على الأقل.",
        })

    if iron_zinc.issubset(sup_names):
        conflicts.append({
            "substances": ["الحديد", "الزنك"],
            "severity": "moderate",
            "description": "الحديد والزنك يتنافسان على الامتصاص.",
            "recommendation": "افصل بينهما ساعتين على الأقل. الحديد صباحاً والزنك مساءً.",
        })

    if calcium_zinc.issubset(sup_names):
        conflicts.append({
            "substances": ["الكالسيوم", "الزنك"],
            "severity": "low",
            "description": "الكالسيوم بجرعات عالية قد يُقلل من امتصاص الزنك.",
            "recommendation": "تناول مكملات الزنك بعد ساعتين على الأقل من الكالسيوم.",
        })

    return conflicts
