import xlwings as xw
import numpy as np

# default mean inter-arrival times(exp)
age_dist = xw.Book("data/Renal Modelling Input File.xlsx").sheets["age_dist"]
referral_dist = xw.Book("data/Renal Modelling Input File.xlsx").sheets["referral_dist"]
IAT_1_EARLY = 1 / (age_dist.range("B1").value * referral_dist.range("B1").value)
IAT_2_EARLY = 1 / (age_dist.range("B2").value * referral_dist.range("B1").value)
IAT_3_EARLY = 1 / (age_dist.range("B3").value * referral_dist.range("B1").value)
IAT_4_EARLY = 1 / (age_dist.range("B4").value * referral_dist.range("B1").value)
IAT_5_EARLY = 1 / (age_dist.range("B5").value * referral_dist.range("B1").value)
IAT_6_EARLY = 1 / (age_dist.range("B6").value * referral_dist.range("B1").value)
IAT_1_LATE = 1 / (age_dist.range("B1").value * referral_dist.range("B2").value)
IAT_2_LATE = 1 / (age_dist.range("B2").value * referral_dist.range("B2").value)
IAT_3_LATE = 1 / (age_dist.range("B3").value * referral_dist.range("B2").value)
IAT_4_LATE = 1 / (age_dist.range("B4").value * referral_dist.range("B2").value)
IAT_5_LATE = 1 / (age_dist.range("B5").value * referral_dist.range("B2").value)
IAT_6_LATE = 1 / (age_dist.range("B6").value * referral_dist.range("B2").value)


class Exponential:
    """
    Convenience class for the exponential distribution.
    packages up distribution parameters, seed and random generator.
    """

    def __init__(self, mean, random_seed=None):
        """
        Constructor

        Params:
        ------
        mean: float
            The mean of the exponential distribution

        random_seed: int| SeedSequence, optional (default=None)
            A random seed to reproduce samples.  If set to none then a unique
            sample is created.
        """
        self.rand = np.random.default_rng(seed=random_seed)
        self.mean = mean

    def sample(self, size=None):
        """
        Generate a sample from the exponential distribution

        Params:
        -------
        size: int, optional (default=None)
            the number of samples to return.  If size=None then a single
            sample is returned.

        Returns:
        -------
        float or np.ndarray (if size >=1)
        """
        return self.rand.exponential(self.mean, size=size)
