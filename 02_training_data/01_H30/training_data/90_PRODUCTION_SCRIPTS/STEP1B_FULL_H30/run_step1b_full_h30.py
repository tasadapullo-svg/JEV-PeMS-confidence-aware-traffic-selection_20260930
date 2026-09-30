"""Step 1B H30 production entry point. Use --smoke only for development checks."""
from __future__ import annotations

import argparse
from pipeline_core import Pipeline

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--smoke', action='store_true', help='Train-only May 23/24/25 smoke run')
    args = parser.parse_args()
    Pipeline(smoke=args.smoke).run()

if __name__ == '__main__':
    main()
