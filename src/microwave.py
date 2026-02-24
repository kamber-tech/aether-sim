"""
microwave.py - Microwave/RF beam physics engine
Hummingbird Sim | Microwave Wireless Power Transmission Module

Sources:
  - Friis transmission: Friis 1946 Proc. IRE + Balanis "Antenna Theory" 4th ed.
  - Phased array gain: Balanis Ch. 6 (G = 4π*Ae/λ²)
  - ITU-R P.676-12: atmospheric gaseous absorption (0.003–0.008 dB/km at 5.8 GHz)
  - Rain attenuation: ITU-R P.838-3, validated values (2025):
      10 mm/hr → 0.07 dB/km, 25 mm/hr → 0.22 dB/km,
      50 mm/hr → 0.44 dB/km, 100 mm/hr → 0.97 dB/km
  - Rectenna efficiency: ScienceDirect 2020 (GaN, power-density dependent):
      ≥2W: 85%, 100–500 mW: 72–80%, 25–100 mW: 60–70%, <25 mW: 52–60%
  - Real-world ceiling: JAXA 2021 demo ~22% end-to-end
  - Power density limits: IEEE C95.1-2019 / ICNIRP
  - Ruze's equation: Ruze 1966 Proc. IEEE (phase error loss)
  - Pointing error: Balanis "Antenna Theory" 4th ed. Ch. 6
"""

import numpy as np
from dataclasses import dataclass
from typing import Optional

# ── Physical constants ─────────────────────────────────────────────────────
C_LIGHT = 2.998e8       # m/s

# ── Frequency bands for WPT ───────────────────────────────────────────────
WPT_FREQUENCIES = {
    "2.45_GHz": 2.45e9,   # ISM band, legacy SPS studies
    "5.8_GHz":  5.80e9,   # ISM, preferred for WPT (smaller apertures, better rectenna efficiency)
    "24_GHz":   24.0e9,   # mm-wave (smaller aperture but higher rain loss)
}

# ── Atmospheric gaseous absorption @ key frequencies (dB/km) ─────────────
# Ref: ITU-R P.676-12 (Table 1, sea-level, standard atmosphere)
GASEOUS_ABS_DB_KM = {
    "2.45_GHz":  0.006,   # O2 + H2O absorption, near-negligible
    "5.8_GHz":   0.008,   # slightly higher H2O component
    "24_GHz":    0.10,    # water vapor resonance nearby (22.235 GHz)
}

# ── Rain attenuation coefficients (ITU-R P.838-3) ─────────────────────────
# γ_R = k * R^α  [dB/km] where R = rain rate mm/hr
# Validated values for 5.8 GHz (2025):
#   10 mm/hr → 0.07 dB/km, 25 mm/hr → 0.22 dB/km,
#   50 mm/hr → 0.44 dB/km, 100 mm/hr → 0.97 dB/km
# Best-fit coefficients derived from above anchor points (k=0.00505, α=1.14)
RAIN_K    = {  "2.45_GHz": 0.0000847, "5.8_GHz": 0.00505,  "24_GHz": 0.00488  }
RAIN_ALPHA= {  "2.45_GHz": 1.528,     "5.8_GHz": 1.140,    "24_GHz": 1.195   }

# Rain rates (mm/hr) by condition — aligned with validated anchor points
RAIN_RATE_MM_HR = {
    "clear":         0.0,
    "drizzle":       1.0,    # 1 mm/hr ≈ 0.005 dB/km  — light drizzle
    "light_rain":    10.0,   # 10 mm/hr → 0.07 dB/km  — validated
    "moderate_rain": 25.0,   # 25 mm/hr → 0.22 dB/km  — validated
    "heavy_rain":    50.0,   # 50 mm/hr → 0.44 dB/km  — validated
    "extreme_rain":  100.0,  # 100 mm/hr → 0.97 dB/km — validated
    "fog":           0.1,    # fog is essentially negligible for microwave
}

