# process.sh

# bash script to process zip file
# zip file should contain csv files from eye diagram data

# arguments
# 1 - full path to zip file
# 2 - cable number

file=$1
cable_num=$2 
storage_dir="/home/kucms/CMS/Tracker/e-links/EyeDiagramData"
target_dir=""$PWD"/data"

echo "It's go time."
echo "Input file: $file"

# check that file was provided
if [ -z "$file" ]
then
    echo "Please provide a zip file containing eye diagram statistics csv files as the first argument."
    exit 1
fi

# check that cable number was provided
if [ -z "$cable_num" ]
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
output_dir="$target_dir"/"Cable_"$cable_num""

# unpack files in a new directory
cd $storage_dir
rsync -az $file .
unzip $file
mkdir -p $raw_dir 
mv *.csv $raw_dir 

# use tail to clean files
# - only keep end of file
# - fixes byte 0x96 issue: there are no 0x96 bytes in the last three lines
mkdir -p $clean_dir
for f in "$raw_dir"/*
do
    if [ -f "$f" ]
    then
        base=`basename "$f"`
        tail -n 3 "$f" > "$clean_dir"/"$base"
    fi
done

# copy to data directory in framework
mkdir -p $output_dir
rsync -az $clean_dir/ $output_dir

