"""
This test looks at the arrivals entering the system and checks
that they are being generated according to the specified distributions.

"""

def test_arrival_processes(results_df,config):

    # Takes in the results dataframe from a model run and checks for each patient type
    # that the number of arrivals is roughly equal to what we would expect 
    expected_iat_dict = {}
    for referral, referral_value in config.referral_dist.items():
        for age_group, age_value in config.age_dist.items():
            expected_iat_dict[f"{age_group}_{referral}"] = config.arrival_rate / (
                age_value * referral_value
            )
    
    observed_iat_dict = {}
    for referral, referral_value in config.referral_dist.items():
        for age_group, age_value in config.age_dist.items():
            inds = results_df.index[(results_df['age_group'] == age_group) & (results_df['referral_type'] == referral)].tolist()
            observed_iat_dict[f"{age_group}_{referral}"] = float(1 / results_df.loc[inds, "entry_time"].mean())

    return {key: expected_iat_dict[key] - observed_iat_dict[key] for key in expected_iat_dict if key in observed_iat_dict}