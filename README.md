# CADOR
Hospital staff scheduling

## Planning data csv file format

The planning data is stored in a csv file with the following special format:

    instance_id                     <id>
    budgeted_workforce              <bw>
    partial_time_contracts_prop     <Pp>
    eighty_percent_contracts_prop   <P80>
    contracts_type                  1   2   3   4   5   6   7
    contracts_ratios                1   .9  .8  .75 .7  .6  .5
    contracts_costs                 1   .91 .85 .75 .7  .6  .5
    contracts_availability          A_1 A_2 A_3 A_4 A_5 A_6 A_7
    contracts_affected              a_1 a_2 a_3 a_4 a_5 a_6 a_7
    day_shifts                      M   J   S   ...
    night_shifts                    N   ...
    off_shifts                      Jca Repos   ...
    week_days                       L   Ma  Me  J   V   S   D
    week_indices                    0   1   2   3   4   5   6
    s                               Ns0 Ns1 Ns2 Ns3 Ns4 Ns5 Ns6     ts  cs  Ds  <bDs>
    s'                              Ns'0    ...     ...     Ns'6    ts' cs' Ds' <bDs'>
    s''                             Ns''0   ...     ...     Ns''6   ts''    ...
    ...                             ...                     ...     ...
    sn                              Nsn0    ...      ...    Nsn6    tsn     ...

Notes: 
- *N*[*s*,*j*] : the need of health employees for the shift *s* at the day *j* of a week
- *t*[*s*] : the beginning time of the shift *s*
- *c*[*s*] : the completion time of the shift *s*
- *D*[*s*] : the duration of the shift *s*
- *bD*[*s*] : the break duration in the shift *s*
