// Command to run: idal -c -A -Sida_list.idc EXE

#include <idc.idc>

static find_a_func() {
    auto seg, ea, flags;
    seg = FirstSeg();
    while (seg != BADADDR) {
        ea = seg;
        while (ea != BADADDR) {
            flags = GetFlags(ea);
            if (isCode(flags)) {
                if (strlen(GetFunctionName(ea)) != 0)
                    return ea;
            }
            ea = NextNotTail(ea);
        }
        seg = NextSeg(seg);
    }
}

static ExpandFunction(ea) {
    if ( (GetFunctionFlags(ea) & FUNC_HIDDEN) == FUNC_HIDDEN )
        SetFunctionFlags(ea, GetFunctionFlags(ea) & (~FUNC_HIDDEN));
}


static main() 
{
    auto outfile;
    auto i, flgs, ffunc;

    // Wait for auto analysis to finish
    Wait(); 

    // Expand all the auto-collapsed functions
    ffunc = find_a_func();
    while ((ffunc != BADADDR) && (PrevFunction(ffunc) != BADADDR))
        ffunc = PrevFunction(ffunc);
    for (i = ffunc; i != BADADDR; i = NextFunction(i))
        ExpandFunction(i);

    // Output lst file
    outfile = fopen("ida.lst", "w");
    GenerateFile(OFILE_LST, outfile, 0, BADADDR, 0);
    fclose(outfile);
    
    Exit(0);
}