# ── Condition mapping from frontend strings to microwave rain keys ─────────
CONDITION_MAP_MW = {
    "rain":  "moderate_rain",   # 25 mm/hr → 0.22 dB/km (validated ITU-R P.838-3)
    "haze":  "drizzle",         # 1 mm/hr — haze ≈ light drizzle for microwave
    "smoke": "clear",           # smoke has negligible effect on microwave
    # These pass through unchanged:
    "clear":         "clear",
    "drizzle":       "drizzle",
    "light_rain":    "light_rain",
    "moderate_rain": "moderate_rain",
    "heavy_rain":    "heavy_rain",
    "extreme_rain":  "extreme_rain",
}

# ── Rectenna efficiency at 5.8 GHz — power-density dependent ─────────────
# Ref: ScienceDirect 2020 (GaN high-efficiency rectenna):
#   High power density (≥2W input):    85%
#   Medium (100–500 mW):               72–80% (use 76%)
#   Low (25–100 mW):                   60–70% (use 65%)
#   Very low (<25 mW):                 52–60% (use 56%)
# This function replaces the flat constant table.
def rectenna_efficiency_by_power(received_rf_power_w: float) -> float:
    """
    GaN rectenna efficiency as a function of actual received RF power.
    Source: ScienceDirect 2020 (power-density dependent curve at 5.8 GHz).
    """
    if received_rf_power_w >= 2.0:
        return 0.85    # high power: 85%
    elif received_rf_power_w >= 0.1:
        # Interpolate between 2W (85%) and 100mW (76%)
        t = (received_rf_power_w - 0.1) / (2.0 - 0.1)
        return 0.76 + t * (0.85 - 0.76)
    elif received_rf_power_w >= 0.025:
        # Interpolate between 100mW (76%) and 25mW (65%)
        t = (received_rf_power_w - 0.025) / (0.1 - 0.025)
        return 0.65 + t * (0.76 - 0.65)
    else:
        # Very low power: interpolate down to 52% at 0 W
        t = received_rf_power_w / 0.025
        return 0.52 + t * (0.65 - 0.52)

# Legacy flat-efficiency table (kept for backwards compat, not used in main path)
RECTENNA_EFF = {
    "schottky_class_A": 0.62,
    "schottky_class_E": 0.50,
    "greinacher":       0.40,
    "cmos":             0.30,
}


def normalize_mw_condition(condition: str) -> str:
    """Map any frontend condition string to a valid microwave rain-rate key."""
    return CONDITION_MAP_MW.get(condition, "clear")


@dataclass
class MicrowaveTransmitter:
    """Phased array transmitter parameters."""
    frequency_hz: float = 5.80e9           # operating frequency
    n_elements: int = 1024                 # number of array elements (e.g. 32×32)
    element_spacing_lambda: float = 0.5    # element spacing in wavelengths (0.5λ standard)
    tx_power_per_element_w: float = 5.0    # power per PA element (W)
    pa_efficiency: float = 0.60            # power amplifier efficiency (DC → RF)
    aperture_efficiency: float = 0.70      # accounts for taper, losses, feed network
    wall_plug_efficiency: float = 0.50     # total DC→RF wall-plug (incl. control, cooling)
    side_lobe_level_db: float = -20.0      # first sidelobe relative to main beam (dB)
    frequency_key: str = "5.8_GHz"        # key for atmospheric lookups
    ambient_temp_c: float = 45.0           # ambient operating temperature (°C)


@dataclass
class MicrowaveReceiver:
    """Rectenna array receiver parameters."""
    aperture_area_m2: float = 3.0          # physical receiving aperture area (m²)
    aperture_efficiency: float = 0.85      # effective aperture fraction (incl. fill)
    rectenna_type: str = "schottky_class_E" # rectenna technology
    dc_dc_efficiency: float = 0.95         # output conditioning
    frequency_key: str = "5.8_GHz"


