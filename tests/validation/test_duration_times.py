from renal_capacity_model.model import Model
from renal_capacity_model.config import Config
import numpy as np
import statistics

## Note ## All variate generation working as expected. Independent check of means of distribution was carried out.


def test_duration_initialisation_ttd(age_group, dialysis_type, config):
    # Generates data from the distributions and provides a mean and variance
    # allows us to check they align with expected values
    data = config.ttd_initial_distribution[dialysis_type][age_group][
        "proportion_uncensored"
    ]
    replications = []
    for _ in range(10000):
        if rng.uniform(0, 1) < data:
            replications.append(1)
        else:
            replications.append(0)
    results = [statistics.mean(replications)]

    params = [
        config.ttd_initial_distribution[dialysis_type][age_group]["shape"],
        config.ttd_initial_distribution[dialysis_type][age_group]["scale"],
    ]
    samples = []
    for _ in range(10000):
        samples.append(params[1] * rng.weibull(params[0]))

    results.append(statistics.mean(samples))
    results.append(statistics.stdev(samples))

    print(
        f"** \n Showing ttd results for age group {age_group} and {dialysis_type}: \n"
    )
    print([data, params])
    print(results)
    return results


def test_duration_initialisation_ttma(age_group, dialysis_type, config):
    # Generates data from the distributions and provides a mean and variance
    # allows us to check they align with expected values
    data = config.ttma_initial_distribution[dialysis_type][age_group][
        "proportion_uncensored"
    ]
    replications = []
    for _ in range(10000):
        if rng.uniform(0, 1) < data:
            replications.append(1)
        else:
            replications.append(0)
    results = [statistics.mean(replications)]

    params = [
        config.ttma_initial_distribution[dialysis_type][age_group]["shape"],
        config.ttma_initial_distribution[dialysis_type][age_group]["scale"],
    ]
    samples = []
    for _ in range(10000):
        samples.append(params[1] * rng.weibull(params[0]))

    results.append(statistics.mean(samples))
    results.append(statistics.stdev(samples))

    print(
        f"** \n Showing ttma results for age group {age_group} and {dialysis_type}: \n"
    )
    print([data, params])
    print(results)
    return results


def test_duration_initialisation_ttd_tx(age_group, tx_type, config):
    # Generates data from the distributions and provides a mean and variance
    # allows us to check they align with expected values
    data = config.ttd_tx_initial_distribution[tx_type][age_group][
        "proportion_uncensored"
    ]
    replications = []
    for _ in range(10000):
        if rng.uniform(0, 1) < data:
            replications.append(1)
        else:
            replications.append(0)
    results = [statistics.mean(replications)]

    params = [
        config.ttd_tx_initial_distribution[tx_type][age_group]["lower_bound"],
        config.ttd_tx_initial_distribution[tx_type][age_group]["upper_bound"],
    ]
    samples = []
    for _ in range(10000):
        samples.append(rng.uniform(params[0], params[1]))

    results.append(statistics.mean(samples))
    results.append(statistics.stdev(samples))

    print(f"** \n Showing ttd results for age group {age_group} and {tx_type}: \n")
    print([data, params])
    print(results)
    return results


def test_duration_initialisation_ttgf_tx(age_group, tx_type, config):
    # Generates data from the distributions and provides a mean and variance
    # allows us to check they align with expected values
    data = config.ttgf_tx_initial_distribution[tx_type][age_group][
        "proportion_uncensored"
    ]
    replications = []
    for _ in range(10000):
        if rng.uniform(0, 1) < data:
            replications.append(1)
        else:
            replications.append(0)
    results = [statistics.mean(replications)]

    params = [
        config.ttgf_tx_initial_distribution[tx_type][age_group]["shape"],
        config.ttgf_tx_initial_distribution[tx_type][age_group]["scale"],
    ]
    samples = []
    for _ in range(10000):
        samples.append(params[1] * rng.weibull(params[0]))

    results.append(statistics.mean(samples))
    results.append(statistics.stdev(samples))

    print(f"** \n Showing ttgf results for age group {age_group} and {tx_type}: \n")
    print([data, params])
    print(results)
    return results


