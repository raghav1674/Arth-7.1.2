import os
import subprocess as sp 


def run_cmd(cmd):
    status , output = sp.getstatusoutput(cmd)
    if status == 0:
        return (0,output)
    return (-1,'Not Successfull\n'+output)



def display_cmd_output(cmd):
    os.system(cmd)





def create_pv(block_dev_path):
    display_cmd_output(f'pvcreate {" ".join(block_dev_path)}')
    display_cmd_output(f'pvdisplay')
    


def create_vg(pvs,vg_name):
     create_pv(pvs)
     display_cmd_output(f'vgcreate {vg_name} {" ".join(pvs)}')
     display_cmd_output(f'vgdisplay {vg_name}')

def extend_vg(pvs,vg_name):
    display_cmd_output(f'vgextend {vg_name} {" ".join(pvs)}')
    display_cmd_output(f'vgdisplay {vg_name}')


def create_lvm_part(vg_name,lv_name,size):
    display_cmd_output(f'lvcreate  --size +{size} --name {lv_name} {vg_name}')
    display_cmd_output(f'lvdisplay /dev/{vg_name}/{lv_name}')
    run_cmd('mkfs -t ext4 /dev/{vg_name}/{lv_name}')

def extend_lvm_part(vg_name,lv_name,size):
    display_cmd_output(f'lvextend -L +{size} /dev/{vg_name}/{lv_name} -q')
    run_cmd(f'resize2fs /dev/{vg_name}/{lv_name}')
    display_cmd_output(f'lvdisplay /dev/{vg_name}/{lv_name}')

def reduce_lvm_part(vg_name,lv_name,size):
    status,_ = run_cmd('umount /dev/{vg_name}/{lv_name}')
    run_cmd('e2fsck /dev/{vg_name}/{lv_name}')
    run_cmd(f'resize2fs /dev/{vg_name}/{lv_name} {size}')
    display_cmd_output(f'lvreduce -L -{size} /dev/{vg_name}/{lv_name} -q')
    display_cmd_output(f'lvdisplay /dev/{vg_name}/{lv_name}')
    if status==0:
        mount_lvm_part(vg_name,lv_name)

def mount_lvm_part(vg_name,lv_name,mount_point=''):
    if mount_point == '':
        mount_point = run_cmd('findmnt -m -o TARGET /dev/{vg_name}/{lv_name}')
    run_cmd(f'mount /dev/{vg_name}/{lv_name} {mount_point[1]}')


if __name__ == '__main__':
    #create_vg(['/dev/xvdg'],'myvg2')
    reduce_lvm_part('myvg2','mylvm2','500M')