@dataclass
class AtmosphericConditions:
    """Atmospheric conditions for microwave link."""
    condition: str = "clear"               # from RAIN_RATE_MM_HR keys
    custom_rain_rate_mm_hr: Optional[float] = None
    relative_humidity: float = 50.0        # % (affects water vapor absorption)


# ── Core physics ──────────────────────────────────────────────────────────

def wavelength_m(freq_hz: float) -> float:
    """λ = c / f"""
    return C_LIGHT / freq_hz


def array_aperture_area(tx: MicrowaveTransmitter) -> float:
    """
    Physical aperture area of a uniformly-spaced planar array.
    A_phys = N * (d_spacing)²  where d = 0.5λ typical
    """
    lam = wavelength_m(tx.frequency_hz)
    d = tx.element_spacing_lambda * lam
    return tx.n_elements * d**2


def array_gain_dbi(tx: MicrowaveTransmitter) -> float:
    """
    Array directivity/gain (dBi).
    G = 4π * η_ap * A_phys / λ²
    Ref: Balanis Eq. 2-21, aperture antenna theory
    """
    lam = wavelength_m(tx.frequency_hz)
    A = array_aperture_area(tx)
    G_linear = 4 * np.pi * tx.aperture_efficiency * A / lam**2
    return 10 * np.log10(G_linear)


def beam_half_angle_deg(tx: MicrowaveTransmitter) -> float:
    """
    3dB half-beamwidth of a uniform aperture (radians → degrees).
    θ_3dB ≈ 0.886 * λ / D    (for square aperture side D)
    """
    lam = wavelength_m(tx.frequency_hz)
    D = np.sqrt(array_aperture_area(tx))  # side of equivalent square aperture
    theta_rad = 0.886 * lam / D
    return np.degrees(theta_rad)


def spot_radius_at_range(tx: MicrowaveTransmitter, range_m: float) -> float:
    """
    Approximate 3dB beam radius at range z (m).
    r_3dB = tan(θ_3dB) * range ≈ θ_3dB * range  (small angle)
    """
    theta_rad = np.radians(beam_half_angle_deg(tx))
    return theta_rad * range_m


def friis_path_loss_db(range_m: float, freq_hz: float) -> float:
    """
    Free-space path loss (FSPL) in dB.
    FSPL = 20*log10(4π*R/λ)
    Ref: Friis 1946 Proc. IRE
    """
    lam = wavelength_m(freq_hz)
    return 20 * np.log10(4 * np.pi * range_m / lam)


def atmospheric_abs_db(range_km: float, frequency_key: str) -> float:
    """
    Gaseous atmospheric absorption (dB).
    Ref: ITU-R P.676-12 Table 1 at sea level
    """
    alpha = GASEOUS_ABS_DB_KM.get(frequency_key, 0.008)
    return alpha * range_km


def rain_attenuation_db(range_km: float, frequency_key: str, condition: str,
                        custom_rate: Optional[float] = None) -> float:
    """
    Rain attenuation per ITU-R P.838-3.
    γ_R = k * R^α  (dB/km)
    """
    if custom_rate is not None:
        R = custom_rate
    else:
        R = RAIN_RATE_MM_HR.get(condition, 0.0)
    if R <= 0:
        return 0.0
    k = RAIN_K.get(frequency_key, 0.000354)
    a = RAIN_ALPHA.get(frequency_key, 1.451)
    gamma = k * R**a
    return gamma * range_km


