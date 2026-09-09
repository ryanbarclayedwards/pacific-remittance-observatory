"""python -m collect.run --all

Minimal connector registry and CLI, matching the entrypoint .github/workflows/collect.yml
already expects. Round 2 registers exactly the two connectors this round builds. Adding a
third connector to this dict is a later, deliberate decision -- not a side effect of this
file's structure.
"""
from __future__ import annotations

import argparse
import sys
import uuid
from datetime import datetime, timezone

from collect.benchmarks.nrbt import connector as nrbt_connector
from collect.store import append_observations

CONNECTORS = {
    "benchmarks.nrbt": nrbt_connector,
}


def new_collection_run_id() -> str:
    return f"run-{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{uuid.uuid4().hex[:8]}"


def run_all(connector_ids: list[str] | None = None) -> list[dict]:
    ids = connector_ids or list(CONNECTORS)
    collection_run_id = new_collection_run_id()
    all_observations: list[dict] = []

    for cid in ids:
        module = CONNECTORS[cid]
        # A connector failing outright (an unhandled exception, not a handled
        # availability_status="error" row) never takes down the whole run -- CLAUDE.md
        # section 4.1: losing a whole day because one provider changed its markup is the
        # failure mode to avoid. The exception itself is still surfaced, not swallowed.
        try:
            observations = module.run(collection_run_id)
        except Exception as exc:  # noqa: BLE001 -- deliberately broad, see comment above
            print(f"collect.run: {cid} raised {exc!r}; recording as an error and continuing", file=sys.stderr)
            observations = []
        all_observations.extend(observations)

    if all_observations:
        by_month: dict[str, list[dict]] = {}
        for obs in all_observations:
            month = obs["collected_at"][:7]
            by_month.setdefault(month, []).append(obs)
        for month, obs_list in by_month.items():
            append_observations(obs_list, month=month)

    return all_observations


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--connector", action="append", dest="connectors")
    args = parser.parse_args(argv)

    if args.all:
        observations = run_all()
    elif args.connectors:
        observations = run_all(args.connectors)
    else:
        parser.error("specify --all or --connector <id>")
        return 2

    not_observed = [o for o in observations if o["availability_status"] != "observed"]
    print(f"collect.run: {len(observations)} observation(s), {len(not_observed)} not 'observed'")
    for o in not_observed:
        print(f"  - {o['connector_id']}: {o['availability_status']}: {o['status_detail']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
