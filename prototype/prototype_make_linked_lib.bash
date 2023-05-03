review_dir=l:/projectspace/kjh60/kempermann_review
for diff in $(echo 'diffusionS69338NLSAMdsi_studio
diffusionS69308NLSAMdsi_studio
diffusionS69312NLSAMdsi_studio
diffusionS69366NLSAMdsi_studio
diffusionS69372NLSAMdsi_studio
diffusionS69364NLSAMdsi_studio
diffusionS69362NLSAMdsi_studio
diffusionS69360NLSAMdsi_studio
diffusionS69358NLSAMdsi_studio
diffusionS69368NLSAMdsi_studio
diffusionS69354NLSAMdsi_studio
diffusionS69352NLSAMdsi_studio
diffusionS69350NLSAMdsi_studio
diffusionS69348NLSAMdsi_studio
diffusionS69346NLSAMdsi_studio
diffusionS69344NLSAMdsi_studio
diffusionS69340NLSAMdsi_studio
diffusionS69336NLSAMdsi_studio
diffusionS69334NLSAMdsi_studio
diffusionS69332NLSAMdsi_studio
diffusionS69330NLSAMdsi_studio
diffusionS69328NLSAMdsi_studio
diffusionS69326NLSAMdsi_studio
diffusionS69324NLSAMdsi_studio
diffusionS69318NLSAMdsi_studio
diffusionS69320NLSAMdsi_studio
diffusionS69316NLSAMdsi_studio
diffusionS69314NLSAMdsi_studio
diffusionS69310NLSAMdsi_studio
diffusionS69342NLSAMdsi_studio
'); do
  d_a=a:/22.kempermann.01/research/$diff; 
  d_l=$review_dir/$diff
  r=$(echo $diff |sed 's/diffusion//'|sed 's/dsi_studio//');
  c_v=//vidconfmac/vidconfmacspace/connectome${r}dsi_studio-results
  c_l=$review_dir/connectome${r}dsi_studio
  if [ -e $d_a -a -e $c_v ];then 
	  if [ ! -e $c_l ];then 
		ln -s $c_v $c_l; 
	  fi
	  if [ ! -e $d_l ]; then 
		ln -s $d_a $d_l; 
	  fi
  fi
done
