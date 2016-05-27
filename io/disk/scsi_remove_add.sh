#!/bin/bash -e

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright: 2016 IBM
# Author: Narasimhan V <sim@linux.vnet.ibm.com>

# This Test removes and adds back a scsi device in all the specified PCI 
# domains specified in the 'config' file.

PATH=$(avocado "exec-path"):$PATH

# Install dependencies
if [[ `python -c 'from avocado.utils.software_manager import SoftwareManager; \
    print SoftwareManager().install("lsscsi")'` == 'False' ]]
then
    echo "lsscsi not installed"
    exit
fi

CONFIG_FILE="$AVOCADO_TEST_DATADIR"/config
pci_devices=$(cat $CONFIG_FILE | grep -w "PCI_devices" | awk -F'=' '{print $(NF)}')
echo "PCI Devices "$pci_devices

for pci_device in $pci_devices; do
    echo "PCI Device $pci_device"
    device_list_output=($(ls -l /dev/disk/by-path/ | grep "$pci_device" | awk '{print $NF}'))
    if [[ -z $device_list_output ]]; then
        echo "No Devices in PCI ID $pci_device"
        continue
    fi
    for (( device_id=0; device_id<${#device_list_output[@]}; device_id++ )); do
        device=$(echo ${device_list_output[device_id]} | sed -e 's/\// /g' | awk '{print $NF}')
        scsi_num=$(lsscsi | grep $device | awk  -F'[' '{print $NF}' | awk  -F']' '{print $1}')
        if [[ -z $scsi_num ]]; then
            echo "No SCSI Devices in PCI ID $pci_device"
            continue
        fi
        scsi_num_seperated=$(echo $scsi_num | sed -e 's/:/ /g')
        echo $device
        echo $scsi_num_seperated
        echo "Current Config"
        lsscsi
        echo "deleting $scsi_num"
        echo 1 > /sys/block/$device/device/delete
        sleep 5
        lsscsi
        echo "$scsi_num deleted"
        echo "adding $scsi_num back"
        echo "scsi add-single-device $scsi_num_seperated" > /proc/scsi/scsi
        sleep 5
        lsscsi
        echo "$scsi_num added back"
        echo
    done
    echo
done
