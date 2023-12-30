import numpy as np
import pyedflib

def split_edf_by_annotations(edf_file, start_times, durations, events):
    # read edf file
    with pyedflib.EdfReader(edf_file) as edf:
        signals = []
        for i in range(edf.signals_in_file):
            signals.append(edf.readSignal(i))

        # results
        split_signals = []

        for start_time, duration, event in tuple(start_times, durations, events):
            start_sample = int(start_time * edf.getSampleFrequency(0))
            end_sample = start_sample + int(duration * edf.getSampleFrequency(0))

            
            event_signals = []
            for signal in signals:
                split_signal = signal[start_sample:end_sample]
                event_signals.append(split_signal)

            split_signals.append((event, event_signals))

        return split_signals

