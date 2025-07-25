from experiment import Experiment
from run_experiment import single_run


def main():
    experiment = Experiment()
    results = single_run(experiment)
    print(results)


if __name__ == "__main__":
    main()
