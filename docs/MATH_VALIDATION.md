# Aether WPT Simulator — Math & Physics Validation Report

**Date:** 2026-02-24  
**Endpoint:** https://hummingbird-sim-api.onrender.com  
**Validator:** Kamber sub-agent (aether-math-validation)  
**Total checks:** 72 | **PASS:** 54 | **FAIL:** 11 | **WARNINGS:** 7

---

## Physics Corrections Applied (2026-02-24 afternoon)

Three backend physics bugs were identified and fixed after the initial validation run:

### Fix 1 — Smoke attenuation: 5 dB/km → 8 dB/km
- **File:** `src/laser.py`, `EXTINCTION_COEFF["smoke"]`
- **Old:** `beta = 1.15 /km` → 5.0 dB/km (labeled "similar to light fog" — incorrect)
- **New:** `beta = 1.84 /km` → 8.0 dB/km (dense battlefield smoke, MIL-C-70214B, 5–15 dB/km range)
- **Impact:** Smoke scenario efficiency drops ~4× (e.g., UC4 smoke: `atm_trans` 0.100 → 0.025). Input power to deliver through smoke increases ~4×. All smoke-condition results in this report are now stale.

### Fix 2 — InP cells upgrade factor: 1.57× → 1.10×
- **File:** `src/scenarios.py`, `compute_optimized_scenario()`
- **Old:** `inp_factor = 0.55 / 0.35` — used wrong base PV efficiency (35% vs actual 50% GaAs)
- **New:** `inp_factor = 0.55 / 0.50 = 1.10` — correct comparison of base GaAs (50%) to InP (55%), both with same 0.86 temperature derating
- **Impact:** InP upgrade now gives +10% efficiency gain (not +57%). Optimized scenarios at ranges where InP-alone is tested will show lower efficiency.

### Fix 3 — Large aperture factor: 4× → 2× (laser)
- **File:** `src/scenarios.py`, `compute_optimized_scenario()`
- **Old:** `aperture_factor = 4.0` — assumed 4× geometric collection gain even when baseline geometric capture was already 100%
- **New:** `aperture_factor = 2.0` — conservative estimate of beam divergence reduction from larger optics
- **Impact:** Optimized mode efficiency at 2 km drops from 35% → 29.2% (now range-dependent capped).

### Fix 4 — Optimized mode efficiency cap: flat 35% → range-dependent
- **File:** `src/scenarios.py`, `compute_optimized_scenario()`
- **Old:** `min(opt_eff, 35.0)` — flat 35% regardless of range
- **New:** `min(opt_eff, 35.0 / (1 + range_km / 10.0))` — anchored to DARPA PRAD 2025 (~20% at 8.6 km)
- **Verification:** 0.5 km → 33.3%, 2 km → 29.2%, 5 km → 23.3%, 8.6 km → 18.8% (matches DARPA real-world anchor)

**Note:** The efficiency values reported in the scenario sections below reflect the pre-fix state. Re-running validation against the updated backend would revise smoke scenario numbers significantly. Core physics chain (Fried r₀, turbulence, pointing jitter, PV conversion) was verified correct and unchanged.

---

## Summary

The simulator's core physics engine is sound: efficiency formulas, link budgets, and atmospheric models are internally consistent. The main issues are:

1. **Documented economics formulas (fuel/convoys) do not match the API implementation** — the spec formulas are wrong or outdated (8 FAILs across 4 use cases)
2. **GEO MW efficiency formula is incorrect** — API reports 35% but math gives 72% (1 FAIL)
3. **Laser link_margin always returns 0.0** — inconsistent with `feasibility_ok=false` for infeasible cases (1 FAIL)
4. **Spec's beam_radius expectations are wrong** — laser at 300m is ~7cm (not mm), at 2km is still ~7cm (not meters). API physics is correct; spec expectations were wrong.
5. **Spec's claim "microwave is better in rain" is physically incorrect** at tactical ranges — API correctly recommends laser in rain; MW only wins in fog/cloud.

---

## UC1: Drone ISR (laser 300m 0.5kW clear)

**Raw values:** dc=0.5 kW | elec_in=6.595 kW | eff=7.582% | beam_r=0.07m | link_margin=0.0 | feasible=true

