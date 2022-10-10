
quick_affine=$WKS_SHARED/pipeline_utilities/quick_affine.bash
targ=$(find ${WORKSTATION_DATA}/atlas/symmetric45um/ -iname "*dwi.nhdr")
template_conf=$(cygpath -m "L:\ProjectSpace\22.edc.05\slicer_review_protocol\specimen_selections\template\lib.conf")
lib_dir=$(cygpath -m "L:\ProjectSpace\22.edc.05\slicer_review_protocol\specimen_selections");
for f in ../*; 
do 
	if [ ! -d $f ];then
		continue; fi
	runno=$(basename $f);
	# quick_affine
	echo $f; 
	od=$f/transforms
	if [ ! -d $od ];then mkdir $od; fi
	mov=$(find $f/ -iname "*dwi.nii.gz");
	$quick_affine $mov $targ $od
	if [ ! -e "$f/origin.mat" ];then
		ComposeMultiTransform 3 compose_t.txt $( for t in $(find $od -type l -exec readlink {} \; |sort -r); do echo $od/$t; done; ) && \
		ConvertTransformFile.exe 3 compose_t.txt origin.mat --convertToAffineType
		mv origin.mat $f/origin.mat;
	fi;
	runno_lib=$lib_dir/$runno
	lib_conf=$runno_lib/lib.conf
	if [ ! -d $runno_lib ];then
		mkdir $runno_lib;
		cp $template_conf $lib_conf
		echo "Path=../../../ornl_data_nifti/$runno" >> $lib_conf
	fi;
done

