from __future__ import print_function
import inner_product_test as mod
import par_args

avg = lambda s: sum(s)/len(s)
def make_plot():
    import pandas as pd
    from pandas import DataFrame 
    df = DataFrame(rows, columns=header)
    spds = df['t_s']/df['t_p']
    gf = spds.groupby(df['scale'])#'p'])
    spds.plot()
    #for s in scales:
    #    sertimes = [t[0] for t in timers[s]]
    #    partimes = [t[1] for t in timers[s]]
    #    avgser = avg(sertimes)
    #    speedups[s] = [avgser/pt for pt in partimes]
    #import pandas as pd
    #df = pd.DataFrame(speedups, index=cpucounts)
    #print(df)
    #df.plot()

def get_main(module):
    """returns the main function of a module to test

    :module: @todo
    :returns: @todo

    """
    return module.big_main

if __name__ == '__main__':
    args = par_args.get_args()
    scales    = [15,20]#,25]
    cpucounts = [2,3,4,6,8]
    
    main_func = get_main(mod)
    print(mod.__name__)
    rows = []
    for s in scales:
        args.scale = s
        for NP in cpucounts:
            args.procs = NP
            rows.append(main_func(args))
    outfp = open('{0}.csv'.format(mod.__name__), 'w')
    header = ("scale","p","t_s","t_p")
    print("{0},{1},{2},{3}".format(*header), file=outfp)
    for row in rows:
        print("{0},{1},{2},{3}".format(*row), file=outfp)
