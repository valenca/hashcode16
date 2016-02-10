for i in {1..100000}; do
  ../carlosf/a.out < dc.in > carlos.out
  cat dc.in carlos.out > OUT
  ../validator/a.out < OUT >> PUMBAS
  rm carlos.out
  rm OUT
  #sleep 1.1
done;
