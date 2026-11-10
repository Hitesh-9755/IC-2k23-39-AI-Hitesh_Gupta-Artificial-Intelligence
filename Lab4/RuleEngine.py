"""
Logical Rule Engine for Knowledge Representation
=================================================
A forward-chaining rule engine over ground predicates.

Facts look like:   symptom(fever)
Rules look like:   IF symptom(fever) AND symptom(cough)
                   THEN condition(respiratory)

The engine repeatedly applies rules whose premises are all present
in the knowledge base, adding the conclusion as a new fact, until
no more rules can fire (fixpoint).
"""

import re


# ---------------------------------------------------------------------------
# Predicate representation
# ---------------------------------------------------------------------------

class Predicate:
    """A ground predicate like name(arg1, arg2)."""

    def __init__(self, name, args=()):
        self.name = name
        self.args = tuple(args)

    def __str__(self):
        if not self.args:
            return self.name
        return "%s(%s)" % (self.name, ", ".join(self.args))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return (isinstance(other, Predicate)
                and self.name == other.name
                and self.args == other.args)

    def __hash__(self):
        return hash((self.name, self.args))


class Rule:
    """An IF-THEN production rule over predicates."""

    def __init__(self, name, premises, conclusion):
        self.name = name
        self.premises = premises
        self.conclusion = conclusion


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

_PRED_RE = re.compile(r"(\w+)\s*\(([^)]*)\)")


def parse_predicate(text):
    """Parse 'name(arg1, arg2)' into a Predicate."""
    text = text.strip()
    match = _PRED_RE.match(text)
    if not match:
        return Predicate(name=text)
    name = match.group(1)
    args_str = match.group(2).strip()
    args = tuple(a.strip().strip("'\"") for a in args_str.split(",")
                 if a.strip()) if args_str else ()
    return Predicate(name=name, args=args)


def parse_rule(text):
    """Parse 'IF p1 AND p2 THEN conclusion' into a Rule."""
    parts = re.split(r"\bTHEN\b", text, flags=re.IGNORECASE)
    if len(parts) != 2:
        raise ValueError("Rule must contain THEN keyword")
    premise_part, conclusion_part = parts
    premise_strs = re.split(r"\bAND\b", premise_part, flags=re.IGNORECASE)
    premises = [parse_predicate(p.replace("IF", "", 1))
                for p in premise_strs if p.strip()]
    conclusion = parse_predicate(conclusion_part)
    premise_label = " AND ".join(str(p) for p in premises)
    return Rule(name=premise_label,
                premises=premises, conclusion=conclusion)


# ---------------------------------------------------------------------------
# Forward-chaining engine
# ---------------------------------------------------------------------------

class RuleEngine:
    """Forward-chaining inference engine over ground predicates."""

    def __init__(self):
        self.facts = set()
        self.rules = []
        self.trace = []

    def add_fact(self, predicate):
        self.facts.add(predicate)

    def add_fact_str(self, text):
        self.add_fact(parse_predicate(text))

    def add_rule(self, rule):
        self.rules.append(rule)

    def add_rule_str(self, text):
        self.add_rule(parse_rule(text))

    def run(self, max_iterations=100):
        """Run forward chaining until fixpoint; return firing trace."""
        self.trace = []
        for _ in range(max_iterations):
            new_facts = []
            for rule in self.rules:
                if all(p in self.facts for p in rule.premises):
                    if rule.conclusion not in self.facts:
                        new_facts.append(rule.conclusion)
                        self.trace.append("FIRED: %s -> %s"
                                          % (rule.name, rule.conclusion))
            if not new_facts:
                break
            self.facts.update(new_facts)
        return self.trace

    def query(self, predicate):
        """Check if a predicate is in the knowledge base."""
        return predicate in self.facts

    def all_facts(self):
        return set(self.facts)


# ---------------------------------------------------------------------------
# Demo 1: Medical Expert System
# ---------------------------------------------------------------------------

def build_medical_engine():
    """Medical KB: symptoms -> conditions -> diagnosis."""
    engine = RuleEngine()

    facts = [
        "symptom(fever)", "symptom(cough)", "symptom(body_aches)",
        "symptom(fatigue)", "symptom(sore_throat)",
    ]
    for f in facts:
        engine.add_fact_str(f)

    rules = [
        "IF symptom(fever) AND symptom(cough) THEN condition(respiratory)",
        "IF symptom(fever) AND symptom(body_aches) THEN condition(flu_like)",
        "IF condition(respiratory) AND condition(flu_like) "
        "THEN diagnosis(influenza)",
        "IF symptom(sore_throat) AND symptom(fever) "
        "THEN diagnosis(strep_throat)",
        "IF symptom(fatigue) AND symptom(cough) THEN condition(chronic)",
    ]
    for r in rules:
        engine.add_rule_str(r)

    return engine


# ---------------------------------------------------------------------------
# Demo 2: University Knowledge Base
# ---------------------------------------------------------------------------

def build_university_engine():
    """University KB: students, courses, enrollment, eligibility."""
    engine = RuleEngine()

    facts = [
        "student(alice)", "student(bob)",
        "course(cs101)", "course(ma201)",
        "enrolled(alice, cs101)", "enrolled(bob, ma201)",
        "completed(alice, ma101)", "completed(bob, cs101)",
        "has_prereq(cs101, ma101)",
        "grade(alice, a)", "grade(bob, b)",
    ]
    for f in facts:
        engine.add_fact_str(f)

    # Ground rules (no variables) for the two students
    rules = [
        "IF enrolled(alice, cs101) AND completed(alice, ma101) "
        "AND has_prereq(cs101, ma101) THEN eligible(alice, cs101)",
        "IF enrolled(bob, ma201) AND completed(bob, cs101) "
        "THEN eligible(bob, ma201)",
        "IF enrolled(alice, cs101) AND grade(alice, a) THEN honors(alice)",
        "IF enrolled(bob, ma201) AND grade(bob, b) THEN honors(bob)",
    ]
    for r in rules:
        engine.add_rule_str(r)

    return engine


def demo():
    """Run both knowledge bases and print results."""
    print("=" * 60)
    print("MEDICAL EXPERT SYSTEM")
    print("=" * 60)
    med = build_medical_engine()
    for step in med.run():
        print(" ", step)
    print("\nDerived facts:")
    for fact in sorted(med.all_facts(), key=str):
        print("  %s" % fact)
    print("\nDiagnosis influenza?",
          med.query(parse_predicate("diagnosis(influenza)")))

    print("\n" + "=" * 60)
    print("UNIVERSITY KNOWLEDGE BASE")
    print("=" * 60)
    uni = build_university_engine()
    for step in uni.run():
        print(" ", step)
    print("\nFacts in KB:")
    for fact in sorted(uni.all_facts(), key=str):
        print("  %s" % fact)


if __name__ == "__main__":
    demo()
