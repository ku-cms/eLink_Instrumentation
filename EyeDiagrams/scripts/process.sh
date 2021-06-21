# process.sh

# bash script to process zip file
# zip file should contain csv files from eye diagram data


file=$1
cable_num=$2 
storage_dir="/home/kucms/CMS/Tracker/e-links/EyeDiagramData"
target_dir="data"

echo "It's go time."
echo "Input file: $file"

# check that file was provided
if [ -z $file ]
then
    echo "Please provide a zip file containing eye diagram statistics csv files as the first argument."
    exit 1
fi

# check that cable number was provided
if [ -z $cable_num ]
then
    echo "Please provide the cable number as the second argument."
    exit 1
fi

# check that file exists
if [ ! -f $file ]
then
    echo "File not found: $file"
    exit 1
fi

raw_dir="Cable_"$cable_num"_raw"
clean_dir="Cable_"$cable_num"_clean"

# move files to new directory
cd $storage_dir
rsync -az $file .
unzip $file
mkdir -p $raw_dir 
mv *.csv $raw_dir 

