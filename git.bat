cd D:\htdocs\git\cheseboy2000\
python wall_all.py
pause
exit
d:
cd d:\htdocs\online-crm
git pull
git fetch origin crmsaller_20191014:crmsaller_20191014
git merge crmsaller_20191014
git push  origin master
set t=%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%
git tag 筑龙后台-%t: =0%-修改
git push  origin 筑龙后台-%t: =0%-修改
cd D:\htdocs\git\cheseboy2000\
python wall.py
