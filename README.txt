1. Function name: list_frequency
2. Parameter: input_list (SExpression), target_list (SExpression)
3. Purpose of the function: given the input_list and target_list, the function will count the number sequence from target_list in input_list. If the number is not in the input_list, the number will have 0 times occurence. The given parameters are both SExpression, the output will be a conslist that consisting of separate conslists. Each conslists will be construed as the numeric that you want to count and the occurence for that number. eg: if you get the list like : 
(list (list 2 3) (list 3 8)) means number 2 will occur three times and number 3 will occur eight times. 

	eg: $slyther
	    >(list_frequency '(12 2 3 3 2 3 2 2 22 12 4 12) '(12 2 3 4))
    	     (list (list 12 3) (list 2 4) (list 3 3) (list 4 1))
4. Lastly, the example file for the function is list_freq.scm which tests for all cases of matching the frequencies
such as boolean(#t or #f), NIL lists as target, numbered lists, and the string list.  
