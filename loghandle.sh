#!/bin/bash
echo "start"
i=1
while [ $i -le 120 ]
do
	d=`date -d "${i} day ago " +%y%m%d`
        echo $d
  	filename="/data/wwwroot/group/group/log/sqllog/${d}.log"
	if [ ! -f $filename ];then
		echo "文件不存在${filename}"
	else
		grep -v downlog ${filename} > ${filename}1
		rm ${filename}
                mv  ${filename}1 ${filename}
		echo "文件处理${filename}"
	fi
	if [ ! -f ${filename}1 ];then
                echo "文件不存在${filename}1"
        else
                mv  ${filename}1 ${filename}
        fi
  	let i++
done
