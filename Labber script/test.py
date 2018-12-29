import os
import sys
import time
import numpy as np
import traceback

import Labber
from Labber import ScriptTools

import fitting


def print_exception():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback,
                              file=sys.stdout)


def main():
    ATS_var = 'AlazarTech Signal Demodulator - Channel A - Average demodulated value'
    readout_freq_var = 'readout - Frequency'
    readout_power_var = 'readout - Power'

    # set path to executable
    ScriptTools.setExePath(r'C:\Program Files (x86)\Labber\Program')

    test_path = r'E:\Data\2018\05\Data_0531'

    filename_sfx = time.strftime('%m_%d_%H_%M_%S', time.localtime())

    test_meas = os.path.join(test_path,
                             'test no hardware loop_config.hdf5')
    test_out = os.path.join(test_path,
                            'test no hardware loop_%s.hdf5' % filename_sfx)

    fitting_out = os.path.join(test_path,
                               'fit_parameters_%s' % filename_sfx)
    fits_out = Labber.createLogFile_ForData(fitting_out,
                                            [{'name': 'Power', 'unit': 'dBm'},
                                             {'name': 'Frequency', 'unit': 'Hz'},
                                             {'name': 'Frequency Error', 'unit': 'Hz'},
                                             {'name': 'FWHM', 'unit': 'Hz'},
                                             {'name': 'FWHM Error', 'unit': 'Hz'}])

    # define measurement objects
    test = ScriptTools.MeasurementObject(test_meas, test_out)
    test.setMasterChannel(readout_power_var)

    pows = np.linspace(8, 10, 2)

    # go through list of points
    for idx, pr in enumerate(pows):
        print('\nFreq point number: %d (out of %d points).'
              % ((idx + 1), pows.size))
        print('Current Power: %.2f dBm.' % pr)

        ### TEST ###
        # set power
        test.updateValue(readout_power_var, pr)

        # find qubit
        print('Test in progress...')
        t_test = time.clock()
        (freqs, _) = test.performMeasurement()
        print('Test measurement time: %.1f s.'
              % (time.clock() - t_test))

        # fit spectrum
        test_in = Labber.LogFile(test_out)
        # last_entry = test_in.getEntry(-1)
        # refls = last_entry[ATS_var]
        refls = test_in.getData(ATS_var)[0]
        print('Fitting to Lorentzian...')
        try:
            fit = fitting.lorentzian_fit(freqs, refls)
            (freq, freq_err) = fit[0]
            (FWHM, FWHM_err) = fit[1]
            print('Cavity frequency: %.4f +/- %.4f GHz.'
                  % (1.e-9 * freq, 1.e-9 * freq_err))
            print('Cavity FWHM: %.4f +/- %.4f GHz.'
                  % (1.e-9 * FWHM, 1.e-9 * FWHM_err))
        except:
            print_exception()
            continue

        # save fit data
        fits_out.addEntry({'Power': np.array([pr]),
                           'Frequency': np.array([freq]),
                           'Frequency Error': np.array([freq_err]),
                           'FWHM': np.array([FWHM]),
                           'FWHM Error': np.array([FWHM_err])})


if __name__ == '__main__':
    main()
