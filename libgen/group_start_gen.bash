#!/usr/bin/env bash
# for each BXD dir, check if content is reasonably complete(using presence of iso and dwi images)
# generate windows batch file to launch with that group from template.

cd /l/ProjectSpace/bxd_RCCF_review;
#g_conf_ex="code/ndLibrarySupport/example/samba_packed_study/lib.conf";
s_template="code/ndLibrarySupport/libgen/start_group_template.bat";

if [ ! -e $s_template ];then
    echo "Missing hard coded template $s_template";
    exit 1;
fi;

# clear the old logs.
find BXD*/ -iname "*.log" -delete
ready_spec=0;
for g in BXD*/; do
    dwi_imgs=$(find $g -iname "*dwi.nhdr"|wc -l);
    iso_imgs=$(find $g -iname "*iso.nhdr"|wc -l);
    label_imgs=$(find $g -iname "*labels.nhdr"|wc -l);
    max=$dwi_imgs;
    min=$label_imgs;
    if [ $max -lt $label_imgs ];then
        max=$label_imgs;
        min=$dwi_imgs;
    fi;
    if [ $max -ne $min ];then
        echo $min/$max $(basename $g);
        find $g -iname "*iso.nhdr" > $g/iso.log &
        find $g -iname "*labels.nhdr" > $g/labels.log &
    else
        g=$(basename $g);
        #g_conf="$g/lib.conf";
        #if [ ! -e $g_conf ];then 
        #    cp -p $g_conf_ex $g_conf || exit 1;
        #fi;
        #
        #if [ -e $g_conf ];then 
        # Thought maybe we should tell how many each represnt....
        #st_file="start_${g}_c$max.bat";
        # I think start X group is good...
        st_file="start_${max}_${g}.bat";
        #st_file="start_${g}.bat";
        if [ ! -e $st_file -o $st_file -ot $s_template ];then
            grep 'GROUP_NAME' $s_template | sed 's/GROUP_NAME/'$g'/' > $st_file
        fi;
        if [ -e $st_file ];then 
            let ready_spec=$ready_spec+$max;
            echo READY:$max $g;
        fi;
        #else 
        #    echo need_conf $g;
        #fi;
    fi;
done
wait;
echo "Total:$ready_spec specimens ready for review";
# label and iso logs
img="iso"; #make this variable so we can switch it out for something else if desired.
for g in BXD*/; do
    lc=$(ls $g/*.log 2> /dev/null|wc -l);
    if [ $lc -ge 2 ];then
        echo "=== $g ===";
        #logs=$(ls $g/*.log);
        for spec in $(for f in $(cat $g/*.log); do dirname $f;done|sort -u); do
            grep $spec $g/*.log |xargs;
        done
        echo "";
    fi;
done
