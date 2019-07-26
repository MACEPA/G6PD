class MosaicMetadata:
    def __init__(self, input_dir, fsc_filt, ssc_filt,
                 fl1, fsc, ssc, amplification,
                 min_peak_size):
        """
        :param input_dir: Directory containing all FCS files
        :param fsc_filt: FSC gate
        :param ssc_filt: SSC gate
        :param fl1: FL1 channel name
        :param fsc: FSC channel name
        :param ssc: SSC channel name
        :param amplification: Linear vs Log, default False (linear)
        :param min_peak_size: Minimum peak size to keep
        """
        self.input_dir = input_dir
        self.fsc_filt = fsc_filt
        self.ssc_filt = ssc_filt
        self.fl1 = fl1
        self.fsc = fsc
        self.ssc = ssc
        self.amplification = amplification
        self.min_peak_size = min_peak_size


class MosaicOutputs:
    def __init__(self, x_vals, y_vals, intensity, frequency,
                 bc_percent, mean_fitc, median_fitc, sd_fitc):
        self.x_vals = x_vals
        self.y_vals = y_vals
        self.intensity = intensity
        self.frequency = frequency
        self.bc_percent = bc_percent
        self.mean_fitc = mean_fitc
        self.median_fitc = median_fitc
        self.sd_fitc = sd_fitc

