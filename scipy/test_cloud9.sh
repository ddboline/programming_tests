#!/bin/bash

for FILE in analyze_audio.py bayesian_blocks.py fft_test.py framing_lena.py image_blur.py linalg_test.py periodicity_finder.py;
do
    echo $FILE
    ./${FILE}
done