def received_power_friis(tx: MicrowaveTransmitter, rx: MicrowaveReceiver,
                         range_m: float, atmosphere: AtmosphericConditions) -> dict:
    """
    Full Friis-based received power calculation with detailed loss budget.
    P_r = P_t * G_t_eff * G_r * (λ/4πR)²  *  T_atmo  *  misc_losses

    New physics (v2):
      - Phase error loss (Ruze's equation): σ_phase = λ/30
      - Pointing/tracking error loss: σ_point = 0.05° RMS
      - Feed network loss: 0.5 dB
      - Atmospheric scintillation: 0.4 dB average
      - Rectenna impedance mismatch: 0.75 dB
      - Temperature derating: 5% PA efficiency drop at 45°C vs 25°C ref

    Returns dict with all intermediate quantities and loss_budget.
    """
    freq = tx.frequency_hz
    lam = wavelength_m(freq)
    range_km = range_m / 1000.0

    # ── TX side ───────────────────────────────────────────────────────────
    total_tx_rf_power = tx.n_elements * tx.tx_power_per_element_w  # RF watts

    # Ideal array gain
    G_t_ideal = 10**(array_gain_dbi(tx) / 10)

    # ── Phase error loss (Ruze's equation) ───────────────────────────────
    # G_actual = G_ideal * exp(-(4π * σ_phase / λ)²)
    # σ_phase = λ/30 (typical for well-calibrated array)
    sigma_phase = lam / 30.0
    phase_error_factor = np.exp(-((4 * np.pi * sigma_phase / lam)**2))
    phase_error_db = -10 * np.log10(phase_error_factor)

    # ── Pointing / tracking error loss ───────────────────────────────────
    # Fraction of beam power captured = exp(-4 * (σ_point / θ_3dB)²)
    sigma_point_deg = 0.05   # 0.05° RMS pointing error
    sigma_point_rad = np.radians(sigma_point_deg)
    theta_3dB_rad   = np.radians(beam_half_angle_deg(tx))
    pointing_factor = np.exp(-4.0 * (sigma_point_rad / theta_3dB_rad)**2)
    pointing_error_db = -10 * np.log10(max(pointing_factor, 1e-10))

    # Effective TX gain after phase and pointing losses
    G_t_eff = G_t_ideal * phase_error_factor * pointing_factor

    # ── Feed network loss ─────────────────────────────────────────────────
    feed_loss_db = 0.5   # dB (corporate feed, typical)
    feed_loss_factor = 10**(-feed_loss_db / 10)

    # ── Temperature derating ──────────────────────────────────────────────
    # PA efficiency drops ~5% at 45°C vs 25°C reference
    temp_ref_c = 25.0
    temp_derating_factor = 1.0 - 0.05 * max(0, (tx.ambient_temp_c - temp_ref_c) / 20.0)
    temp_derating_factor = max(0.5, min(1.0, temp_derating_factor))  # clamp [0.5, 1.0]
    temp_derating_db = -10 * np.log10(temp_derating_factor)

    # Effective TX RF power after feed and temperature losses
    tx_rf_power_eff = total_tx_rf_power * feed_loss_factor * temp_derating_factor

    # ── RX aperture gain ──────────────────────────────────────────────────
    A_rx_eff = rx.aperture_area_m2 * rx.aperture_efficiency
    G_r = 4 * np.pi * A_rx_eff / lam**2

    # ── Free-space path loss ──────────────────────────────────────────────
    fspl_db = friis_path_loss_db(range_m, freq)
    fspl_linear = 10**(fspl_db / 10)

    # ── Atmospheric losses ────────────────────────────────────────────────
    gaseous_abs_db = atmospheric_abs_db(range_km, tx.frequency_key)
    rain_att_db    = rain_attenuation_db(range_km, tx.frequency_key,
                                         atmosphere.condition,
                                         atmosphere.custom_rain_rate_mm_hr)
    atmo_loss_db   = gaseous_abs_db + rain_att_db
    atmo_loss_linear = 10**(atmo_loss_db / 10)

    # ── Atmospheric scintillation ─────────────────────────────────────────
    # Amplitude scintillation from turbulence, ~0.4 dB average at 5.8 GHz over km paths
    scintillation_db = 0.40   # dB
    scintillation_factor = 10**(-scintillation_db / 10)

    # ── Received RF power (Friis) ─────────────────────────────────────────
    P_rf_rx = (tx_rf_power_eff * G_t_eff * G_r /
               (fspl_linear * atmo_loss_linear)) * scintillation_factor

    # Clip at total TX RF (energy conservation)
    P_rf_rx = min(P_rf_rx, total_tx_rf_power * 0.999)

    # ── Rectenna conversion (power-density dependent) ─────────────────────
    # Use GaN power-density curve (ScienceDirect 2020) instead of flat constant
    rect_eff = rectenna_efficiency_by_power(P_rf_rx)

    # Rectenna impedance mismatch loss (additional to rated efficiency)
    mismatch_db     = 0.75   # dB (0.5-1 dB range, midpoint)
    mismatch_factor = 10**(-mismatch_db / 10)

    P_dc_raw = P_rf_rx * rect_eff * mismatch_factor
    P_dc_out = P_dc_raw * rx.dc_dc_efficiency

    # ── Electrical input (wall-plug) ──────────────────────────────────────
    elec_input = total_tx_rf_power / tx.wall_plug_efficiency

    # ── System efficiency — apply real-world overhead + cap ───────────────
    # JAXA 2021 demo: 22% end-to-end. Apply 0.65× overhead factor, cap at 35%.
    SYSTEM_OVERHEAD_FACTOR = 0.65
    MAX_SYSTEM_EFF = 0.35
    physics_eff = P_dc_out / elec_input if elec_input > 0 else 0.0
    sys_eff = min(MAX_SYSTEM_EFF, physics_eff * SYSTEM_OVERHEAD_FACTOR)
    P_dc_out = sys_eff * elec_input  # back-calculate adjusted DC output

    # ── Link budget (dB) ──────────────────────────────────────────────────
    link_db = 10 * np.log10(sys_eff) if sys_eff > 0 else -999.0

    # ── Rayleigh distance (near/far field boundary) ───────────────────────
    aperture_side_m = np.sqrt(array_aperture_area(tx))
    rayleigh_dist_m = 2.0 * aperture_side_m**2 / lam

    # ── Beam capture feasibility ──────────────────────────────────────────
    beam_r = spot_radius_at_range(tx, range_m)
    # Aperture needed to capture 50% of a uniform beam disk
    req_rx_area_for_50pct = np.pi * (0.707 * beam_r)**2
    regime = "near-field" if range_m <= rayleigh_dist_m else "far-field"

    # ── Power density at range (main beam center, W/m²) ───────────────────
    spot_area = np.pi * spot_radius_at_range(tx, range_m)**2
    power_density_w_m2 = P_rf_rx / spot_area if spot_area > 0 else 0.0

    # ── Detailed loss budget ──────────────────────────────────────────────
    wall_plug_db      = -10 * np.log10(tx.wall_plug_efficiency)
    rectenna_eff_db   = -10 * np.log10(rect_eff)
    dc_dc_db          = -10 * np.log10(rx.dc_dc_efficiency)

    loss_budget = {
        "wall_plug_loss_db":          round(wall_plug_db, 2),
        "feed_network_loss_db":       round(feed_loss_db, 2),
        "temperature_derating_db":    round(temp_derating_db, 2),
        "phase_error_loss_db":        round(phase_error_db, 2),
        "pointing_error_loss_db":     round(pointing_error_db, 2),
        "free_space_path_loss_db":    round(fspl_db, 2),
        "gaseous_absorption_db":      round(gaseous_abs_db, 3),
        "rain_attenuation_db":        round(rain_att_db, 3),
        "atmospheric_scintillation_db": round(scintillation_db, 2),
        "rectenna_conversion_loss_db":round(rectenna_eff_db, 2),
        "impedance_mismatch_db":      round(mismatch_db, 2),
        "dc_dc_conditioning_db":      round(dc_dc_db, 2),
        # Gains
        "array_gain_ideal_dbi":       round(10 * np.log10(G_t_ideal), 2),
        "rx_aperture_gain_dbi":       round(10 * np.log10(G_r), 2),
        # Net
        "total_loss_db":              round(-link_db, 2) if sys_eff > 0 else None,
    }

    # ── Factor values (linear) for loss budget display ────────────────────
    loss_fractions = {
        "wall_plug":           round(tx.wall_plug_efficiency, 4),
        "feed_network":        round(feed_loss_factor, 4),
        "temperature_derating":round(temp_derating_factor, 4),
        "phase_error":         round(phase_error_factor, 4),
        "pointing_error":      round(pointing_factor, 4),
        "atmospheric_total":   round(1.0 / atmo_loss_linear, 6),
        "scintillation":       round(scintillation_factor, 4),
        "rectenna_conversion": round(rect_eff, 4),
        "impedance_mismatch":  round(mismatch_factor, 4),
        "dc_dc_conditioning":  round(rx.dc_dc_efficiency, 4),
    }

    return {
        "range_m":               range_m,
        "condition":             atmosphere.condition,
        "electrical_input_w":    elec_input,
        "tx_rf_power_w":         total_tx_rf_power,
        "tx_rf_power_eff_w":     tx_rf_power_eff,
        "array_gain_dbi":        array_gain_dbi(tx),
        "array_gain_eff_db":     10 * np.log10(G_t_eff),
        "rx_gain_dbi":           10 * np.log10(G_r),
        "fspl_db":               fspl_db,
        "atmo_loss_db":          atmo_loss_db,
        "gaseous_abs_db":        gaseous_abs_db,
        "rain_att_db":           rain_att_db,
        "phase_error_db":        phase_error_db,
        "pointing_error_db":     pointing_error_db,
        "feed_loss_db":          feed_loss_db,
        "scintillation_db":      scintillation_db,
        "mismatch_db":           mismatch_db,
        "temp_derating_db":      temp_derating_db,
        "received_rf_power_w":   P_rf_rx,
        "rectenna_eff":          rect_eff,
        "dc_output_w":           P_dc_out,
        "wall_plug_eff":         tx.wall_plug_efficiency,
        "total_system_eff":      sys_eff,
        "link_budget_db":        link_db,
        "beam_radius_m":         spot_radius_at_range(tx, range_m),
        "power_density_w_m2":    power_density_w_m2,
        "power_density_mw_cm2":  power_density_w_m2 / 10,
        "beam_halfangle_deg":    beam_half_angle_deg(tx),
        "loss_budget":           loss_budget,
        "loss_fractions":        loss_fractions,
        "n_elements":            tx.n_elements,
        "total_rf_power_w":      total_tx_rf_power,
        # ── Feasibility / regime fields ───────────────────────────────────
        "rayleigh_distance_m":          round(rayleigh_dist_m, 1),
        "regime":                        regime,
        "beam_radius_at_range_m":        round(beam_r, 1),
        "req_rx_area_50pct_m2":          round(req_rx_area_for_50pct, 1),
        "actual_rx_area_m2":             rx.aperture_area_m2,
        "aperture_capture_fraction":     round(min(1.0, rx.aperture_area_m2 / max(req_rx_area_for_50pct, 0.001)), 4),
        "darpa_prad_anchor":             "800W @ 8.6km achieved in 2025 (DARPA POWER PRAD)",
        "jaxa_mw_anchor":                "22% end-to-end efficiency demonstrated (JAXA 2021)",
    }


