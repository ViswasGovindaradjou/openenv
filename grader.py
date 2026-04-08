def grade(tickets, ground_truth, task_id: str) -> float:
    total = len(tickets)
    score = 0.0

    for t in tickets:
        gt = ground_truth[t.id]

        if task_id == "easy":
            if t.category == gt:
                score += 1.0

        elif task_id == "medium":
            if t.category == gt:
                score += 0.5
                if t.responded:
                    score += 0.5
            else:
                # penalize confident wrong handling
                if t.responded:
                    score -= 0.2

        elif task_id == "hard":
            # classification
            if t.category == gt:
                score += 0.3

            # response correctness
            if t.responded:
                if t.category == gt:
                    score += 0.3
                else:
                    score -= 0.2

            # escalation correctness
            if t.sentiment == "angry":
                if t.escalated:
                    score += 0.4
                else:
                    score -= 0.2

            # SLA adherence
            if t.steps_taken <= t.sla_deadline:
                score += 0.2
            else:
                score -= 0.2

    # normalize and clamp
    score = score / max(total, 1)
    return max(0.0, min(round(score, 3), 1.0))