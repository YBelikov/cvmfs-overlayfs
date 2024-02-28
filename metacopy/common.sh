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



