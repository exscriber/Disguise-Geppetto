#!/usr/bin/env python3
# Created by Artificial Blondes
# This code is freely distributable under the terms of the [MIT license]

import argparse
import json
import os
from pprint import pprint
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

DEFAULT_URL = "http://192.168.1.34:80"
EXEC_ENDPOINT = "api/session/python/execute"


def split_multiline(string: str):
    """Split multiline string into JSON array"""
    return [x for x in string.splitlines() if x.strip()]


def emit(data):
    """Write machine-readable JSON to stdout."""
    # print(json.dumps(data, indent=2, ensure_ascii=False))
    pprint(data, width=120, compact=True, sort_dicts=False)


def read_script(args: argparse.Namespace) -> str:
    if args.file:
        with open(args.file, 'r', encoding='utf-8') as file:
            return ''.join(line for line in file if line.strip() != 'from d3 import *')

    if args.code is not None:
        if args.code == "-":
            return sys.stdin.read()
        return args.code

    if not sys.stdin.isatty():
        return sys.stdin.read()

    raise ValueError("Provide code, a file, or pipe Python through stdin")


def run(args: argparse.Namespace):
    try:
        script = read_script(args)
        payload = {"script": script}

        if args.module:
            payload["moduleName"] = args.module

        request = Request(
            url=urljoin(args.server, EXEC_ENDPOINT),
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=args.timeout) as response:
                status_code = response.status
                response_text = response.read().decode("utf-8", errors="replace")

        except HTTPError as e:
            status_code = e.code
            response_text = e.read().decode("utf-8", errors="replace")

        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            emit({"error": "Server did not return valid JSON", "response": response_text})
            return 1

        # RPC error code and message formatting
        if result['status']['code'] != 0:
            result['status']['message'] = split_multiline(result['status']['message'])
            emit(result)
            return 1

        # Make JSON values easier to read
        try:
            del result["pythonLog"]
            result["d3Log"] = split_multiline(result.get("d3Log"))
            result["returnValue"] = json.loads(result.get("returnValue"))
        except json.JSONDecodeError:
            pass

        emit(result)
        return 0

    except URLError as e:
        emit({"error": f"Could not connect to D3 server {e=}"})
        return 1

    except Exception as e:
        emit({"error": repr(e)})
        return 1


def main():
    parser = argparse.ArgumentParser(description="Execute Python scripts in Disguise Designer")

    parser.add_argument(
        "--server",
        metavar='URL',
        default=os.environ.get("D3_URL", DEFAULT_URL),
        help="D3 server base URL (or set D3_URL)",
    )
    parser.add_argument(
        "--timeout",
        metavar='SEC',
        type=float,
        default=5,
        help="HTTP timeout (default: %(default).1f seconds)",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
        help="Execute Python in Designer",
    )

    exec_parser = subparsers.add_parser("exec", aliases=["execute"])
    group = exec_parser.add_mutually_exclusive_group(required=True)
    group.add_argument("code", metavar='CODE', nargs="?", help="Python code, or '-' to read stdin")
    group.add_argument("-f", "--file", help="Read Python code from file")
    exec_parser.add_argument("-m", "--module", help="Execute inside named module")

    args = parser.parse_args()

    sys.exit(run(args))


if __name__ == "__main__":
    main()
