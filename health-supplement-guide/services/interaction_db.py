from models.interaction import Interaction


def find_local_interactions(substance_list):
    """Check for known interactions among a list of substances using the local DB."""
    results = []
    substances_lower = [s.lower().strip() for s in substance_list]
    all_interactions = Interaction.query.all()

    for interaction in all_interactions:
        a_lower = interaction.substance_a.lower().strip()
        b_lower = interaction.substance_b.lower().strip()
        if a_lower in substances_lower and b_lower in substances_lower:
            results.append(interaction.to_dict())

    return results


def check_pair(substance_a, substance_b):
    """Check a single pair for interactions."""
    a_lower = substance_a.lower().strip()
    b_lower = substance_b.lower().strip()

    interaction = Interaction.query.filter(
        (
            (Interaction.substance_a.ilike(a_lower) & Interaction.substance_b.ilike(b_lower))
            | (Interaction.substance_a.ilike(b_lower) & Interaction.substance_b.ilike(a_lower))
        )
    ).first()

    return interaction.to_dict() if interaction else None
