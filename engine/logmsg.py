import sys
from utils import log

if len(sys.argv) < 3:
    sys.exit(1)

level = sys.argv[1]
message = " ".join(sys.argv[2:])

log(message, level)
