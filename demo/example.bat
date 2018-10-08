..\test.exe -i test.efsm -o 0.seq -m white_box
..\test.exe -i test.efsm -o 1.seq -m black_box -mt transition_tour
..\test.exe -i test.efsm -o 2.seq -m black_box -mt hsi
..\test.exe -i test.efsm -o 3.seq -m white_box -mt efsm