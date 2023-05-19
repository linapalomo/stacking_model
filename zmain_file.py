# run_scripts.py

import subprocess

num_runs = 50
keyword= 'Result -'

for i in range(num_runs):
    result0 = subprocess.run(["python", "ztest0.py"], capture_output=True, text=True)
    output0 = result0.stdout
    with open('all_output.txt', 'a') as f:
        f.write(output0)
    
    result1 = subprocess.run(["python", "ztest1.py"], capture_output=True, text=True)
    output1 = result1.stdout
    lines= output1.split("\n")
    start_line=next((index for index, line in enumerate(lines)if keyword in line), None)
    
    if start_line is not None:
        result_output = '\n'.join(lines[start_line:])
    else:
        result_output =''
        
    with open('all_output.txt', 'a') as f:
          f.write(result_output + '\n\n')

    result2 = subprocess.run(["python", "ztest2.py"], capture_output=True, text=True)
    output2 = result2.stdout
    lines2= output2.split("\n")
    start_line2=next((index for index, line in enumerate(lines2)if keyword in line), None)
    
    if start_line2 is not None:
        result_output2 = '\n'.join(lines2[start_line2:])
    else:
        result_output2 =''
    with open('all_output.txt', 'a') as f:
        f.write(result_output2)
        
'''for i in range(num_runs):
    result0 = subprocess.run(["python", "ztest0.py"], capture_output=True, text=True)
    output0 = result0.stdout
    with open('test0_output.txt', 'a') as f:
        f.write(output0)
    
    result1 = subprocess.run(["python", "ztest1.py"], capture_output=True, text=True)
    output1 = result1.stdout
    with open('test1_output.txt', 'a') as f:
        f.write(output1)

    result2 = subprocess.run(["python", "ztest2.py"], capture_output=True, text=True)
    output2 = result2.stdout
    with open('test2_output.txt', 'a') as f:
        f.write(output2)

'''