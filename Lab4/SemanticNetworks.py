"""
Semantic Networks for Knowledge Representation
================================================
A semantic network is a graph where:
    - Nodes  represent concepts (objects, classes, attributes).
    - Edges  represent relationships (IS-A, HAS-A, TEACHES, etc.).

This file provides a small SemanticNetwork class with IS-A
inheritance reasoning and a pre-built University knowledge base.
"""

from collections import defaultdict, deque


class SemanticNetwork:
    """Directed labelled graph for semantic-network KR."""

    def __init__(self):
        self.links = defaultdict(list)   # node -> [(relation, target)]
        self.nodes = set()

    def add_node(self, name):
        self.nodes.add(name)

    def add_link(self, source, relation, target):
        self.add_node(source)
        self.add_node(target)
        self.links[source].append((relation, target))

    def get_links(self, node, relation=None):
        """Return all (relation, target) pairs from `node`."""
        result = self.links.get(node, [])
        if relation is not None:
            result = [(r, t) for r, t in result if r == relation]
        return result

    def is_a(self, node, ancestor):
        """Check if `node` is-a `ancestor` via transitive IS-A links."""
        visited = set()
        queue = deque([node])
        while queue:
            current = queue.popleft()
            if current == ancestor:
                return True
            if current in visited:
                continue
            visited.add(current)
            for rel, target in self.links.get(current, []):
                if rel.upper() in ("IS-A", "ISA", "SUBCLASS-OF"):
                    queue.append(target)
        return False

    def get_all_ancestors(self, node):
        """Return all transitive IS-A ancestors of `node`."""
        ancestors = set()
        queue = deque([node])
        visited = set()
        while queue:
            current = queue.popleft()
            for rel, target in self.links.get(current, []):
                if rel.upper() in ("IS-A", "ISA", "SUBCLASS-OF"):
                    if target not in visited:
                        ancestors.add(target)
                        visited.add(target)
                        queue.append(target)
        return ancestors

    def get_property(self, node, prop):
        """Retrieve a property value via a labelled link."""
        for rel, target in self.links.get(node, []):
            if rel.upper() == prop.upper():
                return target
        return None


def build_university_kb():
    """Construct a small university domain semantic network."""
    sn = SemanticNetwork()

    # Class hierarchy
    sn.add_link("Student", "IS-A", "Person")
    sn.add_link("Faculty", "IS-A", "Person")
    sn.add_link("Professor", "IS-A", "Faculty")
    sn.add_link("Lecturer", "IS-A", "Faculty")

    # Instances
    sn.add_link("Alice", "IS-A", "Student")
    sn.add_link("Bob", "IS-A", "Student")
    sn.add_link("DrSmith", "IS-A", "Professor")

    # Attributes / relations
    sn.add_link("Alice", "HAS-ID", "STU-001")
    sn.add_link("Alice", "ENROLLED-IN", "CS101")
    sn.add_link("Bob", "ENROLLED-IN", "CS101")
    sn.add_link("DrSmith", "TEACHES", "CS101")
    sn.add_link("CS101", "IS-A", "Course")
    sn.add_link("CS101", "HAS-CREDITS", "4")
    sn.add_link("CS101", "HAS-DEPARTMENT", "CSE")

    return sn


def demo():
    """Run queries against the university knowledge base."""
    sn = build_university_kb()

    print("University Knowledge Base (Semantic Network)\n")

    queries = [
        ("Alice", "Student"),
        ("Alice", "Person"),        # transitive
        ("DrSmith", "Faculty"),
        ("DrSmith", "Person"),      # transitive
        ("Bob", "Professor"),       # should be False
    ]
    for node, ancestor in queries:
        print("  is_a(%r, %r) -> %s" % (node, ancestor, sn.is_a(node, ancestor)))

    print("\nAncestors of DrSmith:", sorted(sn.get_all_ancestors("DrSmith")))
    print("CS101 credits:", sn.get_property("CS101", "HAS-CREDITS"))
    print("DrSmith teaches:",
          [t for r, t in sn.get_links("DrSmith", "TEACHES")])


if __name__ == "__main__":
    demo()
