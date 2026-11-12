"""Entry point: python -m pipeline.run [probe|full]"""
import sys


def main() -> None:
    mode = (sys.argv[1] if len(sys.argv) > 1 else "full").strip()
    if mode == "probe":
        from . import probe

        probe.main()
    else:
        from . import build

        build.main()


if __name__ == "__main__":
    main()
