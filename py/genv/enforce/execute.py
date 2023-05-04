import sys
from typing import Dict

from genv import os_
from genv import devices
from genv.envs.snapshot import Snapshot as Envs
from genv.processes.snapshot import Snapshot as Processes
from genv.enforce.report import Report


def _terminate(processes: Processes) -> None:
    for process in processes:
        try:
            print(
                f"Terminating process {process.pid} from environment {process.eid or 'N/A'} that is running on GPU(s) {','.join([str(index) for index in process.indices])}"
            )

            os_.terminate(process.pid)
        except PermissionError:
            print(
                f"[ERROR] Not enough permissions to terminate process {process.pid}",
                file=sys.stderr,
            )
        except ProcessLookupError:
            print(f"[DEBUG] Process {process.pid} already terminated", file=sys.stderr)


def _detach(envs: Dict[int, Envs]) -> None:
    for index, envs in envs.items():
        for env in envs:
            print(
                f"Detaching environment {env.eid} of user {env.username or 'N/A'} from device {index}"
            )

            devices.detach(env.eid, index)


def execute(report: Report) -> None:
    """
    Terminates processes and detaches environments from devices according to the given report.
    """
    _terminate(report.terminate)
    _detach(report.detach)
