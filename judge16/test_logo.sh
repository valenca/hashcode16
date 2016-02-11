for i in {1..80..1}; do
  echo $i
  pypy main.py $i < tests/logo.in > results/logo_2/logo_${i}.out
  echo $(wc -l results/logo_2/logo_${i}.out)
  echo ""
done
