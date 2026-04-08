from env import SupportEnv
from models import Action
from grader import grade

def run_baseline():
    env = SupportEnv(seed=42, max_steps=15)
    obs = env.reset()
    done = False

    # simple rule-based agent (deterministic)
    while not done:
        for t in obs.tickets:
            text = t.text.lower()

            if "payment" in text:
                cat = "billing"
            elif "crash" in text:
                cat = "technical"
            else:
                cat = "refund"

            obs, _, done, _ = env.step(Action(type="classify", ticket_id=t.id, value=cat))
            if done: break

            obs, _, done, _ = env.step(Action(type="respond", ticket_id=t.id))
            if done: break

            if t.sentiment == "angry":
                obs, _, done, _ = env.step(Action(type="escalate", ticket_id=t.id))
            if done: break

    return {
        "easy": grade(env.tickets, env.gt, "easy"),
        "medium": grade(env.tickets, env.gt, "medium"),
        "hard": grade(env.tickets, env.gt, "hard"),
    }

if __name__ == "__main__":
    print(run_baseline())