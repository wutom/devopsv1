#!/bin/bash

#####tom.wang#####

BASE_ROOT=$(dirname $0)
LOG_FILE=/var/log/idcmanage.log
HOST=0.0.0.0
PORT=8000

if [ ! -d ${BASE_ROOT} ]; then
	echo "Error can't find ${BASE_ROOT}"
	exit 2
fi

pushd ${BASE_ROOT} > /dev/null

check()
{
    _c=$(ps -ef|grep "manage.py runserver ${HOST}:${PORT}"|egrep -v "grep|vi|cat"|wc -l)
	if (( $_c != 0 )); then
		return 1
	else
		return 0
	fi
}

start()
{
	python manage.py runserver ${HOST}:${PORT} >> ${LOG_FILE} 2>&1 &
}

stop()
{
	ps -ef|grep "python manage.py runserver ${HOST}:${PORT}"|egrep -v "grep|vi|cat"|awk '{print "kill -9 "$2}'|sh
}

case "$1" in
    start)
	check
	if (( $? == 0 )); then
		start
	else
		echo "service is running"
	fi
        ;;
    stop)
	check
        if (( $? == 1 )); then
		stop
	else
		echo "service not run"
	fi
        ;;
    *)
	echo $"Usage: $0 {start|stop}"
	exit 1
esac
