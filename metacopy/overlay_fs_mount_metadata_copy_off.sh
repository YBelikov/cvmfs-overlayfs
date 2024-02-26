#!/bin/bash
source ./common.sh
OVERLAY_FS_MOUNT_POINT="overlayfs_metacopy_off"
UPPER_DIR=/home/$USER/$OVERLAY_FS_MOUNT_POINT/write_dir
LOWER_DIR=/home/$USER/$OVERLAY_FS_MOUNT_POINT/readonly_dir
MERGE_DIR=/home/$USER/$OVERLAY_FS_MOUNT_POINT/merge_dir
WORK_DIR=/home/$USER/$OVERLAY_FS_MOUNT_POINT/work_dir

mount_overlay_fs $LOWER_DIR $UPPER_DIR $WORK_DIR $MERGE_DIR off