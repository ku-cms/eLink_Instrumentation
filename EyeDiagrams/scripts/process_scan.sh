# process_scan.sh

data_dir=$1
storage_dir="/Users/caleb/CMS/Tracker/e-links/EyeDiagramData"


# check that directory was provided
if [ -z "$data_dir" ]
then
    echo "Please provide a direcotry in $storage_dir as the first argument"
    exit 1
fi

# check that directory exists
if [ ! -d "$storage_dir/$data_dir" ]
then
    echo "ERROR: The directory \"$storage_dir/$data_dir\" does not exist"
    exit 1
fi

clean_dir=""$data_dir"_clean"

cd $storage_dir
mkdir -p $clean_dir 

# use tail to clean files
# - only keep end of file
# - fixes byte 0x96 issue: there are no 0x96 bytes in the last three lines
# - some files have data from multiple runs
# - the correct data for each run is at the end of the file
for d in $data_dir/*
do
    d_base=`basename "$d"`
    # count number of csv files
    count=`ls -1 $d/*.csv 2>/dev/null | wc -l`
    #echo "numbers of csv files: $count"
    if [ $count != 0 ]
    then
        echo "$d_base"
        mkdir -p $clean_dir/$d_base
        for f in $d/*.csv
        do
            f_base=`basename "$f"`
            tail -n 3 $f > $clean_dir/$d_base/$f_base
        done
    fi
done

