"""
Production Rule Systems
=======================
A simple forward-chaining rule engine used to build two small
expert-system style applications:

    1. Rule-Based Medical Diagnosis System
    2. Rule-Based Chatbot (intent matching)
"""


class ProductionSystem:
    """Forward-chaining production system.

    Working memory holds facts as name -> value pairs.  Rules have
    conditions (functions that check the memory) and actions
    (functions that modify it).
    """

    def __init__(self):
        self.memory = {}
        self.rules = []
        self.trace = []

    def add_fact(self, name, value=True):
        self.memory[name] = value

    def get(self, name, default=None):
        return self.memory.get(name, default)

    def add_rule(self, name, conditions, actions):
        self.rules.append({
            "name": name,
            "conditions": conditions,
            "actions": actions,
            "fired": False,
        })

    def run(self, max_iterations=100):
        """Keep firing rules until nothing new fires."""
        self.trace = []
        for _ in range(max_iterations):
            fired_any = False
            for rule in self.rules:
                if rule["fired"]:
                    continue
                if all(cond(self.memory) for cond in rule["conditions"]):
                    self.trace.append("FIRED: " + rule["name"])
                    for action in rule["actions"]:
                        action(self.memory)
                    rule["fired"] = True
                    fired_any = True
            if not fired_any:
                break
        return self.trace


# ---------------------------------------------------------------------------
# Application 1: Rule-Based Medical Diagnosis
# ---------------------------------------------------------------------------

def build_medical_system():
    """Build a small medical diagnosis expert system."""
    ps = ProductionSystem()

    def symptom(name):
        return lambda wm: wm.get(name) is True

    def set_fact(key, value=True):
        return lambda wm: wm.__setitem__(key, value)

    # Step 1: combine symptoms into conditions
    ps.add_rule("fever_and_cough",
                [symptom("fever"), symptom("cough")],
                [set_fact("respiratory")])
    ps.add_rule("fever_and_rash",
                [symptom("fever"), symptom("rash")],
                [set_fact("viral_rash")])
    ps.add_rule("sore_throat_and_fever",
                [symptom("sore_throat"), symptom("fever")],
                [set_fact("strep")])

    # Step 2: conditions -> diagnosis
    ps.add_rule("diagnose_flu",
                [lambda wm: wm.get("respiratory") is True,
                 symptom("body_aches")],
                [set_fact("diagnosis", "Influenza (Flu)")])
    ps.add_rule("diagnose_common_cold",
                [lambda wm: wm.get("respiratory") is True,
                 lambda wm: wm.get("body_aches") is not True],
                [set_fact("diagnosis", "Common Cold")])
    ps.add_rule("diagnose_measles",
                [lambda wm: wm.get("viral_rash") is True],
                [set_fact("diagnosis", "Measles")])
    ps.add_rule("diagnose_strep_throat",
                [lambda wm: wm.get("strep") is True],
                [set_fact("diagnosis", "Strep Throat")])
    ps.add_rule("diagnose_unknown",
                [lambda wm: "diagnosis" not in wm],
                [set_fact("diagnosis",
                          "Insufficient symptoms - consult a physician")])
    return ps


def run_medical_demo():
    """Run the diagnosis demo on two patient profiles."""
    cases = [
        {"fever": True, "cough": True, "body_aches": True},
        {"fever": True, "sore_throat": True},
    ]
    for i, symptoms in enumerate(cases, 1):
        ps = build_medical_system()
        for name, value in symptoms.items():
            ps.add_fact(name, value)
        ps.run()
        print("\n=== Patient %d ===" % i)
        print("Symptoms:", symptoms)
        for step in ps.trace:
            print("   ", step)
        print("Diagnosis:", ps.get("diagnosis"))


# ---------------------------------------------------------------------------
# Application 2: Rule-Based Chatbot
# ---------------------------------------------------------------------------

def build_chatbot():
    """Build a simple intent-based chatbot."""
    ps = ProductionSystem()

    def intent_is(intent):
        return lambda wm: wm.get("intent") == intent

    def reply(text):
        return lambda wm: wm.__setitem__("response", text)

    ps.add_rule("greeting", [intent_is("greeting")],
                [reply("Hello! How can I help you today?")])
    ps.add_rule("goodbye", [intent_is("goodbye")],
                [reply("Goodbye! Feel free to return anytime.")])
    ps.add_rule("hours", [intent_is("hours")],
                [reply("We are open Monday to Friday, 9 AM to 6 PM.")])
    ps.add_rule("fees", [intent_is("fees")],
                [reply("Please visit the admissions office for fee details.")])
    ps.add_rule("fallback", [lambda wm: "response" not in wm],
                [reply("I'm sorry, I didn't understand. Could you rephrase?")])
    return ps


def classify_intent(message):
    """Naive keyword-based intent classifier."""
    text = message.lower()
    if any(w in text for w in ("hi", "hello", "hey")):
        return "greeting"
    if any(w in text for w in ("bye", "goodbye", "see you")):
        return "goodbye"
    if any(w in text for w in ("hour", "open", "time")):
        return "hours"
    if any(w in text for w in ("fee", "cost", "price", "payment")):
        return "fees"
    return "unknown"


def run_chatbot_demo():
    """Run the chatbot on a few sample messages."""
    messages = [
        "Hello there!",
        "What are your working hours?",
        "How much are the course fees?",
        "Tell me a joke",
        "Bye, thanks!",
    ]
    for msg in messages:
        ps = build_chatbot()
        ps.add_fact("intent", classify_intent(msg))
        ps.run()
        print("User :", msg)
        print("Bot  :", ps.get("response"))
        print()


def main():
    print("=" * 60)
    print("LAB 1 - PRODUCTION RULE SYSTEMS")
    print("=" * 60)

    print("\n--- Application 1: Medical Diagnosis ---")
    run_medical_demo()

    print("\n--- Application 2: Rule-Based Chatbot ---")
    run_chatbot_demo()


if __name__ == "__main__":
    main()
