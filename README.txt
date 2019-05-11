Deliverable 6

1. Function name: list_frequency
2. Parameter: input_list (SExpression), target_list (SExpression)
3. Purpose of the function: given the input_list and target_list, the function will count the number sequence from target_list in input_list. If the number is not in the input_list, the number will have 0 times occurence. The given parameters are both SExpression, the output will be a conslist that consisting of separate conslists. Each conslists will be construed as the numeric that you want to count and the occurence for that number. eg: if you get the list like : 
(list (list 2 3) (list 3 8)) means number 2 will occur three times and number 3 will occur eight times. 

	eg: $slyther
	    >(list_frequency '(12 2 3 3 2 3 2 2 22 12 4 12) '(12 2 3 4))
    	     (list (list 12 3) (list 2 4) (list 3 3) (list 4 1))
4. Lastly, the example file for the function is list_freq.scm which tests for all cases of matching the frequencies
such as boolean(#t or #f), NIL lists as target, numbered lists, and the string list.  

Deliverable 7

- We got the REPL working nicer by using prompt toolkit, now the user should be able to re-run the commands
in history by simply pressing the up arrow key.
- We also have curry to be possible with lambda functions.
so cases, like (define foo (curry (lambda (x) (+ x 1)))) will create
the curry function that can be used for other things. We could not figure
out how to do ConsList as a function, or ConsCell as a function as shown in
the racket documentation of the curry function.
- We also have some functions from python module matplotlib. We implemented the plotting methods for pie-plot and scatter plot. type in (plot?) for information on the plotting methods. An example of how to use the function is shown
below.

(plot-scatter '(1 2 3 4) '(5 6 7 8) "--p")
will have the user run through the program of plotting the plot with given
title, x-axis, and y-axis. In this case, the x data is '(1 2 3 4)
and the y data is '(5 6 7 8)
It will then save the plot to a pdf file specified by the function.
(plot-scatter any-conslist any-conslist "--h")
will tell the user how the function works

(plot-pie '("C++" "Java" "Python") '(98 88 50) "--p")
will have the user run through the program of plotting the plot with the given title, x-axis, and y-axis. In this case, the x data represent the legend
for the pie plot and the y data is the data respective to each legend. In this example let's say the % usage of C++ is 98% and percent usage of Java is 88% and vise versa. It will also save the file specified by the function.
(plot-pie any-conslist any-conslist "--h")
will tell the user how the function works

