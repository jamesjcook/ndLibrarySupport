#!/usr/bin/env bash
# facilitate not-archived connectome review_dir
# assumes archive is mounted to a:
# and remote scratch mounted to s:


project_code=20.5xfad.01;

# WARNING: letter-colon ex c: is NOT a valid path in git-bash.
# these are being assigned this way to reduce nonsense,
# when testing for their existing a forced letter is added.
archive_dir="a:";
scratch_dir="s:";

if [ ! -e "${archive_dir}/" ];
then
    echo "Missing archive dir on \"${archive_dir}/\"" >&2;
    exit 1;
fi;
if [ ! -e "${scratch_dir}/" ];
then
    echo "Missing scratch disk on \"${scratch_dir}/\"" >&2;
    exit 1;
fi;

review_dir=$BIGGUS_DISKUS/data_review_links/$project_code;
if [[ ! -e $review_dir ]];
then mkdir $review_dir; fi
for r in $(echo '
N58931 N58933 N58950 N59017 N59061 N59068 N59082 N59084 N59087 N59089
N60050 N60053 N60121 N60179 N60202 N60519 N60529 N60541 N60545 N60173
N60469 N60481 N60335 N60339 N60341 N60429 N60431 N60433 N60439 N60441
N60443 N60447 N60477 N60479 N60483 N60485 N60497 N60503 N60543 N60547
N60549 N60553 N60565 N60327 N60329 N60331 N60333 N60351 N60353 N60355
N60371 N60377 N60379 N60425 N60449 N60451 N60455 N60457 N60459 N60463
N60465 N60471 N60473 N60475
');
do
  r=${r}NLSAM
  diff=diffusion${r}dsi_studio
  # diffusion in archive
  d_a=${archive_dir}/$project_code/research/$diff;
  # diffusion link
  d_l=$review_dir/$diff
  #r=$(echo $diff |sed 's/diffusion//'|sed 's/dsi_studio//');
  # connectome on scratch
  c_s=${scratch_dir}/connectome${r}dsi_studio-results
  # connectome link
  c_l=$review_dir/connectome${r}dsi_studio
  if [ -e $d_a -a -e $c_s ];then
      if [ ! -e $c_l ];then
        ln -s $c_s $c_l;
      fi
      if [ ! -e $d_l ]; then
        ln -s $d_a $d_l;
      fi
  else
      echo "Skipped $r";
  fi
done
echo Set base dir to $(dirname $review_dir)
