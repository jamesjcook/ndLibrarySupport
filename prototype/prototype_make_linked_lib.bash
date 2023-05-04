#review_dir=l:/projectspace/kjh60/kempermann_review
project_code=20.5xfad.01;
review_dir=$BIGGUS_DISKUS/review_links/$project_code;
if [[ ! -e $review_dir ]];
then mkdir $review_dir; fi
for r in $(echo '
N60206NLSAM
N60208NLSAM
N60213NLSAM
N60215NLSAM');
do
  diff=diffusion${r}dsi_studio
  d_a=a:/$project_code/research/$diff;
  d_l=$review_dir/$diff
  #r=$(echo $diff |sed 's/diffusion//'|sed 's/dsi_studio//');
  c_v=s:/connectome${r}dsi_studio-results
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
echo Set base dir to $(dirname $review_dir)
