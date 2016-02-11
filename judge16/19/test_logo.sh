for i in {1..80..1}; do
  echo $i
  pypy painting.py $i < ../tests/logo.in > results/logo/logo_${i}.out
  echo $(wc -l results/logo/logo_${i}.out)
  echo ""
done
