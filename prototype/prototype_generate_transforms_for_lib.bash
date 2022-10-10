
quick_affine=$WKS_SHARED/pipeline_utilities/quick_affine.bash
targ=$(find ${WORKSTATION_DATA}/atlas/symmetric45um/ -iname "*dwi.nhdr")
for f in ../*; 
do 
	if [ ! -d $f ];then
		continue; fi
	# quick_affine
	echo $f; 
	od=$f/transforms
	if [ ! -d $od ];then mkdir $od; fi
	mov=$(find $f/ -iname "*dwi.nii.gz");
	$quick_affine $mov $targ $od
	rm "$f/origin.mat";
	if [ ! -e "$f/origin.mat" ];then
		ComposeMultiTransform 3 compose_t.txt $( for t in $(find $od -type l -exec readlink {} \; |sort -r); do echo $od/$t; done; ) && \
		ConvertTransformFile.exe 3 compose_t.txt origin.mat --convertToAffineType
		mv origin.mat $f/origin.mat;
	fi;
done

