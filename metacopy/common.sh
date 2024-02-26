create_overlay_fs_working_dirs() 
{
    if [ ! -d $1 ]; then
        mkdir -p "$1"
    fi

    if [ ! -d $2 ]; then
        mkdir -p "$2"
    fi

    if [ ! -d $3 ]; then
        mkdir -p "$3"
    fi  

    if [ ! -d $4 ]; then
        mkdir -p "$4"
    fi
}

mount_overlay_fs()  
{
    create_overlay_fs_working_dirs $1 $2 $3 $4
    echo "lower: $1, upper: $2, work: $3, merge: $4, metacopy: $5"
    sudo mount -t overlay overlay -olowerdir=$1,upperdir=$2,workdir=$3,redirect_dir=on,metacopy=$5 $4
}

