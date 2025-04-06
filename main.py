from HeadMade import HeadMade
import sys

HEADLESS = sys.argv[1] if len(sys.argv) > 1 else "No"

if __name__ == "__main__":
    HeadMade.main(HEADLESS)