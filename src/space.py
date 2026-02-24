"""
space.py — Space-to-Earth Wireless Power Transmission Physics
Aether Sim | Space Mode Module

Supports LEO (200-2000 km), MEO (2000-35786 km), GEO (35786 km).

Key physics differences vs ground-to-ground:
  1. FSPL over full orbital distance
  2. Atmospheric attenuation only over ~10-20 km effective atmospheric path (zenith)
  3. Ionospheric effects for microwave below ~3 GHz (not significant at 5.8 GHz)
  4. Orbital geometry: zenith vs off-zenith angle affects atmospheric path length
  5. Space thermal environment (no thermal noise from surroundings)
  6. No ground-level turbulence sources for space-to-ground (turbulence concentrated in lower atmosphere)

Real-world anchors:
  - NRL PRAM (2021): 10W laser from ISS (408 km LEO)
  - JAXA SSPS concept: 1 GW at GEO → 1 GW on ground (theoretical)
  - Caltech MAPLE (2023): first in-space WPT demonstration, 100 mW at LEO
  - DARPA NOM4D: on-orbit assembly for large aperture WPT
  - ESA SOLARIS: proposed 2 GW GEO microwave WPT by 2040
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional

C = 2.998e8  # m/s

# Orbit definitions
ORBIT_PRESETS = {
    "iss_leo":   {"altitude_km": 408,    "name": "ISS / Low Earth Orbit"},
    "leo":       {"altitude_km": 600,    "name": "Standard LEO"},
    "meo":       {"altitude_km": 10000,  "name": "Medium Earth Orbit"},
    "geo":       {"altitude_km": 35786,  "name": "Geostationary (GEO)"},
    "custom":    {"altitude_km": None,   "name": "Custom altitude"},
}

# Effective atmospheric path length at zenith for each loss mechanism
ATMOSPHERIC_DEPTH_KM = 10.0   # troposphere effective depth for rain/clouds
TOTAL_ATMOSPHERE_KM  = 100.0  # for gaseous absorption (full column)

# Microwave frequency
MW_FREQ_GHZ = 5.8
MW_LAMBDA = C / (MW_FREQ_GHZ * 1e9)

# Validated rain attenuation at 5.8 GHz (ITU-R P.838-3) — same as ground
RAIN_ATT_DB_KM = {"clear": 0.0, "haze": 0.0, "rain": 0.437, "smoke": 0.0, "fog": 0.0}
GASEOUS_ABS_DB_KM = 0.005  # negligible at 5.8 GHz

# Laser atmospheric extinction at 1070 nm — same coefficients as ground
LASER_EXT_DB_KM = {
    "clear": 0.05,
    "haze":  1.0,
    "rain":  0.2,
    "smoke": 8.0,
    "fog":   20.0,  # hard block
}
FOG_HARD_BLOCK = {"fog"}


@dataclass
class SpaceTransmitter:
    """Space-based WPT transmitter — microwave or laser."""
    mode: str                    # "microwave" or "laser"
    altitude_km: float           # orbital altitude in km
    # Microwave params
    mw_array_diameter_m: float = 1000.0    # TX aperture diameter (JAXA concept: 2.6km)
    mw_freq_ghz: float = 5.8
    mw_pa_eff: float = 0.55      # GaN PA efficiency (space-rated, slightly lower than ground)
    # Laser params
    laser_aperture_m: float = 2.0          # telescope primary mirror diameter
    laser_wavelength_nm: float = 1070.0
    laser_wall_plug_eff: float = 0.40      # Yb:fiber laser
    laser_m2: float = 1.2                  # beam quality


@dataclass
class SpaceReceiver:
    """Ground-based WPT receiver."""
    mode: str
    # Microwave
    mw_rectenna_area_m2: float = 1e6       # 1 km² (realistic for GEO concept)
    mw_rectenna_eff: float = 0.85
    # Laser
    laser_pv_aperture_m: float = 10.0      # receiver telescope/mirror diameter
    laser_pv_eff: float = 0.45             # InP cells, space-grade illumination
    laser_pv_temp_derating: float = 0.90   # less thermal issue in space-to-ground


def fspl_db(range_m: float, freq_hz: float) -> float:
    lam = C / freq_hz
    return 20 * np.log10(4 * np.pi * range_m / lam)


def atmospheric_path_km(altitude_km: float, zenith_angle_deg: float = 0.0) -> float:
    """Effective atmospheric path length accounting for zenith angle."""
    cos_z = np.cos(np.radians(zenith_angle_deg))
    return ATMOSPHERIC_DEPTH_KM / max(cos_z, 0.1)  # cap at near-horizon


def compute_space_link(
    tx: SpaceTransmitter,
    rx: SpaceReceiver,
    condition: str = "clear",
    target_power_w: float = 1000.0,
    zenith_angle_deg: float = 0.0,
) -> dict:
    """
    Compute space-to-earth WPT link budget.
    Returns full result dict compatible with scenarios.py output format.
    """
    range_m = tx.altitude_km * 1000.0
    atmo_km = atmospheric_path_km(tx.altitude_km, zenith_angle_deg)

    if tx.mode == "microwave":
        return _compute_space_microwave(tx, rx, condition, target_power_w, range_m, atmo_km)
    elif tx.mode == "laser":
        return _compute_space_laser(tx, rx, condition, target_power_w, range_m, atmo_km)
    else:
        raise ValueError(f"Unknown space mode: {tx.mode}")


def _compute_space_microwave(tx, rx, condition, target_power_w, range_m, atmo_km):
    freq_hz = tx.mw_freq_ghz * 1e9
    lam = C / freq_hz

    # TX array gain (circular aperture)
    A_tx = np.pi * (tx.mw_array_diameter_m / 2) ** 2
    eta_ap = 0.7
    G_tx = eta_ap * (4 * np.pi / lam**2) * A_tx
    G_tx_db = 10 * np.log10(G_tx)

    # Beam radius at ground
    beam_radius_m = 0.5 * 1.22 * lam * range_m / (tx.mw_array_diameter_m / 2)
    beam_area_m2 = np.pi * beam_radius_m**2

    # FSPL
    fspl = fspl_db(range_m, freq_hz)

    # Atmospheric attenuation (only through atmosphere, not full orbit)
    rain_att = RAIN_ATT_DB_KM.get(condition, 0) * atmo_km
    gaseous  = GASEOUS_ABS_DB_KM * 100.0  # full atmosphere column
    atmo_db  = rain_att + gaseous

    # RX gain
    G_rx = eta_ap * (4 * np.pi / lam**2) * rx.mw_rectenna_area_m2
    G_rx_db = 10 * np.log10(G_rx)

    # Total link gain
    link_gain_db = G_tx_db + G_rx_db - fspl - atmo_db
    link_gain_linear = 10 ** (link_gain_db / 10)

    # Rectenna RF-to-DC conversion (power-density dependent)
    rx_rf_w_per_1w_tx = link_gain_linear  # RF at receiver per 1W TX RF
    # Use 85% rectenna eff if power density is high enough
    rectenna_eff = 0.85 if rx_rf_w_per_1w_tx * target_power_w > 2.0 else 0.70

    # DC per watt of RF input
    dc_per_rf_w = link_gain_linear * rectenna_eff

    # Required RF power
    required_rf_w = target_power_w / max(dc_per_rf_w, 1e-12)
    required_rf_w = min(required_rf_w, 5e9)  # 5 GW cap (GEO scale)

    # Wall-plug input
    elec_input_w = required_rf_w / tx.mw_pa_eff

    # Actual DC delivered
    dc_delivered_w = required_rf_w * link_gain_linear * rectenna_eff

    # System overhead
    system_overhead = 0.65
    dc_delivered_w *= system_overhead

    system_eff_pct = min((dc_delivered_w / elec_input_w) * 100, 35.0)
    dc_delivered_kw = dc_delivered_w / 1000.0
    elec_input_kw = elec_input_w / 1000.0

    # Hardware sizing — Elements: area / (0.5λ)²
    element_spacing = 0.5 * lam
    n_elements = int(A_tx / element_spacing**2)

    return {
        "mode": "space_microwave",
        "orbit": f"{tx.altitude_km:.0f} km",
        "dc_power_delivered_kw": round(dc_delivered_kw, 3),
        "electrical_input_kw": round(elec_input_kw, 1),
        "system_efficiency_pct": round(system_eff_pct, 2),
        "beam_radius_at_ground_m": round(beam_radius_m, 0),
        "required_hardware": {
            "type": "Space microwave array",
            "orbital_altitude_km": tx.altitude_km,
            "tx_array_diameter_m": tx.mw_array_diameter_m,
            "tx_array_area_m2": round(A_tx, 0),
            "n_elements_approx": f"~{n_elements:,}",
            "tx_array_gain_dbi": round(G_tx_db, 1),
            "beam_radius_at_ground_m": round(beam_radius_m, 1),
            "required_rx_area_m2": round(rx.mw_rectenna_area_m2, 0),
            "required_rf_power_gw": round(required_rf_w / 1e9, 3),
            "fspl_db": round(fspl, 1),
            "atmo_loss_db": round(atmo_db, 2),
        },
        "link_budget": {
            "tx_gain_dbi": round(G_tx_db, 1),
            "fspl_db": round(fspl, 1),
            "atmo_loss_db": round(atmo_db, 2),
            "rx_gain_dbi": round(G_rx_db, 1),
            "link_gain_db": round(link_gain_db, 1),
        },
        "context": {
            "note": (
                f"GEO microwave WPT requires a {tx.mw_array_diameter_m:.0f}m TX array and "
                f"{rx.mw_rectenna_area_m2/1e6:.1f} km² rectenna. "
                f"This is the JAXA/ESA SOLARIS scale infrastructure."
            ),
            "jaxa_ssps_ref": "JAXA SSPS: 2.6 km TX array at GEO → 1 GW delivered with ~3.5 km² rectenna",
            "caltech_maple_ref": "Caltech MAPLE (2023): first in-space WPT demo, 100 mW at LEO",
        },
    }


def _compute_space_laser(tx, rx, condition, target_power_w, range_m, atmo_km):
    lam = tx.laser_wavelength_nm * 1e-9

    # Beam quality factor
    M2 = tx.laser_m2

    # Rayleigh range
    w0 = tx.laser_aperture_m / 2.0  # beam waist = aperture radius
    z_R = np.pi * w0**2 / (M2 * lam)

    # Beam radius at ground
    w_R = w0 * np.sqrt(1 + (range_m / z_R)**2)

    # Geometric collection efficiency
    r_rx = rx.laser_pv_aperture_m / 2.0
    eta_geo = 1.0 - np.exp(-2 * (r_rx / w_R)**2)
    geo_db = -10 * np.log10(max(eta_geo, 1e-10))

    # Atmospheric attenuation — only through atmosphere (10-20 km), not full orbit
    ext_db_km = LASER_EXT_DB_KM.get(condition, 0.05)
    if condition in FOG_HARD_BLOCK:
        return {
            "mode": "space_laser",
            "orbit": f"{tx.altitude_km:.0f} km",
            "dc_power_delivered_kw": 0.0,
            "electrical_input_kw": 0.0,
            "system_efficiency_pct": 0.0,
            "beam_radius_at_ground_m": round(w_R, 2),
            "error": "FOG_HARD_BLOCK: cloud/fog layer blocks laser transmission",
            "context": {
                "note": "Fog/clouds block laser WPT entirely. Use microwave or wait for clear conditions."
            },
        }

    atmo_db = ext_db_km * atmo_km  # only atmospheric depth, not full orbital range
    atmo_factor = 10 ** (-atmo_db / 10)

    # Turbulence (lower for space-to-ground: mainly lower atmosphere)
    # Cn² for ground layer (worst case): 1e-14 m^(-2/3)
    Cn2 = 1e-15  # weaker turbulence for downward path (less boundary layer)
    k = 2 * np.pi / lam
    rytov_var = 1.23 * Cn2 * k**(7/6) * range_m**(11/6)
    # Scintillation factor — milder for downward path
    scintillation_factor = np.exp(-0.5 * min(rytov_var, 2.0))

    # PV receiver efficiency
    pv_eff = rx.laser_pv_eff * rx.laser_pv_temp_derating
    dc_dc_eff = 0.95

    # Combined efficiency per optical watt at transmitter
    eta_total = eta_geo * atmo_factor * scintillation_factor * pv_eff * dc_dc_eff

    # Wall-plug chain
    optical_per_electric = tx.laser_wall_plug_eff
    system_eff = optical_per_electric * eta_total * 0.70  # overhead factor
    system_eff = min(system_eff, 0.35)

    # Power sizing
    elec_input_w = target_power_w / max(system_eff, 1e-10)
    elec_input_w = min(elec_input_w, 1e9)  # 1 GW cap
    optical_power_w = elec_input_w * optical_per_electric
    dc_delivered_w = elec_input_w * system_eff

    return {
        "mode": "space_laser",
        "orbit": f"{tx.altitude_km:.0f} km",
        "dc_power_delivered_kw": round(dc_delivered_w / 1000, 3),
        "electrical_input_kw": round(elec_input_w / 1000, 1),
        "system_efficiency_pct": round(system_eff * 100, 2),
        "beam_radius_at_ground_m": round(w_R, 2),
        "required_hardware": {
            "type": "Space laser (orbital)",
            "orbital_altitude_km": tx.altitude_km,
            "laser_aperture_m": tx.laser_aperture_m,
            "beam_radius_at_ground_m": round(w_R, 2),
            "optical_power_kw": round(optical_power_w / 1000, 1),
            "wall_plug_input_kw": round(elec_input_w / 1000, 1),
            "rx_aperture_m": rx.laser_pv_aperture_m,
            "geometric_capture_pct": round(eta_geo * 100, 3),
            "atmo_loss_db": round(atmo_db, 2),
        },
        "link_budget": {
            "wall_plug_to_photon_db": round(-10 * np.log10(optical_per_electric), 1),
            "geometric_capture_db": round(geo_db, 1),
            "atmospheric_loss_db": round(atmo_db, 2),
            "turbulence_db": round(-10 * np.log10(max(scintillation_factor, 1e-10)), 2),
            "pv_efficiency_db": round(-10 * np.log10(pv_eff), 1),
        },
        "context": {
            "rayleigh_range_km": round(z_R / 1000, 1),
            "nrl_pram_ref": "NRL PRAM (2021): 10W from ISS at 408 km LEO",
            "caltech_maple_ref": "Caltech MAPLE (2023): first in-space WPT, 100 mW",
            "darpa_nom4d_ref": "DARPA NOM4D: on-orbit assembly for large-aperture WPT",
            "note": (
                f"At {tx.altitude_km:.0f} km, a {tx.laser_aperture_m:.1f}m aperture produces a "
                f"{w_R:.1f}m beam radius at ground. "
                f"Receiver captures {eta_geo*100:.3f}% of beam."
            ),
        },
    }
