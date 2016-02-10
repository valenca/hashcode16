for i in {1..200..5}; do
  echo $i
  pypy main.py $i < tests/right_angle.in > results/right_angle/right_angle_${i}.out
  echo $(wc -l results/right_angle/right_angle_${i}.out)
  echo ""
done