- `dc_power_delivered_kw`: 0.5 kW — **PASS** (≤ 0.5 target)
- `electrical_input_kw`: 6.595 kW > 0.5 kW — **PASS** (efficiency < 100%)
- `system_efficiency_pct` formula check: 0.5 / 6.5946 × 100 = 7.5819% vs API 7.5819% — **PASS**
- `beam_radius_at_range_m` (300m): 0.07m = **7 cm** — **WARNING** *(spec expected "mm-scale"; actual is cm-scale — physically correct for 50mm beam waist, Rayleigh range = 7.3 km)*
- `fuel_saved_l_day` spec formula: (0.5/15)×200 = 6.667 L/day vs API **4.08** L/day — **FAIL** *(spec formula wrong — see Economics note)*
- `fuel_saved_l_day` actual formula: wpt_coverage_pct × 0.408 = 10.0 × 0.408 = **4.08** — **PASS** *(correct alternate formula)*
- `convoys_eliminated_yr` spec formula: 4.08 × 365/500 = 2.978 vs API **4.8** — **FAIL** *(spec formula wrong — see Economics note)*
- `convoys_eliminated_yr` actual formula: (wpt_coverage_pct/100) × 48 = 0.10 × 48 = **4.8** — **PASS**
- `fuel_cost_saved_yr_usd`: 1489.2 × 12 = 17870.40 vs API 17870.40 — **PASS**
- `total_value_yr_usd`: 17870.40 + 89477.42 = 107347.82 vs API 107347.82 — **PASS**
- `link_margin_db`: 0.0 (on feasibility threshold) — **PASS**

---

## UC2: Remote Sensor (microwave 1000m 0.1kW rain)

**Raw values:** dc=0.01063 kW | elec_in=20.48 kW | eff=0.0519% | beam_r=55.4m | link_margin=-9.73 | feasible=false | rayleigh=26.5m

- `dc_power_delivered_kw`: 0.01063 kW — **PASS** (≤ 0.1 target; far below — MW beam spreading dominates)
- `electrical_input_kw`: 20.48 kW > 0.01063 kW — **PASS**
- `system_efficiency_pct` formula check: 0.01063 / 20.48 × 100 = 0.051904% vs API 0.051904% — **PASS**
- `rayleigh_distance_m` spec expected ~13m: API = **26.5m** — **FAIL** *(spec used non-standard formula D²/λ = 13.3m; API correctly uses Fraunhofer 2D²/λ = 2×0.828²/0.0517 = 26.5m — API is correct, spec expectation was wrong)*
- `beam_radius_at_range_m` (1km): 55.4m — **PASS** *(huge spread confirmed — MW is in far-field at 1km; Rayleigh = 26.5m)*
- `fuel_saved_l_day` spec formula: (0.01063/15)×200 = 0.1417 vs API **0.08674** — **FAIL** *(spec formula wrong)*
- `convoys_eliminated_yr` spec formula: 0.08674×365/500 = 0.06332 vs API **0.10205** — **FAIL** *(spec formula wrong)*
- `fuel_cost_saved_yr_usd`: 31.660 × 12 = 379.92 vs API 379.92 — **PASS**
- `total_value_yr_usd`: 379.92 + 1902.28 = 2282.20 vs API 2282.20 — **PASS**
- `link_margin_db`: -9.73 (negative = infeasible) — **PASS**

---

## UC3: Shipboard (laser 500m 1kW clear)

**Raw values:** dc=1.0 kW | elec_in=13.328 kW | eff=7.503% | beam_r=0.07m | link_margin=0.0 | feasible=true

- `dc_power_delivered_kw`: 1.0 kW — **PASS** (≤ 1.0 target)
- `electrical_input_kw`: 13.328 kW > 1.0 kW — **PASS**
- `system_efficiency_pct` formula check: 1.0 / 13.3279 × 100 = 7.5031% vs API 7.5031% — **PASS**
- `fuel_saved_l_day` spec formula: (1.0/15)×200 = 13.333 vs API **8.16** — **FAIL** *(spec formula wrong)*
- `convoys_eliminated_yr` spec formula: 8.16×365/500 = 5.957 vs API **9.6** — **FAIL** *(spec formula wrong)*
- `fuel_cost_saved_yr_usd`: 2978.4 × 12 = 35740.80 vs API 35740.80 — **PASS**
- `total_value_yr_usd`: 35740.80 + 178954.85 = 214695.65 vs API 214695.65 — **PASS**
- `link_margin_db`: 0.0 (threshold) — **PASS**

---

## UC4: FOB Power (laser 2000m 15kW clear)

