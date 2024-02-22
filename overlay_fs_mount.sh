#!/bin/bash
OVERLAY_FS_MOUNT_POINT="overlay_fs_test_no_metacopy"
UPPER_DIR=/home/$USER/$OVERLAY_FS_MOUNT_POINT/write_dir
LOWER_DIR=/home/$USER/$OVERLAY_FS_MOUNT_POINT/readonly_dir
MERGE_DIR=/home/$USER/$OVERLAY_FS_MOUNT_POINT/merge_dir
WORK_DIR=/home/$USER/$OVERLAY_FS_MOUNT_POINT/work_dir

create_test_dirs() 
{
    if [ ! -d $UPPER_DIR ]; then
        mkdir -p "$UPPER_DIR"
    fi

    if [ ! -d $LOWER_DIR ]; then
        mkdir -p "$LOWER_DIR"
    fi

    if [ ! -d $WORK_DIR ]; then
        mkdir -p "$WORK_DIR"
    fi

    if [ ! -d $MERGE_DIR ]; then
        mkdir -p "$MERGE_DIR"
    fi  
}

mount_with_metadata_copy()  
{
    create_test_dirs
    sudo mount -t overlay overlay -olowerdir=$LOWER_DIR,upperdir=$UPPER_DIR,workdir=$WORK_DIR,metacopy=on $MERGE_DIR
}

mount_with_metadata_copy