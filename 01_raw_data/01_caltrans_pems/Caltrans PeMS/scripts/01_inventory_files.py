# Resumable audit entry point. See run_full_pems_audit.py.
from run_full_pems_audit import inventory, scan
from audit_report import build
if __name__ == '__main__': inventory()
