#!/bin/sh
  function ergodic(){
   for file in `ls $1`
   do
     if [ -d $1"/"$file ]
     then
       ergodic $1"/"$file
     else
       local path=$1"/"$file
       local name=$file
       file_type=${name##*.}
       if [[ $file_type == "php" ]];then
         php -l $path
       fi
     fi
   done
 }
 ergodic $1