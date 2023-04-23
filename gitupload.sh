function get_char()
{
  SAVEDSTTY=`stty -g`
  stty -echo
  stty cbreak
  dd if=/dev/tty bs=1 count=1 2> /dev/null
  stty -raw
  stty echo
  stty $SAVEDSTTY
}

enable_pause=1
function pause()
{
  if [ "x$1" != "x" ]; then
    echo $1
  fi
  if [ $enable_pause -eq 1 ]; then
    echo "Press any key to continue!"
    char=`get_char`
  fi
}

git add .
git commit -m "update algos"
git push ;
echo "开心的一天"
pause "upload done.! "
