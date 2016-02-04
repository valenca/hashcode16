for i in {1..100}; do
  ../carlosf/a.out < dc.in > carlos.out
  cat dc.in carlos.out > OUT
  ../validator/a.out < OUT
  rm carlos.out
  rm OUT
done;
