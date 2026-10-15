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
            changes = {
                k: v
                for k, v in {
                    "title": args.title,
                    "priority": args.priority,
                    "status": args.status,
                }.items()
                if v is not None
            }
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
            pairs = [[int(x) for x in item.split(":")] for item in args.intervals]
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



"""OpenTrack command-line interface.

Usage examples:
    python -m src.main create --title "Fix login" --priority high
    python -m src.main get 1
    python -m src.main list
    python -m src.main update 1 --status closed
    python -m src.main delete 1
    python -m src.main find --status open
    python -m src.main triage --limit 5
    python -m src.main ref 1
    python -m src.main windows 1:3 2:5
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


def positive_integer(value):
    """Parse a positive integer for command-line arguments."""
    try:
        number = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "must be an integer"
        ) from exc

    if number <= 0:
        raise argparse.ArgumentTypeError(
            "must be greater than zero"
        )

    return number


def parse_interval(value):
    """Parse an inclusive interval in start:end format."""
    parts = value.split(":")

    if len(parts) != 2:
        raise argparse.ArgumentTypeError(
            f"invalid interval {value!r}; expected start:end"
        )

    try:
        start, end = map(int, parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            f"invalid interval {value!r}; endpoints must be integers"
        ) from exc

    if start > end:
        raise argparse.ArgumentTypeError(
            f"invalid interval {value!r}; start cannot exceed end"
        )

    return [start, end]


def build_parser():
    parser = argparse.ArgumentParser(
        prog="opentrack",
        description="OpenTrack issue tracker",
    )

    parser.add_argument(
        "--db",
        default=DEFAULT_DB,
        help="path to the JSON storage file",
    )

    sub = parser.add_subparsers(
        dest="command",
        required=True,
    )

    p_create = sub.add_parser("create", help="create a new issue")
    p_create.add_argument("--title", required=True)
    p_create.add_argument("--priority", default="medium")
    p_create.add_argument("--status", default="open")

    p_get = sub.add_parser("get", help="show one issue")
    p_get.add_argument("id", type=positive_integer)

    sub.add_parser("list", help="list all issues")

    p_update = sub.add_parser(
        "update",
        help="partially update an issue",
    )
    p_update.add_argument("id", type=positive_integer)
    p_update.add_argument("--title")
    p_update.add_argument("--priority")
    p_update.add_argument("--status")

    p_delete = sub.add_parser("delete", help="delete an issue")
    p_delete.add_argument("id", type=positive_integer)

    p_find = sub.add_parser(
        "find",
        help="filter and search issues",
    )
    p_find.add_argument("--status")
    p_find.add_argument("--priority")
    p_find.add_argument("--title-contains")

    p_triage = sub.add_parser(
        "triage",
        help="rank open issues for triage",
    )
    p_triage.add_argument(
        "--limit",
        type=positive_integer,
        default=5,
    )

    p_ref = sub.add_parser(
        "ref",
        help="show an issue's reference hint",
    )
    p_ref.add_argument("id", type=positive_integer)

    p_windows = sub.add_parser(
        "windows",
        help="consolidate maintenance windows",
    )
    p_windows.add_argument(
        "intervals",
        nargs="+",
        type=parse_interval,
        metavar="START:END",
        help="inclusive intervals, e.g. 1:3 2:5",
    )

    return parser


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        service = IssueService(JsonStorage(args.db))

        if args.command == "create":
            result = service.create({
                "title": args.title,
                "priority": args.priority,
                "status": args.status,
            })

        elif args.command == "get":
            result = service.get(args.id)

        elif args.command == "list":
            result = service.list_all()

        elif args.command == "update":
            changes = {
                key: value
                for key, value in {
                    "title": args.title,
                    "priority": args.priority,
                    "status": args.status,
                }.items()
                if value is not None
            }

            if not changes:
                parser.error(
                    "update requires at least one of "
                    "--title, --priority, or --status"
                )

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
            result = rank_open_issues(
                service.list_all(),
                args.limit,
            )

        elif args.command == "ref":
            issue = service.get(args.id)
            title = issue["title"]
            index = first_unique_index(title)

            result = {
                "id": issue["id"],
                "title": title,
                "ref_index": index,
                "ref_char": title[index] if index >= 0 else None,
            }

        elif args.command == "windows":
            result = merge_intervals(args.intervals)

        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    except ValidationError as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 2

    except IssueNotFound as exc:
        print(f"not found: {exc.args[0]}", file=sys.stderr)
        return 3

    except (OSError, json.JSONDecodeError) as exc:
        print(f"storage error: {exc}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    sys.exit(main())