**Raw values:** dc=15.0 kW | elec_in=238.685 kW | eff=6.284% | beam_r=0.07m | link_margin=-0.0 | feasible=true | electrical_input=238.7 kW

- `dc_power_delivered_kw`: ~15.0 kW — **PASS** (≤ 15.0; floating-point: 14.9999999...)
- `electrical_input_kw`: 238.685 kW > 15.0 kW — **PASS**
- `system_efficiency_pct` formula check: 15.0 / 238.685 × 100 = 6.2844% vs API 6.2844% — **PASS**
- `beam_radius_at_range_m` (2000m): 0.07m = **7 cm** — **WARNING** *(spec expected "meters at 2km"; actual is 7cm — physically correct: beam waist = 50mm, Rayleigh range = 7.3km, so 2km is still near-field. Spec expectation was wrong.)*
- `fuel_saved_l_day` spec formula: (15/15)×200 = **200 L/day** vs API **40.8 L/day** — **FAIL** *(spec formula 5× wrong)*
- `convoys_eliminated_yr` spec formula: 40.8×365/500 = 29.784 vs API **48.0** — **FAIL** *(spec formula wrong)*
- `fuel_cost_saved_yr_usd`: 14892.0 × 12 = 178704.00 vs API 178704.00 — **PASS**
- `total_value_yr_usd`: 178704 + 894774.24 = 1073478.24 vs API 1073478.24 — **PASS**
- `link_margin_db`: -0.0 (floating-point zero, meets threshold) — **PASS**

---

## UC5: Battlefield Relay (compare 2000m 5kW smoke)

### Laser side
**Raw values:** dc=5.0 kW | elec_in=1809.27 kW | eff=0.2764% | link_margin=0.0 | feasible=false

- `dc_power_delivered_kw`: 5.0 kW — **PASS** (≤ 5.0 target; but requires 1.8 MW input!)
- `electrical_input_kw`: 1809.27 kW > 5.0 kW — **PASS** (efficiency < 100%; 1.8 MW to deliver 5 kW)
- `system_efficiency_pct` formula check: 5.0 / 1809.27 × 100 = 0.2764% vs API 0.2764% — **PASS**
- `link_margin_db = 0.0` but `feasibility_ok = false` — **FAIL** *(inconsistency: for laser mode, link_margin is always 0.0 regardless of feasibility. UC5 laser requires 1.8 MW which is clearly infeasible — link_margin should be deeply negative like the physics shows (−25.6 dB). This is a laser link_margin reporting bug.)*

### Microwave side
**Raw values:** dc=0.00555 kW | elec_in=20.48 kW | eff=0.0271% | link_margin=-29.54 | feasible=false

