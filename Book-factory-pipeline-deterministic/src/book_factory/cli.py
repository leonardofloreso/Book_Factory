from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline_controller import PipelineController


def main() -> None:
    p = argparse.ArgumentParser(prog="book_factory")
    p.add_argument("input", help="Path to input_book.json")
    args = p.parse_args()

    controller = PipelineController()
    run_dir = controller.run_all(input_path=Path(args.input))
    print(str(run_dir))


if __name__ == "__main__":
    main()
