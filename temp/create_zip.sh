source ~/Tinder_env/bin/activate
cd /home/owner/Tinder_env/lib/python3.6/site-packages/
zip -r9 /home/owner/Documents/Github_projects/Tinder_analysis/temp/aws_transformer.zip . -q
cd $git_path/Tinder_analysis/temp
cp -r ../Scripts .
cp ../aws_transformer.py aws_transformer.py
zip -g aws_transformer.zip aws_transformer.py 
zip -g -r aws_transformer.zip Scripts
echo "Completed zip"
