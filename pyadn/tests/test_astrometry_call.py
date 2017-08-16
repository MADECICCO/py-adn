from subprocess import check_output

def test_call_astrometry():
    print check_output("echo $PATH",shell=True)
    print check_output("$HOME/an/bin/solve-field",shell=True)
    print check_output("solve-field",shell=True)
