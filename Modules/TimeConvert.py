#This function get the difference between two time values returning them as a string
def TimeConvert(oldTime, Now):
    #get difference in seconds
    diff = Now - oldTime
    diffS = diff.total_seconds()
    #using the mod function able to shrink the values down to seconds
    y , mod_ = divmod(diffS, 31556926)
    d , mod_ = divmod(mod_, 86400)        
    h , mod_ = divmod(mod_, 3600)               
    m , mod_ = divmod(mod_, 60)                
    s , mod_ = divmod(mod_, 1) 
    #return the string
    return('{:02d} Days {:02d} Hours {:02d} Minutes and {:02d} Seconds'.format(int(d), int(h), int(m), int(s)))