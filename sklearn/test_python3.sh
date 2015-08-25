#!/bin/bash

for FILE in cluster_example.py  dimension_reduction.py  faces.py  grid_search.py  linear_model.py  sklearn_examples.py;
do
    echo $FILE
    python3 ./${FILE}
done

