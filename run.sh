#!/bin/sh

python3 my-fault-injection-tool.py read_EIO
python3 my-fault-injection-tool.py read_EINTR
python3 my-fault-injection-tool.py write_ENOSPC
python3 my-fault-injection-tool.py write_EIO
python3 my-fault-injection-tool.py select_ENOMEM
python3 my-fault-injection-tool.py malloc_ENOMEM
