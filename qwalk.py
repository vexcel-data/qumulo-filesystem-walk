#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import os
import sys

from qwalk_utils import get_disk_usage, write_error_in_data
from qwalk_worker import QTASKS, QWalkWorker, log_it


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Walk Qumulo filesystem and do that thing."
    )
    parser.add_argument("-s", help="Qumulo hostname", required=True)
    parser.add_argument(
        "-u", help="Qumulo API user", default=os.getenv("QUSER") or "admin"
    )
    parser.add_argument(
        "-p", help="Qumulo API password", default=os.getenv("QPASS") or "admin"
    )
    parser.add_argument("-d", help="Starting directory", required=True)
    parser.add_argument("-g", help="Run with filesystem changes", action="store_true")
    parser.add_argument("-l", help="Log file", default="output-walk-log.txt")
    parser.add_argument(
        "-c",
        help="Class to run.",
        choices=list(QTASKS.keys()),
        required=True,
    )
    parser.add_argument("--security_space",help="Security space in disk  in bytes",required=False,default=219902325555200)
    parser.add_argument("--data_ticket",help="Data to be copied",required=False)
    parser.add_argument("--snap", help="Snapshot id")

    try:
        # Will fail with missing args, but unknown args will all fall through.
        args, other_args = parser.parse_known_args()
    except:
        print("-" * 80)
        parser.print_help()
        print("-" * 80)
        sys.exit(-2)
    security_space = int(args.security_space)
    other_args.append("--data_ticket")
    other_args.append(args.data_ticket)
    other_args.append("--security_space")
    other_args.append(str(args.security_space))
    other_args.append("--host")
    other_args.append(args.s)

    if 'qc208' in args.s:
        normal_path = args.d
        qc_path = normal_path.replace('Shares','qc208')
        if not os.path.exists(qc_path):
            log_it("Path does not exists")
            write_error_in_data(args.data_ticket, 'Path does not exists')
            exit(-1)
        total, used, free, used_percent = get_disk_usage('/qc208/ultramap-production')
        if free < security_space:
            log_it("Security space has been reached")
        else:
            log_it(f'free space is {free} and security space is {security_space}')

    if 'QHPE180' in args.s:
        normal_path = args.d
        qc_path = normal_path.replace('Shares','qhpe180')
        if not os.path.exists(qc_path):
            log_it("Path does not exists")
            write_error_in_data(args.data_ticket, 'Path does not exists')
            exit(-1)
        total, used, free, used_percent = get_disk_usage('/qhpe180/ultramap-production')
        if free < security_space:
            log_it("Security space has been reached")
        else:
            log_it(f'free space is {free} and security space is {security_space}')



    QWalkWorker.run_all(
        args.s,
        args.u,
        args.p,
        args.d,
        args.g,
        args.l,
        args.c,
        args.snap,
        other_args,
    )


if __name__ == "__main__":
    main()