def test_duration_ttd(age_group, dialysis_type, config):
    # Generates data from the distributions and provides a mean and variance
    # allows us to check they align with expected values

    params = [
        config.ttd_distribution[dialysis_type][age_group]["shape"],
        config.ttd_distribution[dialysis_type][age_group]["scale"],
    ]
    samples = []
    for _ in range(10000):
        samples.append(rng.gamma(params[0], params[1]))

    results = []
    results.append(statistics.mean(samples))
    results.append(statistics.stdev(samples))

    print(
        f"** \n Showing ttd results for age group {age_group} and {dialysis_type}: \n"
    )
    print(params)
    print(results)
    return results


def test_duration_ttma(age_group, dialysis_type, config):
    # Generates data from the distributions and provides a mean and variance
    # allows us to check they align with expected values

    results = []

    params = [
        config.ttma_distribution[dialysis_type][age_group]["shape"],
        config.ttma_distribution[dialysis_type][age_group]["scale"],
    ]
    samples = []
    for _ in range(10000):
        samples.append(rng.gamma(params[0], params[1]))

    results.append(statistics.mean(samples))
    results.append(statistics.stdev(samples))

    print(
        f"** \n Showing ttma results for age group {age_group} and {dialysis_type}: \n"
    )
    print(params)
    print(results)
    return results


def test_duration_ttd_tx(age_group, tx_type, config):
    # Generates data from the distributions and provides a mean and variance
    # allows us to check they align with expected values

    results = []

    params = [
        config.ttd_tx_distribution[tx_type][age_group]["shape"],
        config.ttd_tx_distribution[tx_type][age_group]["scale"],
    ]
    samples = []
    for _ in range(10000):
        samples.append(params[1] * rng.weibull(params[0]))

    results.append(statistics.mean(samples))
    results.append(statistics.stdev(samples))

    print(f"** \n Showing ttd results for age group {age_group} and {tx_type}: \n")
    print(params)
    print(results)
    return results


def test_duration_ttgf_tx(age_group, tx_type, config):
    # Generates data from the distributions and provides a mean and variance
    # allows us to check they align with expected values

    results = []

    params = [
        config.ttgf_tx_distribution[tx_type][age_group]["break_point"],
        config.ttgf_tx_distribution[tx_type][age_group]["mode"],
        config.ttgf_tx_distribution[tx_type][age_group]["proportion_below_break"],
        config.ttgf_tx_distribution[tx_type][age_group]["shape"],
        config.ttgf_tx_distribution[tx_type][age_group]["scale"],
    ]

    samples = []
    for _ in range(10000):
        if rng.uniform(0, 1) < params[2]:
            samp = rng.triangular(
                left=0,
                mode=params[1],
                right=params[0],
                size=None,
            )
        else:
            samp = params[0] + params[4] * rng.weibull(
                a=params[3],
                size=None,
            )
        samples.append(samp)

    results.append(statistics.mean(samples))
    results.append(statistics.stdev(samples))

    print(f"** \n Showing ttgf results for age group {age_group} and {tx_type}: \n")
    print(params)
    print(results)
    return results


if __name__ == "__main__":
    config = Config({"sim_duration": 13 * 365, "initialise_prevalent_patients": False})
    rng = np.random.default_rng(config.random_seed)
    model = Model(1, rng, config)
    dialysis_types = ["ichd", "hhd", "pd"]
    tx_types = ["live", "cadaver"]
    age_groups = [1, 2, 3, 4, 5, 6]
    for dialysis_type in dialysis_types:
        for age_group in age_groups:
            # test_duration_initialisation_ttma(age_group, dialysis_type, config)
            # test_duration_initialisation_ttd(age_group, dialysis_type, config)
            # test_duration_ttma(age_group, dialysis_type, config)
            # test_duration_ttd(age_group, dialysis_type, config)
            pass

    for tx_type in tx_types:
        for age_group in age_groups:
            # test_duration_initialisation_ttd_tx(age_group, tx_type, config)
            # test_duration_initialisation_ttgf_tx(age_group, tx_type, config)
            # test_duration_ttd_tx(age_group, tx_type, config)
            # test_duration_ttgf_tx(age_group, tx_type, config)
            pass
