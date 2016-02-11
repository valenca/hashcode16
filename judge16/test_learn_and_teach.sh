for i in {1..20..2}; do
  echo $i
  pypy main.py $i < tests/learn_and_teach.in > results/learn_and_teach/learn_and_teach_${i}.out
  echo $(wc -l results/learn_and_teach/learn_and_teach_${i}.out)
  echo ""
done

for i in {21..800..10}; do
  echo $i
  pypy main.py $i < tests/learn_and_teach.in > results/learn_and_teach/learn_and_teach_${i}.out
  echo $(wc -l results/learn_and_teach/learn_and_teach_${i}.out)
  echo ""
done