def rayleigh_distance_m(tx: MicrowaveTransmitter) -> float:
    """
    Far-field (Fraunhofer) distance: R_ff = 2*D²/λ
    where D is the aperture side length.
    """
    lam = wavelength_m(tx.frequency_hz)
    D = np.sqrt(array_aperture_area(tx))
    return 2.0 * D**2 / lam


def sidelobe_power_density(tx: MicrowaveTransmitter, range_m: float,
                            total_tx_rf_power_w: float) -> float:
    """
    Approximate sidelobe power density at range (W/m²).
    First sidelobe ~ SLL below main beam.
    """
    sl_linear = 10**(tx.side_lobe_level_db / 10)
    G_t_main = 10**(array_gain_dbi(tx) / 10)
    G_sl = G_t_main * sl_linear
    lam = wavelength_m(tx.frequency_hz)
    fspl = (4 * np.pi * range_m / lam)**2
    P_sl = total_tx_rf_power_w * G_sl / fspl
    # Power density (approximate uniform distribution over hemisphere)
    area = 2 * np.pi * range_m**2
    return P_sl / area


def crossover_analysis(range_m: float, condition: str,
                       tx_aperture_m2: float = 10.0,
                       rx_area_m2: float = None) -> dict:
    """
    Compare microwave vs laser efficiency at a given range/condition.
    Returns which mode is better and why.

    Microwave wins: short range, rain/fog/smoke (no laser hazard, all-weather)
    Laser wins:     long range, clear sky (lower divergence)
    """
    if rx_area_m2 is None:
        rx_area_m2 = min(50.0, max(10.0, range_m / 40.0))

    lam = C_LIGHT / 5.8e9
    d = 0.5 * lam
    n_elements = max(64, int(tx_aperture_m2 / d**2))

    condition_norm = normalize_mw_condition(condition)
    tx = MicrowaveTransmitter(n_elements=n_elements, tx_power_per_element_w=10.0)
    rx = MicrowaveReceiver(aperture_area_m2=rx_area_m2)
    atmo = AtmosphericConditions(condition=condition_norm)
    mw_result = received_power_friis(tx, rx, range_m, atmo)
    mw_eff = mw_result["total_system_eff"] * 100

    # Laser crossover estimate using simplified Beer-Lambert model
    # Validated: clear 0.05 dB/km, rain 0.20 dB/km, smoke ~5 dB/km
    from .laser import ATMO_CONDITIONS as LASER_ATMO, FOG_HARD_BLOCK_CONDITIONS
    laser_beta = LASER_ATMO.get(condition, LASER_ATMO.get("clear", 0.0115))
    range_km = range_m / 1000.0
    T_laser = np.exp(-laser_beta * range_km)
    fog_blocked = condition in FOG_HARD_BLOCK_CONDITIONS

    # Simple laser system efficiency estimate (no full Gaussian computation)
    # wall-plug 40%, geometric ~80% at 2km, PV 45% derated, DC-DC 95%
    # Then overhead factor 0.65; this is a rough crossover estimate
    geo_eff_est = min(0.90, 1.0 / (1.0 + (range_km / 5.0)**2))  # rough
    laser_chain_eff = 0.40 * T_laser * geo_eff_est * 0.45 * 0.95
    laser_eff = min(0.35, laser_chain_eff * 0.65) * 100  # overhead + cap
    if fog_blocked:
        laser_eff = 0.0

    if fog_blocked:
        best_mode = "microwave"
        reason = "Fog/cloud is a HARD BLOCK for laser (10–30 dB/km); microwave barely affected (<0.1 dB/km)"
    elif condition in ("smoke",) and range_km >= 1.0:
        best_mode = "microwave"
        reason = "Heavy smoke (~5 dB/km) causes >5 dB laser loss over 1km; microwave penetrates smoke freely"
    elif mw_eff >= laser_eff:
        best_mode = "microwave"
        reason = "Microwave more efficient at this range/condition combination"
    else:
        best_mode = "laser"
        if condition in ("rain", "moderate_rain", "heavy_rain"):
            reason = (
                "Rain is mild for 1070nm laser (0.09–0.35 dB/km validated ITU); "
                "laser wins in rain unless fog/cloud is present"
            )
        elif condition in ("haze",):
            reason = "Haze causes ~1 dB/km for laser but still beats microwave's beam divergence penalty"
        elif range_m > 2000:
            reason = "Laser diverges far less (λ=1070nm vs λ=52mm), much better beam concentration at long range"
        else:
            reason = "Laser more efficient in clear-sky conditions; microwave beam too wide for practical apertures"

    return {
        "range_km":       round(range_km, 2),
        "condition":      condition,
        "microwave_eff_pct": round(mw_eff, 2),
        "laser_eff_pct":    round(laser_eff, 2),
        "best_mode":        best_mode,
        "reason":           reason,
        "mw_rx_area_m2":    rx_area_m2,
        "mw_n_elements":    n_elements,
        "laser_fog_blocked": fog_blocked,
    }


