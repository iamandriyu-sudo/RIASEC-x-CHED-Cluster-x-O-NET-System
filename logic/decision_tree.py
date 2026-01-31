def ched_decision_tree(dominant, secondary):
    if dominant == 'R':
        return ["Engineering and Technology",
                "Maritime Education",
                "Architecture and Related Programs"]

    if dominant == 'I':
        if secondary == 'C':
            return ["Science and Mathematics"]
        elif secondary == 'A':
            return ["Information Technology Education"]
        else:
            return ["Multi and Interdisciplinary Cluster"]

    if dominant == 'A':
        if secondary == 'R':
            return ["Architecture and Related Programs"]
        elif secondary == 'S':
            return ["Teacher Education"]
        else:
            return ["Information Technology Education"]

    if dominant == 'S':
        return ["Health Profession Education",
                "Teacher Education",
                "Social Sciences"]

    if dominant == 'E':
        return ["Business and Management",
                "Multi and Interdisciplinary Cluster"]

    if dominant == 'C':
        return ["Business and Management",
                "Information Technology Education",
                "Science and Mathematics"]
