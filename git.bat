d:
cd d:\htdocs\online-crm
git pull
git fetch origin crmsaller_20191004:crmsaller_20191004
git merge crmsaller_20191004
git push  origin master
set t=%date:~0,4%%date:~5,2%%date:~8,2%%time:~0,2%%time:~3,2%%time:~6,2%
git tag ������̨-%t: =0%-�޸�
git push  origin ������̨-%t: =0%-�޸�
cd D:\htdocs\git\cheseboy2000\
python wall.py
pause