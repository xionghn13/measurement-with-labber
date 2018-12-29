import sys
import traceback
import numpy as np
from scipy.optimize import curve_fit, least_squares


def lorentzian(x, a, b, c, d):
    return a / np.sqrt((x - b) ** 2. + c ** 2. / 4.) + d


def lorentzian_fit(x, y):
    y = np.unwrap(np.angle(y))
    median_y = np.median(y)
    max_x = np.max(x)
    min_x = np.min(x)
    max_y = np.max(y)
    min_y = np.min(y)
    if max_y - median_y >= median_y - min_y:
        d0 = min_y
        idx = np.argmax(y)
    else:
        d0 = max_y
        idx = np.argmin(y)
    b0 = x[idx]
    if idx == 0:
        idx += 1
    elif idx == x.size - 1:
        idx -= 1
    c0 = min([5. * np.abs(x[idx + 1] - x[idx - 1]), max_x - min_x])
    a0 = (y[idx] - d0) * c0 / 2.
    p0 = [a0, b0, c0, d0]
    bounds = ([-10. * np.abs(a0), min_x, c0 / 100., min_y],
              [10. * np.abs(a0), max_x, min([max_x - min_x, c0]), max_y])
    popt, pcov = curve_fit(lorentzian, x, y, p0=p0, bounds=bounds)
    perr = np.sqrt(np.diag(pcov))

    return ((popt[1], perr[1]), (popt[2], perr[2]))


def decaying_oscillations(x, a, b, c, d, e):
    return a * np.exp(-x / b) * np.cos(2. * np.pi * (x - d) / e) + c


def decaying_oscillations_residual(p, x, y):
    (a, b, c, d, e) = p
    return decaying_oscillations(x, a, b, c, d, e) - y


def decaying_oscillations_fit(x, y):
    y = np.unwrap(np.angle(y))
    half = .5 * (np.max(y) + np.min(y))
    period = 2. * np.abs(x[np.argmax(y)] - x[np.argmin(y)])
    guess = [y[0] - y[-1], max(x) - min(x), y[-1], 0., period]
    try:
        popt, pcov = curve_fit(decaying_oscillations, x, y, guess)
        perr = np.sqrt(np.abs(np.diag(pcov)))
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_exception(exc_type, exc_value, exc_traceback,
                                  file=sys.stdout)
        res_robust = least_squares(decaying_oscillations_residual, guess,
                                   loss='soft_l1', f_scale=0.1, args=(x, y))
        popt = res_robust.x
        perr = [np.nan] * 5

    pi_opt = np.abs(.5 * popt[4] + popt[3])
    pi_err = np.abs(np.hypot(perr[4] / 2., perr[3]))

    return ((pi_opt, pi_err), (np.abs(popt[4]), np.abs(perr[4])), (popt[1], perr[1]))


def decaying_exponent(x, a, b, c):
    return a * np.exp(-x / b) + c


def decaying_exponent_fit(x, y):
    y = np.unwrap(np.angle(y))
    half = .5 * (np.max(y) + np.min(y))
    if y[0] > y[-1]:
        b_guess = x[np.argmax(y < half)]
    else:
        b_guess = x[np.argmax(y > half)]
    if b_guess == 0:
        b_guess = .5 * (x[0] + x[-1])
    guess = [y[0] - y[-1], b_guess, y[-1]]

    popt, pcov = curve_fit(decaying_exponent, x, y, guess)
    perr = np.sqrt(np.abs(np.diag(pcov)))

    return ((popt[1], perr[1])),