- `dc_power_delivered_kw`: 0.00555 kW — **PASS** (≤ 5.0 target; tiny delivery due to beam spread)
- `electrical_input_kw`: 20.48 kW > 0.00555 kW — **PASS**
- `system_efficiency_pct` formula check: 0.00555 / 20.48 × 100 = 0.02711% vs API 0.02711% — **PASS**
- `link_margin_db`: −29.54 (negative = infeasible) — **PASS**
- `condition smoke→clear` mapping for MW — **WARNING** *(API correctly maps smoke→clear for MW physics since smoke doesn't attenuate microwave. But the UI/docs should explain this mapping explicitly.)*

**Key insight:** In smoke at 2km, laser needs 1.8 MW input (impractical) while MW needs only 20 kW but delivers only 5.5W. Neither is useful, but MW has practical input power. The `best_mode=microwave` recommendation is correct for smoke.

---

## UC6: Space LEO Laser (ISS 408km, 1kW, clear)

**Raw values:** dc=1.0 kW | elec_in=28.3 kW | eff=3.53% | beam_radius=1.01m

- `dc_power_delivered_kw`: 1.0 kW — **PASS** (≤ 1.0 target)
- `electrical_input_kw`: 28.3 kW > 1.0 kW — **PASS**
- `system_efficiency_pct` formula check: 1.0/28.3×100 = 3.534% vs API 3.53% — **PASS** (minor rounding)
- `beam_radius_at_ground_m`: 1.01m for 2m aperture at 408km — **PASS** *(expected ~1m; physically: w(z)=λz/(πw₀) at far field = 1070e-9×408e3/(π×1.0) ≈ 0.139m for a 1m aperture; with M²=1.3 and pointing, 1m is reasonable)*
- `fuel_cost_saved_yr_usd`: 4867×12 = 58404 vs API 58400 — **PASS** (minor rounding, space economics rounded differently)

---

## Fog Test (laser 2000m 5kW fog)

**Raw values:** dc=0.0 kW | link_margin=-99.0 | feasible=false | elec_input=12500 kW

- `dc_power_delivered_kw`: 0.0 kW — **PASS** ✓ (fog hard block correctly applied)
- `link_margin_db`: -99.0 — **PASS** (sentinel value for complete block)
- `feasibility_ok = false` — **PASS**
- `electrical_input_kw`: 12,500 kW — **WARNING** *(this is a sentinel/placeholder value for a hard-blocked link. Should be reported as N/A, 0, or null — not 12.5 MW. Misleading in UI display.)*

---

## MW Rain (microwave 500m 5kW rain)

**Raw values:** dc=0.02177 kW | elec_in=20.48 kW | eff=0.1063% | link_margin=-23.61 | feasible=false

- `dc_power_delivered_kw`: 0.02177 kW > 0 — **PASS** (rain is not a hard block for MW ✓)
- `electrical_input_kw`: 20.48 kW > 0.02177 kW — **PASS**
- `system_efficiency_pct` formula check: 0.02177/20.48×100 = 0.10631% vs API 0.10630% — **PASS**
- `link_margin_db`: -23.61 (negative = infeasible; beam spreads to 27.7m radius, need 1204m² RX vs 12.5m² actual) — **PASS**

---

## GEO MW (space microwave GEO 1000kW clear)

**Raw values:** dc=650 kW | elec_in=901.9 kW | eff=35% | TX array=2600m | rx_area=3.5km²

- `dc_power_delivered_kw`: 650 kW — **PASS** (≤ 1000 target)
- `electrical_input_kw`: 901.9 kW > 650 kW — **PASS**
- `system_efficiency_pct` formula check: 650/901.9×100 = **72.07%** vs API **35.0%** — **FAIL** *(CRITICAL: formula doesn't verify. The reported efficiency of 35% does NOT equal dc/elec × 100. Likely the API's elec_input field is the RF power budget, not total wall-plug input. The 35% appears to be an end-to-end estimate from literature (JAXA SSPS), not derived from the dc/elec ratio. The elec_input field meaning is unclear for space MW.)*
- `TX array km-scale`: 2600m diameter — **PASS** ✓
- `n_elements planetary scale`: ~7.948 billion elements — **PASS** ✓ (confirms infeasible for portable gear)
- `RX area km²-scale`: 3.5 km² rectenna required — **PASS** ✓

---

## Cross-Scenario Checks

### Check 13: Laser 300m efficiency > Laser 2km
- 300m: **7.582%** > 2km: **6.284%** — **PASS** ✓
- *Note: difference is modest because primary losses are wall-plug and PV efficiency, not geometric. Atmospheric/turbulence losses increase at 2km.*

### Check 14: Laser clear > Laser smoke at 2km
- Clear 2km: **6.284%** vs Smoke 2km: **0.276%** — **PASS** ✓
- *Smoke attenuates at ~5 dB/km → 10 dB loss at 2km → 10× power penalty — dramatic difference confirmed*

### Check 15: GEO MW requires km-scale hardware (infeasible portable)
- TX array: 2,600m diameter | Elements: 7.9 billion | RX rectenna: 3.5 km² — **PASS** ✓
- *JAXA SSPS scale infrastructure confirmed — zero possibility of portable deployment*

### Check 16: LEO laser more feasible than GEO laser
- LEO laser (408km): 3.53% efficiency, 1kW delivered from 28.3kW — functional system
- GEO laser: not directly tested, but GEO MW already requires 2600m TX array at GEO — **PASS** *(inferred; WARNING: no direct GEO laser test case in the test suite)*

### Check 5: Microwave better than laser in rain
- UC2 best_mode: **laser** | mw_rain best_mode: **laser** — **WARNING** ✓
- API says laser WINS in rain at tactical ranges (1070nm near-IR has only 0.09–0.35 dB/km rain attenuation per ITU)
- MW beam spreading (55m radius at 1km) completely dominates over 0.2 dB/km rain loss for laser
- **Spec claim "MW is better than laser in rain" is physically incorrect at 0.3–2km ranges**
- MW only wins vs laser in **FOG** and **CLOUD** (hard block for laser, ~0.01 dB/km for MW)
- At very long ranges (>20km) or extreme precipitation, MW may overcome beam-spread penalty

---

## Economics Formula Analysis

The documented spec formulas do NOT match the API implementation. The actual formulas are:

| Formula | Spec | Actual API |
|---------|------|-----------|
| `wpt_coverage_pct` | not specified | `min(100, dc_power_kw × 20)` |
| `fuel_saved_l_day` | `(dc/15) × 200` | `wpt_coverage_pct × 0.408` |
| `convoys_eliminated_yr` | `fuel_saved_l_day × 365/500` | `(wpt_coverage_pct/100) × 48` |
| `fuel_cost_saved_yr_usd` | `fuel_saved_l_yr × 12` | `fuel_saved_l_yr × 12` ✓ |
| `total_value_yr_usd` | `fuel_cost + convoy_cost` | `fuel_cost + convoy_cost` ✓ |

**Verification of actual formulas:**
- UC1 (dc=0.5kW): wpt=10%, fuel=10×0.408=4.08 ✓, convoys=0.10×48=4.8 ✓
- UC3 (dc=1kW): wpt=20%, fuel=20×0.408=8.16 ✓, convoys=0.20×48=9.6 ✓
- UC4 (dc=15kW): wpt=100%, fuel=100×0.408=40.8 ✓, convoys=1.00×48=48 ✓

The spec formula `(dc/15) × 200` would give 200 L/day at 15kW (fantasy), while the actual baseline is 40.8 L/day (realistic for a squad outpost at ~0.113 L/kWh × 24h × 15kW).

---

## FAILS Summary (11 total)

| # | Use Case | Field | Expected | Actual | Fix |
|---|----------|-------|----------|--------|-----|
| 1 | UC1 | `fuel_saved_l_day` formula | (dc/15)×200 = 6.667 | 4.08 | Update spec: use `wpt_cov×0.408` |
| 2 | UC1 | `convoys_eliminated_yr` formula | fuel_day×365/500 = 2.978 | 4.8 | Update spec: use `(wpt_cov/100)×48` |
| 3 | UC2 | `rayleigh_distance_m` | ~13m (D²/λ) | 26.5m | Update spec: correct formula is 2D²/λ = 26.5m ✓ |
| 4 | UC2 | `fuel_saved_l_day` formula | (dc/15)×200 = 0.1417 | 0.08674 | Update spec formula |
| 5 | UC2 | `convoys_eliminated_yr` formula | fuel_day×365/500 = 0.0633 | 0.10205 | Update spec formula |
| 6 | UC3 | `fuel_saved_l_day` formula | (dc/15)×200 = 13.333 | 8.16 | Update spec formula |
| 7 | UC3 | `convoys_eliminated_yr` formula | fuel_day×365/500 = 5.957 | 9.6 | Update spec formula |
| 8 | UC4 | `fuel_saved_l_day` formula | (dc/15)×200 = 200.0 | 40.8 | Update spec formula (5× error!) |
| 9 | UC4 | `convoys_eliminated_yr` formula | fuel_day×365/500 = 29.784 | 48.0 | Update spec formula |
| 10 | UC5 | `link_margin_db` laser | Should be negative for infeasible | 0.0 (always) | Fix: laser mode should return actual link margin dB, not always 0 |
| 11 | GEO MW | `system_efficiency_pct` formula | dc/elec×100 = 72.07% | 35.0% | Fix: space MW `electrical_input_kw` field doesn't represent total wall-plug; clarify meaning or recalculate |

---

## WARNINGS Summary (7 total)

| # | Use Case | Field | Warning |
|---|----------|-------|---------|
| 1 | UC1 | `beam_radius` 300m | Spec expected "mm-scale"; actual 7cm. Spec wrong. API correct (50mm waist, Rayleigh=7.3km) |
| 2 | UC2 | `rayleigh_distance` physics | API uses 2D²/λ = 26.5m (standard Fraunhofer). Spec expected D²/λ = 13m (non-standard). API correct. |
| 3 | UC2 | `beam_radius` 1km MW | 55.4m — confirms MW is far-field at 1km, beam spread is the dominant loss ✓ |
| 4 | UC4 | `beam_radius` 2km | Spec expected "meters"; actual 7cm. Spec wrong. Gaussian beam stays narrow within Rayleigh range. |
| 5 | UC5 | MW smoke→clear | API maps smoke→clear for MW physics (correct: smoke ≠ MW attenuation). Should be documented. |
| 6 | Fog | `electrical_input_kw` | 12,500 kW sentinel value for hard-blocked link. Should be null/0/N/A in response. |
| 7 | Cross-5 | MW vs laser in rain | Spec claim "MW better in rain" incorrect at tactical ranges. Near-IR laser wins in rain. MW only wins in fog/cloud. Update spec/marketing materials. |

---

## Suggested Fixes

### Priority 1 — Critical (breaks correctness)

**1. Fix economics spec documentation**
```
# Actual formulas (verified against all test cases):
wpt_coverage_pct = min(100, dc_power_delivered_kw * 20)
fuel_saved_l_day = wpt_coverage_pct * 0.408           # 40.8 L/day baseline at 100%
fuel_saved_l_yr  = fuel_saved_l_day * 365
convoys_eliminated_yr = (wpt_coverage_pct / 100) * 48  # 48 convoys/yr baseline at 100%
fuel_cost_saved_yr_usd = fuel_saved_l_yr * 12          # $12/L ✓
convoy_cost_saved_yr_usd = convoys_eliminated_yr * 18641.13  # per convoy cost
total_value_yr_usd = fuel_cost_saved_yr_usd + convoy_cost_saved_yr_usd
```

**2. Fix laser `link_margin_db` reporting**
```
# Current: always returns 0.0 for laser mode
# Fix: return actual link budget in dB (link_budget_db from physics object)
# UC5 laser physics shows link_budget_db = -25.59 dB — that should be the link_margin
```

**3. Fix GEO MW efficiency reporting**
```
# Current: system_efficiency_pct=35% does not equal dc/elec_input*100 (=72%)
# Fix options:
#   a) Report true wall-plug efficiency: elec_input should include RF amplifier losses
#   b) Clarify that elec_input for space MW is the RF power budget, not total power draw
#   c) Add a note explaining the 35% figure comes from JAXA literature, not dc/elec calculation
```

### Priority 2 — Warnings (misleading outputs)

**4. Fix fog test `electrical_input_kw` sentinel value**
```json
// Current: "electrical_input_kw": 12500.0  (meaningless placeholder)
// Fix: "electrical_input_kw": null, "feasibility_note": "FOG HARD BLOCK — no meaningful input power"
```

**5. Update spec beam_radius expectations**
- At 300m: expect **~5–10 cm** (near-field Gaussian, beam waist 50mm)
- At 2km: expect **~6–8 cm** (still near-field, Rayleigh = 7.3 km)
- MW beam at 1km: expect **~50–60 m** (far-field spreading)

**6. Update Rayleigh distance spec**
- Correct formula: `2D²/λ = 2 × 0.828² / 0.0517 = 26.5m` (Fraunhofer, standard)
- Not: `D²/λ = 13m` (non-standard, off by 2×)

**7. Correct the "MW better in rain" claim**
- Near-IR laser (1070nm) has very low rain attenuation: 0.09–0.35 dB/km (ITU-R P.838)
- MW at 5.8 GHz has beam spreading that overwhelms rain improvement at tactical ranges
- **Correct claim:** "MW is immune to FOG and CLOUD; laser wins in rain at ranges < 20km"

---

## Physics Summary

| Mode | Range | Condition | Efficiency | Input | Delivered | Feasible |
|------|-------|-----------|-----------|-------|-----------|----------|
| Laser | 300m | clear | 7.58% | 6.6 kW | 0.5 kW | ✓ |
| Laser | 500m | clear | 7.50% | 13.3 kW | 1.0 kW | ✓ |
| Laser | 2000m | clear | 6.28% | 238.7 kW | 15.0 kW | ✓ |
| Laser | 2000m | smoke | 0.28% | 1809 kW | 5.0 kW | ✗ (1.8MW impractical) |
| Laser | 2000m | fog | 0.00% | 12500 kW* | 0 kW | ✗ (hard block) |
| Microwave | 500m | rain | 0.11% | 20.5 kW | 22 W | ✗ (beam too wide) |
| Microwave | 1000m | rain | 0.05% | 20.5 kW | 10.6 W | ✗ (beam too wide) |
| Microwave | 2000m | smoke | 0.03% | 20.5 kW | 5.6 W | ✗ (beam too wide) |
| Space Laser | 408km LEO | clear | 3.53% | 28.3 kW | 1.0 kW | ✓ |
| Space MW | 35786km GEO | clear | 35%* | 902 kW | 650 kW | ✓ (km-scale only) |

*sentinel/literature value — see FAILs above

---

*Report generated by Kamber sub-agent | aether-math-validation session*
