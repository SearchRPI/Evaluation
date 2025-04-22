import argparse
import os

FLAGGED_FILE = "flagged_terms.txt"


def load_terms():
    if not os.path.exists(FLAGGED_FILE):
        return []
    with open(FLAGGED_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def save_terms(terms):
    with open(FLAGGED_FILE, "w", encoding="utf-8") as f:
        for term in sorted(set(terms)):
            f.write(term + "\n")


def list_terms():
    terms = load_terms()
    if not terms:
        print("\nNo flagged terms yet.")
    else:
        print("\nFlagged Terms:")
        for i, term in enumerate(terms, 1):
            print(f"{i}. {term}")


def add_term(term):
    terms = load_terms()
    if term in terms:
        print(f"\n'{term}' is already flagged.")
    else:
        terms.append(term)
        save_terms(terms)
        print(f"\nAdded '{term}' to flagged terms.")


def remove_term(term):
    terms = load_terms()
    if term not in terms:
        print(f"\n'{term}' is not in the list.")
    else:
        terms.remove(term)
        save_terms(terms)
        print(f"\nRemoved '{term}' from flagged terms.")


def main():
    parser = argparse.ArgumentParser(description="Manage your flagged search terms")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--list", action="store_true", help="List all flagged terms")
    group.add_argument("--add", metavar="TERM", help="Add a new flagged term")
    group.add_argument("--remove", metavar="TERM", help="Remove a flagged term")

    args = parser.parse_args()

    if args.list:
        list_terms()
    elif args.add:
        add_term(args.add)
    elif args.remove:
        remove_term(args.remove)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
