for i in {400..10..50}; do
  echo $i
  pypy painting.py $i < ../tests/learn_and_teach.in > results/learn_and_teach/learn_and_teach_${i}.out
  echo $(wc -l results/learn_and_teach/learn_and_teach_${i}.out)
  echo ""
done
