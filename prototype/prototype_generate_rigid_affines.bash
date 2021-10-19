#!/usr/bin/env bash
# while these originally had an atlas rigid reg done as part of samba, it has samba's pre-process headers
# which have some caveats to use.
# To skip that problem we can get a quick rigid for all.

study_dir="L:/ProjectSpace/bxd_RCCF_review";
code_dir="$study_dir/code";
contrast="labels";

atlas_file=$(find $WORKSTATION_DATA/atlas/symmetric45um/ -iname "*_${contrast}.nhdr");
work_log="$code_dir/${contrast}_images.log";
find $study_dir/BXD* -iname "*_${contrast}.nhdr" > $work_log
declare -x ANTSPATH=/l/workstation/home/ants_2021_06_26;
declare -x PATH="$ANTSPATH:$PATH";
while read image; do
    out_dir="$(dirname $image)/transforms/rotate_to_atlas";
    if [ ! -d "$out_dir" ];then mkdir -p $out_dir; fi;
    tform=$(find $out_dir/ -iname "*${contrast}*.mat");
    if [ -z "$tform" ];then
        echo "";
        $WKS_SHARED/pipeline_utilities/reg_quick.bash $image $atlas_file $out_dir |tee $out_dir/reg.log
    else
        echo -n ".";
    fi;
#done < <(echo "no_file");
done < $work_log

while read image; do
    im_dir=$(dirname $image);
    out_dir="$im_dir/transforms/rotate_to_atlas";
    t_count=$(find $out_dir/ -iname "*${contrast}*.mat" |wc -l);
    tform=$(find $out_dir/ -iname "*${contrast}*.mat");
    ot_name="origin_rotation.mat";
    origin_tform="$im_dir/$ot_name";
    if [ "$t_count" -gt 1 ];then
        #ComposeMultiTransform ImageDimension output_affine_txt [-R reference_affine_txt] {[-i] affine_transform_txt}
        if [ ! -e "$origin_tform" ];then
            echo "Composite transform"
            ComposeMultiTransform 3 $origin_tform $(ls -r $tform);
        fi;
        ConvertTransformFile 3 $origin_tform $origin_tform --convertToAffineType
    elif [ -a ! -e "$origin_tform" ];then
        echo "single transform";
        ln -s $tform $origin_tform;
    fi
    #
    # conf update
    #
    conf="$im_dir/lib.conf";
    et=$(grep OriginTransform $conf |cut -d '=' -f2-);
    if [ -z "$et" -o "$et" != "$ot_name" ];then 
        tfline="OriginTransform=$ot_name";
        if [ -z "$et" ];then
            echo $tf_line >> $conf;
        else
            #sed -i 's/old-text/new-text/g' input.txt
            sed -i 's/OriginTransform.*/'"$tfline"'/' $conf;
        fi;
    fi;
done < $work_log