def print_microwave_report(result: dict) -> str:
    """Format a readable microwave link budget report."""
    lb = result.get("loss_budget", {})
    lines = [
        "=" * 65,
        "  MICROWAVE WPT LINK BUDGET REPORT (v2 - Enhanced Physics)",
        "=" * 65,
        f"  Range:              {result['range_m']/1000:.2f} km",
        f"  Condition:          {result['condition']}",
        f"  Elements:           {result.get('n_elements', '?')}",
        "",
        "  ── Power Chain ──────────────────────────────────────────",
        f"  Electrical input:   {result['electrical_input_w']/1000:.2f} kW",
        f"  TX RF power:        {result['tx_rf_power_w']/1000:.2f} kW",
        f"  TX RF (after losses):{result['tx_rf_power_eff_w']/1000:.2f} kW",
        f"  Received RF power:  {result['received_rf_power_w']/1000:.3f} kW",
        f"  DC output:          {result['dc_output_w']/1000:.3f} kW",
        "",
        "  ── Loss Budget (dB) ─────────────────────────────────────",
        f"  Wall-plug loss:    +{lb.get('wall_plug_loss_db', 0):.2f} dB",
        f"  Feed network:      +{lb.get('feed_network_loss_db', 0):.2f} dB",
        f"  Temp derating:     +{lb.get('temperature_derating_db', 0):.2f} dB",
        f"  Phase error (Ruze):+{lb.get('phase_error_loss_db', 0):.2f} dB",
        f"  Pointing error:    +{lb.get('pointing_error_loss_db', 0):.2f} dB",
        f"  FSPL:              +{lb.get('free_space_path_loss_db', 0):.2f} dB",
        f"  Gaseous absorption:+{lb.get('gaseous_absorption_db', 0):.3f} dB",
        f"  Rain attenuation:  +{lb.get('rain_attenuation_db', 0):.3f} dB",
        f"  Scintillation:     +{lb.get('atmospheric_scintillation_db', 0):.2f} dB",
        f"  Rectenna conv:     +{lb.get('rectenna_conversion_loss_db', 0):.2f} dB",
        f"  Impedance mismatch:+{lb.get('impedance_mismatch_db', 0):.2f} dB",
        f"  DC-DC cond.:       +{lb.get('dc_dc_conditioning_db', 0):.2f} dB",
        f"  Array gain:        -{lb.get('array_gain_ideal_dbi', 0):.2f} dBi",
        f"  RX aperture gain:  -{lb.get('rx_aperture_gain_dbi', 0):.2f} dBi",
        "",
        f"  TOTAL system eff:   {result['total_system_eff']*100:.2f}%",
        f"  Link budget:        {result['link_budget_db']:.1f} dB",
        "",
        "  ── Beam Properties ──────────────────────────────────────",
        f"  3dB beam radius:    {result['beam_radius_m']:.1f} m",
        f"  Beam half-angle:    {result['beam_halfangle_deg']:.3f}°",
        "",
        "  ── Safety ───────────────────────────────────────────────",
        f"  Main-beam PD:       {result['power_density_mw_cm2']:.3f} mW/cm²",
        f"  (IEEE C95.1 occ):   10 mW/cm²  (at 5.8 GHz)",
        "=" * 65,
    ]
    return "\n".join(lines)
