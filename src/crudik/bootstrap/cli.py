import argparse
import contextlib

import alembic.config

from crudik.adapters.db.alembic.config import get_alembic_config_path
from crudik.bootstrap.entrypoint.fast_api import run_api


def run_migrations() -> None:
    """Run database migrations to head."""
    alembic_path_gen = get_alembic_config_path()
    alembic_path = str(next(alembic_path_gen))
    alembic.config.main(
        argv=["-c", alembic_path, "upgrade", "head"],
    )

    with contextlib.suppress(StopIteration):
        next(alembic_path_gen)


def autogenerate_migrations(message: str) -> None:
    """Autogenerate migration with given message."""
    alembic_path_gen = get_alembic_config_path()
    alembic_path = str(next(alembic_path_gen))
    alembic.config.main(
        argv=["-c", alembic_path, "revision", "--autogenerate", "-m", message],
    )

    with contextlib.suppress(StopIteration):
        next(alembic_path_gen)


def create_parser() -> argparse.ArgumentParser:
    """Create CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="crudik",
        description="CRUDIK CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s run api          # Run FastAPI server
  %(prog)s migrations autogenerate "Add user table"  # Create migration
  %(prog)s migrations apply  # Apply migrations
        """,
    )

    subparsers = parser.add_subparsers(title="commands", dest="command", help="available commands", required=True)

    # run command
    run_parser = subparsers.add_parser("run", help="Run services")
    run_subparsers = run_parser.add_subparsers(dest="subcommand", help="service to run", required=True)

    run_subparsers.add_parser("api", help="Run FastAPI server")

    # migrations command
    migrations_parser = subparsers.add_parser("migrations", help="Database migrations")
    migrations_subparsers = migrations_parser.add_subparsers(
        dest="subcommand",
        help="migration operation",
        required=True,
    )

    autogenerate_parser = migrations_subparsers.add_parser("autogenerate", help="Autogenerate migration")
    autogenerate_parser.add_argument("message", help="Migration message/description")

    run_parser = migrations_subparsers.add_parser("apply", help="Apply migrations")

    return parser


def main() -> None:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "run":
        if args.subcommand == "api":
            run_api()
        else:
            parser.error(f"Unknown run subcommand: {args.subcommand}")

    elif args.command == "migrations":
        if args.subcommand == "autogenerate":
            autogenerate_migrations(args.message)
        elif args.subcommand == "apply":
            run_migrations()
        else:
            parser.error(f"Unknown migrations subcommand: {args.subcommand}")

    else:
        parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
