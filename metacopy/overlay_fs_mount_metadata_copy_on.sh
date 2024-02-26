#!/bin/bash
source ./common.sh
OVERLAY_FS_MOUNT_POINT="overlayfs_metacopy_on"
UPPER_DIR=/home/$USER/$OVERLAY_FS_MOUNT_POINT/write_dir
#LOWER_DIR=/home/$USER/non-overlayfs-test
LOWER_DIR=/home/$USER/$OVERLAY_FS_MOUNT_POINT/readonly_dir
MERGE_DIR=/home/$USER/$OVERLAY_FS_MOUNT_POINT/merge_dir
WORK_DIR=/home/$USER/$OVERLAY_FS_MOUNT_POINT/work_dir

mount_overlay_fs()  
{
    create_overlay_fs_working_dirs $1 $2 $3 $4
    echo "lower: $1, upper: $2, work: $3, merge: $4, metacopy: $5"
    if [-e $5 on]
    sudo mount -t overlay overlay -olowerdir=$1,upperdir=$2,workdir=$3,redirect_dir=on,metacopy=$5 $4
}

mount_overlay_fs $LOWER_DIR $UPPER_DIR $WORK_DIR $MERGE_DIR on