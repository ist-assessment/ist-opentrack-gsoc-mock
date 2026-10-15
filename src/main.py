"""OpenTrack command-line interface.

Usage examples:
    python -m src.main create --title "Fix login" --priority high
    python -m src.main get 1
    python -m src.main list
    python -m src.main update 1 --status closed
    python -m src.main delete 1
"""

import argparse
import json
import sys

from .algorithms import first_unique_index, merge_intervals
from .issue_service import IssueNotFound, IssueService
from .ranking import rank_open_issues
from .storage import JsonStorage
from .validators import ValidationError

DEFAULT_DB = "opentrack.json"


def build_parser():
    parser = argparse.ArgumentParser(prog="opentrack", description="OpenTrack issue tracker")
    parser.add_argument("--db", default=DEFAULT_DB, help="path to the JSON storage file")
    sub = parser.add_subparsers(dest="command", required=True)

    p_create = sub.add_parser("create", help="create a new issue")
    p_create.add_argument("--title", required=True)
    p_create.add_argument("--priority", default="medium")
    p_create.add_argument("--status", default="open")

    p_get = sub.add_parser("get", help="show one issue")
    p_get.add_argument("id", type=int)

    sub.add_parser("list", help="list all issues")

    p_update = sub.add_parser("update", help="partially update an issue")
    p_update.add_argument("id", type=int)
    p_update.add_argument("--title")
    p_update.add_argument("--priority")
    p_update.add_argument("--status")

    p_delete = sub.add_parser("delete", help="delete an issue")
    p_delete.add_argument("id", type=int)

    p_find = sub.add_parser("find", help="filter and search issues")
    p_find.add_argument("--status")
    p_find.add_argument("--priority")
    p_find.add_argument("--title-contains")

    p_triage = sub.add_parser("triage", help="rank open issues for triage")
    p_triage.add_argument("--limit", type=int, default=5)

    p_ref = sub.add_parser("ref", help="show an issue's reference hint (first unique title character)")
    p_ref.add_argument("id", type=int)

    p_windows = sub.add_parser("windows", help="consolidate maintenance windows")
    p_windows.add_argument(
        "intervals",
        nargs="+",
        help="inclusive intervals as start:end pairs, e.g. 1:3 2:5",
    )

    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    service = IssueService(JsonStorage(args.db))
    try:
        if args.command == "create":
            result = service.create(
                {"title": args.title, "priority": args.priority, "status": args.status}
            )
        elif args.command == "get":
            result = service.get(args.id)
        elif args.command == "list":
            result = service.list_all()
        elif args.command == "update":
            # Simplify the changes dictionary filter using regular if statements
            changes = {}
            if args.title is not None:
                changes["title"] = args.title
            if args.priority is not None:
                changes["priority"] = args.priority
            if args.status is not None:
                changes["status"] = args.status

            result = service.update(args.id, changes)
        elif args.command == "delete":
            service.delete(args.id)
            result = {"deleted": args.id}
        elif args.command == "find":
            result = service.find(
                status=args.status,
                priority=args.priority,
                title_contains=args.title_contains,
            )
        elif args.command == "triage":
            result = rank_open_issues(service.list_all(), args.limit)
        elif args.command == "ref":
            issue = service.get(args.id)
            index = first_unique_index(issue["title"])
            result = {
                "id": issue["id"],
                "title": issue["title"],
                "ref_index": index,
                "ref_char": issue["title"][index] if index >= 0 else None,
            }
        elif args.command == "windows":
            # Formulating the list using a standard nested list loop approach
            pairs = []
            for item in args.intervals:
                parts = item.split(":")
                int_pair = [int(parts[0]), int(parts[1])]
                pairs.append(int_pair)

            result = merge_intervals(pairs)

        print(json.dumps(result, indent=2))
        return 0
    except ValidationError as e:
        print(f"invalid input: {e}", file=sys.stderr)
        return 2
    except IssueNotFound as e:
        print(f"not found: {e.args[0]}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    sys.exit(main())
