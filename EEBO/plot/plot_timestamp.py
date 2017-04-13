

def dates_to_dayXmonth(self, df_in, z_in):
        
        # http://stackoverflow.com/questions/31613018/datetime64ns-to-timestamp-string-in-pandas
        dates = pd.DatetimeIndex(df_in['Date']).to_native_types()
        
        # (1.1) List of months for all item in dates 
        months = np.array([datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%m')
                           for date in dates])
        
        # (1.2) Find indices of first day of the months
        _, ind_tmp = np.unique(months, return_index=True)  # -> array([90,212,31,0, ...])
        the_months_ind = np.sort(ind_tmp).tolist()  # -> array([0,31,59,90, ...])
    
        # (1*) Use these indices to make list months' name
        the_months = months[the_months_ind].astype(np.int)
        N_the_months = len(the_months)  # 8 months, in our case, from Jan to Aug
        
        # (2*) Make list of days of the month 
        N_the_days = 31
        the_days = np.arange(1, N_the_days + 1)  # [1, ..., 31]
    
        # (3.1) Make tmp array filled with NaNs
        Z_tmp = np.empty((N_the_days, N_the_months))
        Z_tmp.fill(np.nan)
    
        # (3.2) Make list of indices to fill in Z_tmp month by month
        fill_i = the_months_ind + [len(months)]
    
        # (3.3) Loop through months
        for i in range(N_the_months):
            i0 = fill_i[i]  # get start
            i1 = fill_i[i + 1]  #  and end index
            delta_i = i1 - i0  # compute their difference (either 30,31 or 28)
            Z_tmp[0:delta_i, i] = z_in[i0:i1]  # fill in rows of 
    
        # (3*) Copy tmp array to output variable
        Z = Z_tmp
    
        return (the_months, the_days, Z)  # output coordinates for our plot