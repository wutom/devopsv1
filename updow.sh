#!/bin/bash
#set -x
dowops()
 {
     rsync -aSvH root@192.168.0.251:/opt/django/vcgopsdev/* ~/wutom/code/vcg/vcgopsdev/
    }
upops()
    {
    rsync -aSvH ~/wutom/code/vcg/vcgopsdev/* root@192.168.0.251:/opt/django/vcgopsdev/
    }

    case "$1" in
        upcode)
            upops
            ;;
        dowcode)
            dowops
            ;;
        *)
    esac
