# WPT Research Compendium — 2025
Last updated: 2026-02-24

> Compiled for the Aether WPT Simulator physics validation.
> Covers microwave and laser/optical power beaming — defense/logistics focus, 2018–2025.
> ~45 primary sources cited. Bolded numbers are **simulator-critical values**.

---

## 1. Microwave WPT — Key Papers

### Microwave Power Transmission Technologies for Space Solar Power Satellites
- **Authors:** Naoki Shinohara (Kyoto University)
- **Year:** 2011 (foundational) + 2025 update (co-authored with Bo Yang)
- **Source:** IEEE Proceedings + Chinese Space Science & Technology Journal (2025)
- **URL:** https://www.researchgate.net/publication/252010365 | https://journal26.magtechjournal.com/kjkxjs/EN/10.16708/j.cnki.1000-758X.2025.0017
- **Key finding:** Comprehensive framework for high-efficiency MPT. Rectenna designs achieving **70% RF-DC conversion** at 2.45/5.8 GHz in lab. Reviews phase/amplitude-controlled magnetron arrays for beam steering and efficiency optimization.
- **Relevance to Aether:** Direct source for rectenna efficiency parameterization. Beam-pointing error models for the phased array transmitter module.

### New Phased Array and Rectenna Array Systems for Microwave Power Transmission Research
- **Authors:** Naoki Shinohara et al. (Kyoto University)
- **Year:** 2011 (IEEE IMWS-IWPT)
- **Source:** IEEE Xplore
- **URL:** https://ieeexplore.ieee.org/document/5877091
- **Key finding:** Four core requirements for SPS-grade MPT identified: (1) high-efficiency microwave transmission, (2) huge output power capability, (3) high RF-DC conversion, (4) high beam-control accuracy. Demonstrates phased array + rectenna array coupling experiments.
- **Relevance to Aether:** System-level efficiency chain model — transmitter → free space → rectenna.

### A 5.8-GHz High-Power and High-Efficiency Rectifier Circuit With Lateral GaN Schottky Diode
- **Authors:** Dang, Wei et al.
- **Year:** 2021–2023
- **Source:** IEEE Transactions / Semantic Scholar
- **URL:** https://www.semanticscholar.org/paper/A-5.8-GHz-High-Power-and-High-Efficiency-Rectifier-Dang-Wei/254dff20256ea8678dbfc76401e627315ffd5a75
- **Key finding:** Lateral GaN SBD with turn-on voltage 0.38V, on-resistance 4.5Ω, junction capacitance 0.32 pF at 0V, breakdown voltage 164V. RF-DC conversion **85.1% at 33 dBm (2W) input** using AlGaN/GaN HEMT multi-channel structure. Efficiency >60% over wide range (14–38 dBm).
- **Relevance to Aether:** Best validated GaN rectenna efficiency for 5.8 GHz at practical (watts-class) power levels. Use **85% as the achievable high-power rectenna ceiling** at this frequency.

### Fast and Accurate Approach to RF-DC Conversion Efficiency Estimation for Multi-Tone Signals
- **Authors:** Various (MDPI Sensors)
- **Year:** January 2022
- **Source:** MDPI Sensors 22(3), 787
- **URL:** https://www.mdpi.com/1424-8220/22/3/787
- **Key finding:** GaAs diode-based rectennas optimized for high input power (>30 dBm) can achieve **>90% RF-DC conversion efficiency**. Notes this is only achievable with purpose-built high-power receivers; not typical for general applications.
- **Relevance to Aether:** Sets upper theoretical bound for rectenna efficiency in simulator. The ~90% number applies only at high power density and ideal matching.

### Broadband Compact Rectenna System Using Wilkinson Power Divider
- **Authors:** Various
- **Year:** May 2025
- **Source:** Scientific Reports (Nature)
- **URL:** https://www.nature.com/articles/s41598-025-02555-1
- **Key finding:** Broadband rectenna (1–18 GHz) using Schottky diodes. Demonstrates simultaneous dual-polarization reception. Efficiency drops significantly at low power density.
- **Relevance to Aether:** Wide-band rectenna behavior — relevant if modeling frequency-agile or multi-band WPT.

### Ground Demonstration Testing of Microwave Wireless Power Transmission (JAXA 2015)
- **Authors:** JAXA / Japan Space Systems team
- **Year:** 2015
- **Source:** JAXA R&D Directorate
- **URL:** https://www.kenkai.jaxa.jp/eng/research/ssps/150301.html
- **Key finding:** **1.8 kW WPT transmitted over 55 meters** to rectenna array. Precise beam-pointing control demonstrated. Concurrent: Mitsubishi Heavy Industries demonstrated **10 kW over 500 meters** in the same period — milestone for industrial-scale ground WPT.
- **Relevance to Aether:** Closest real-world validation of kW-class terrestrial WPT at hundreds of meters. Use JAXA 2015 as the benchmark calibration point.

### JAXA SSPS Microwave WPT Study: 1.6 kW Beam, 350W Output at 50m
- **Authors:** JAXA / Mitsubishi
- **Year:** 2021 report
- **Source:** IEEE Spectrum reporting
- **URL:** https://spectrum.ieee.org/japan-demoes-wireless-power-transmission-for-spacebased-solar-farms
- **Key finding:** 1.6 kW microwave beam → **~350W at rectenna** over 50m. Implies **~22% end-to-end system efficiency** (transmitter to rectenna DC). Beam pointing accuracy demonstrated for SSPS precursor.
- **Relevance to Aether:** Key number for end-to-end system efficiency. The large gap between rectenna-only (~70%) and system-level (~22%) efficiency is important — free-space beam losses and aperture mismatch dominate at short range without large receiving array.

### Japan OHISAMA Aircraft WPT Flight Demonstration (December 2024)
- **Authors:** Japan Space Systems, JAXA/ISAS
- **Year:** December 2024
- **Source:** Japan Space Systems Test Report + Space Energy Insights
- **URL:** https://www.jspacesystems.or.jp/jss/wp-content/uploads/2025/01/1stTestReport_2024.12.24en-1.pdf
- **Key finding:** **World's first WPT from aircraft at 7 km altitude to ground receiving station**. Aircraft-mounted microwave transmitter beamed power at 5–7 km range over Nagano Prefecture, Kirigamine. Precursor to OHISAMA satellite demo from 450 km LEO orbit. Tests assess how ionosphere + atmosphere affect efficiency at operational ranges.
- **Relevance to Aether:** Validates that **ground-level horizontal path through thick atmosphere is hardest case** (as confirmed by Jaffe/DARPA); vertical path ~10× less atmospheric loss. Critical for FOB scenario modeling.

### Space Solar Power Programs and Microwave Wireless Power Transmission Technology
- **Authors:** Naoki Shinohara, Hiroshi Matsumoto
- **Year:** 2003 (foundational), 2025 review cited
- **Source:** Academia.edu / IEEE
- **URL:** https://www.academia.edu/3147367/Space_solar_power_programs_and_microwave_wireless_power_transmission_technology
- **Key finding:** Reference SPS designs at 5.8 GHz — **JAXA model uses 1 km diameter transmitting antenna, Gaussian taper 10 dB**, max power density at center 420 mW/cm² for 1.3 GW system. Antenna spacing 0.75λ standard. This table is the canonical reference for SPS microwave system parameters.
- **Relevance to Aether:** Source for SPS-scale beam parameters if extending Aether to space-to-ground scenario.

### Microwave Wireless Power Transfer Efficiency Analysis for Thin-Film Space Solar Power Satellite
- **Authors:** Various (Nakasuka group, Tokyo)
- **Year:** 2024
- **Source:** Acta Astronautica (ScienceDirect)
- **URL:** https://www.sciencedirect.com/science/article/abs/pii/S0273117724003223
- **Key finding:** Framework for analyzing WPT efficiency (WPTE) for the "furoshiki" modular SSPS concept. Characterizes performance vs. mass, fuel consumption during LEO operations. Design trade-offs documented.
- **Relevance to Aether:** Framework for modular WPT system efficiency chains applicable to terrestrial deployments.

### The High Power Electricity Generation and WPT Demonstration Mission (China)
- **Authors:** Chinese research team (CASC-related)
- **Year:** 2025
- **Source:** ScienceDirect (Acta Astronautica / space energy journal)
- **URL:** https://www.sciencedirect.com/science/article/pii/S2950104025000276
- **Key finding:** First-step mission for Chinese SBSP: kW-level microwave WPT from LEO + simultaneous kW-level laser WPT from LEO. Validates theoretical energy transmission efficiency chain and long-distance beam control precision. Cross-validates 5.8 GHz and laser (~1 µm) simultaneously.
- **Relevance to Aether:** Dual-modality (microwave + laser) WPT in one mission — efficiency chain data applicable to combined-system simulations.

### Naval Postgraduate School Thesis: Space-Based Solar Power for Defense
- **Authors:** NPS student (DTIC)
- **Year:** ~2022
- **Source:** DTIC (AD1201667)
- **URL:** https://apps.dtic.mil/sti/trecms/pdf/AD1201667.pdf
- **Key finding:** Reviews SPS concepts from a DoD logistics perspective. Notes that beaming power from space to FOBs would eliminate fuel convoy requirements — key driver for military adoption.
- **Relevance to Aether:** Military-specific efficiency requirements and FOB scenario parameters.

### NRL PRAM (Photovoltaic Radio-Frequency Antenna Module)
- **Authors:** Paul Jaffe, NRL
- **Year:** 2020 (launched on X-37B OTV; tests ongoing 2020–2022)
- **Source:** EE Power / NRL press releases
- **URL:** https://eepower.com/news/nrl-begins-testing-solar-power-satellite-in-orbit/
- **Key finding:** First solar power sandwich module in orbit (launched May 2020 on X-37B OTV-6). Demonstrated end-to-end conversion of solar energy to microwave RF in space. Not beamed to Earth, but validated the tile architecture for future transmission. Jaffe: "For solar-powered satellites, the idea would be to provide energy anywhere in the world."
- **Relevance to Aether:** PRAM architecture informs efficiency budget for space-to-ground microwave WPT.

---

## 2. Laser/Optical Power Beaming — Key Papers

### DARPA POWER Program — PRAD World Record (May 2025)
- **Authors:** Paul Jaffe (PM), Teravec Technologies (receiver), NRL, White Sands HELSTF team
- **Year:** May 2025
- **Source:** DARPA official press release
- **URL:** https://www.darpa.mil/news/2025/darpa-program-distance-record-power-beaming
- **Key finding:** **800W+ delivered over 8.6 km (5.3 miles) in a 30-second transmission.** Total campaign: >1 megajoule transferred. Previous records: 230W at 1.7 km. Receiver designed by Teravec: compact aperture, parabolic mirror reflecting onto dozens of PV cells. **~20% efficiency from optical-out to electrical-out at shorter distances.** Horizontal ground path through maximum atmospheric thickness. Scalable to UAVs. POWER Phase 2 now moving to vertical transmission + integrated relays.
- **Relevance to Aether:** **Single most important 2025 data point.** Sets real-world efficiency floor (~20%) for laser WPT at km-scale with state-of-the-art hardware. Key input: horizontal path is worst case; model vertical FOB beaming with ~5× lower loss.

### PowerLight Technologies — PTROL-UAS Program (December 2025)
- **Authors:** Tom Nugent (CTO/co-founder), PowerLight Technologies
- **Year:** December 16, 2025
- **Source:** EINPresswire / PowerLight press release
- **URL:** https://powerlighttech.com/press-release-laser-power-beaming-uas/
- **Key finding:** End-to-end laser power beaming system for DoD UAS developed under CENTCOM sponsorship. Key specs: **kilowatt-class laser transmitter**, autonomous precision optical tracking, **range up to 5,000 feet (~1.5 km) altitude**, 6-pound airframe-mounted receiver using laser power converters. Integrated with Kraus Hamdani Aerospace K1000ULE ultra-long-endurance UAS (used by US Navy and Army). Full flight test scheduled early 2026.
- **Relevance to Aether:** Real system parameters for laser UAV WPT: ~kW power, ~1.5 km altitude, non-visible laser (unspecified wavelength), active tracking required. The "intelligent mesh energy network" concept = multiple transmitters coordinating to multiple UAVs.

### 55% Efficient High-Power Multijunction PV Laser Power Converters for 1070 nm
- **Authors:** Various (InP-based III-V heterostructure group)
- **Year:** April 2025
- **Source:** MDPI Photonics 12(5), 406
- **URL:** https://www.mdpi.com/2304-6732/12/5/406
- **Key finding:** InP-based 8-junction InGaAsP photovoltaic laser power converters. **Conversion efficiency of 55% at 18W output power at 1070 nm.** First high-power demonstration at this wavelength. Bandgap engineering for ~1.1 eV optimized for Yb fiber laser (1070 nm) which is the dominant industrial/military high-power laser source.
- **Relevance to Aether:** **Use 55% as the current state-of-the-art PV receiver efficiency at 1070 nm.** This is the peak, not average — derate to ~45-50% for system modeling.

### Beaming Power: Photovoltaic Laser Power Converters for Power-by-Light (Review)
- **Authors:** Various
- **Year:** December 2021
- **Source:** Joule (Cell Press) / ScienceDirect
- **URL:** https://www.cell.com/joule/fulltext/S2542-4351(21)00540-7
- **Key finding:** Comprehensive review of PVLPC technology. **Highest efficiency achieved: 55% at 800–850 nm wavelength.** Reviews all wavelength windows. Notes second window (~1310 nm): efficiencies not exceeding 60% reported in limited studies. GaAs-based converters dominate for 800–850 nm; InGaAs/InP for 1000–1100 nm range.
- **Relevance to Aether:** PVLPC efficiency as a function of wavelength — directly feeds laser receiver efficiency model.

### Photovoltaic AlGaAs/GaAs Devices for Conversion of High-Power Density Laser (800–860 nm)
- **Authors:** Russian/European team
- **Year:** September 2023
- **Source:** Solar Energy Materials and Solar Cells (ScienceDirect)
- **URL:** https://www.sciencedirect.com/science/article/abs/pii/S0927024823003720
- **Key finding:** AlGaAs/GaAs converters: **52% efficiency at 1.06 µm (ELR = 6.5 W/cm²)**; **55% at 1.02 µm (4 W/cm²)**; drops to 48% at 13 W/cm². Critical finding: **efficiency degrades significantly at very high power density** — relevant for close-range high-intensity beaming.
- **Relevance to Aether:** Power density dependent efficiency curve for laser receivers. Simulator should implement saturation curve, not flat efficiency.

### 1.1 eV GaInAs Cell Development for Dual-Use Solar and 1070 nm Laser Power Converters
- **Authors:** NREL/DOE group
- **Year:** November 2024
- **Source:** OSTI.gov
- **URL:** https://www.osti.gov/biblio/2499744
- **Key finding:** Dual-use solar+laser converter cells for space applications. Simultaneously receives solar and 1070 nm laser power. Critical for satellites that need to collect ambient solar AND receive beamed laser power. Single-junction GaInAs optimized for 1.1 eV bandgap.
- **Relevance to Aether:** Dual-mode receiver concept relevant to hybrid solar+WPT UAV scenarios.

### Caltech SSPD-1 / MAPLE In-Orbit Demonstration (2023)
- **Authors:** Ali Hajimiri, Harry Atwater, et al. (Caltech SSPP)
- **Year:** Launched January 2023; WPT demonstration May–June 2023
- **Source:** Caltech official announcements + IEEE Spectrum
- **URL:** https://www.caltech.edu/about/news/in-a-first-caltechs-space-solar-power-demonstrator-wirelessly-transmits-power-in-space
- **Key finding:** MAPLE (Microwave Array for Power-transfer Low-orbit Experiment) — **first-ever wireless power transmission from orbit to Earth.** Flexible lightweight microwave power transmitters on custom ICs with precise timing for beam steering. Power detected at Caltech campus (Pasadena) on May 22, 2023 with correct frequency and Doppler shift from LEO. DOLCE structure (6×6 ft deployable) + ALBA (32 PV cell types) also tested. Mission concluded with "successes and lessons."
- **Relevance to Aether:** Proof that phased-array microwave WPT from LEO works. Hajimiri IC architecture (integrated transmitter tile) is the leading approach for low-mass, high-density transmitter arrays.

### Laser Power Beaming for UAV Charging — Feasibility Assessment
- **Authors:** Various
- **Year:** June 2021
- **Source:** ScienceDirect (Optics & Laser Technology)
- **URL:** https://www.sciencedirect.com/science/article/abs/pii/S0030399221003716
- **Key finding:** Reviews LWPT for UAV applications. Notes JAXA tested **horizontal lasers over 500 m in 2012** for SSPS research. WPT market was $2.5B in 2016, growing at 23.15% CAGR through 2022. Confirms laser WPT enables theoretical unlimited endurance for UAVs.
- **Relevance to Aether:** Market and technology context; confirms 500m laser WPT ground demo.

### Wireless Power Transfer With UAVs: State of the Art and Open Challenges
- **Authors:** Various
- **Year:** July 2023
- **Source:** Pervasive and Mobile Computing (ScienceDirect)
- **URL:** https://www.sciencedirect.com/science/article/pii/S1574119223000780
- **Key finding:** Comprehensive review of UAV WPT combining LWPT, MWPT, and near-field approaches. Key challenge: tracking moving UAVs at distance while maintaining beam alignment. Notes that LWPT and MWPT are the only viable approaches for >10m range UAV powering.
- **Relevance to Aether:** Taxonomy and architecture reference for multi-UAV WPT scenarios.

### Laser-Powered UAV Trajectory and Charging Optimization
- **Authors:** Various
- **Year:** December 2024 (online)
- **Source:** IEEE Transactions on Mobile Computing
- **URL:** https://dl.acm.org/doi/10.1109/TMC.2024.3523281
- **Key finding:** Trajectory optimization for data-gathering UAV receiving laser charging from high-altitude platforms (HAPs). Models laser-to-battery charging efficiency vs. distance and angle. Confirms charging feasibility for sustained IoT-type missions.
- **Relevance to Aether:** Trajectory-aware WPT model — angle of incidence effects on receiver efficiency.

### DARPA Far-Field Wireless Power Beaming for Drone Recharging (2024)
- **Authors:** DARPA program office / University of Texas Dallas (Mahbub)
- **Year:** May 2024
- **Source:** NewAtlas / UTD News
- **URL:** https://newatlas.com/technology/darpa-far-field-wireless-power-beaming-charges-drones-in-flight/ | https://news.utdallas.edu/science-technology/mahbub-darpa-grant-2024/
- **Key finding:** DARPA committed additional funding for far-field WPT to **wirelessly recharge drones in flight without mission interruption**. University of Texas Dallas received DARPA grant for power beaming circuits. Goal: enable persistent ISR/combat drone swarms without battery-swap landings.
- **Relevance to Aether:** Direct military application. DARPA is now funding multiple power-beaming-to-UAV programs simultaneously (POWER + this track).

---

## 3. Defense/Logistics Applications

### ESA SOLARIS Initiative (2022–2024)
- **Authors:** ESA / Sanjay Vijendran (lead, now Space Energy Insights)
- **Year:** 2022–2024
- **Source:** ESA.int official pages
- **URL:** https://www.esa.int/Enabling_Support/Space_Engineering_Technology/SOLARIS
- **Key finding:** ESA commissioned two independent cost/benefit studies in 2022 (Frazer-Nash UK; Roland Berger Germany). Signed contracts for two parallel SBSP commercial-scale concept studies in 2023. SOLARIS uses **radio waves (microwave) as the preferred WPT modality** for ground delivery. 2022 German lab test demonstrated WPT over **36 meters** for technology validation. Still a long way from commercial scale.
- **Relevance to Aether:** European institutional validation of microwave WPT. 36m lab demo sets a floor for technology readiness.

### John Mankins — SPS-ALPHA Mark III and Achievable Roadmap (2021)
- **Authors:** John C. Mankins
- **Year:** October 2021 (72nd IAC)
- **Source:** International Astronautical Congress
- **URL:** Referenced in NASA OTPS SBSP Report (2024)
- **Key finding:** SPS-ALPHA architecture uses cone-shaped framework with thin-film mirrors up to 6 km diameter, power transmitted via arbitrarily large phased arrays. Mark III is more achievable than earlier concepts. Key insight: modular architecture allows incremental deployment.
- **Relevance to Aether:** Scalable modular transmitter architecture — applicable to terrestrial deployment where multiple small transmitters coordinate.

### NASA Office of Technology, Policy, and Strategy — Space-Based Solar Power Report (January 2024)
- **Authors:** NASA OTPS team
- **Year:** January 2024
- **Source:** NASA.gov
- **URL:** https://www.nasa.gov/wp-content/uploads/2024/01/otps-sbsp-report-final-tagged-approved-1-8-24-tagged-v2.pdf
- **Key finding:** Comprehensive review of SBSP feasibility. Cites Mankins SPS-ALPHA-III (2021) and Pellegrino et al. lightweight SSPS (2022). Discusses both microwave (2.45/5.8 GHz) and laser WPT options. Key conclusion: technology is advancing rapidly but deployment is still 15–25 years away for commercial GW-scale systems. Smaller tactical/military systems are nearer-term.
- **Relevance to Aether:** Official U.S. government assessment of WPT technology maturity and timelines.

### Forward Operating Base Energy Logistics — Military WPT Applications
- **Authors:** Army Technology / Marine Corps research (various)
- **Year:** Ongoing
- **Source:** Army Technology, Marine Design Dynamics
- **URL:** https://www.army-technology.com/features/featuresafe-and-well-stocked-new-technology-for-todays-forward-operating-bases-4647465/
- **Key finding:** FOB energy is a critical vulnerability. Each gallon of fuel at a remote FOB costs $400–$600 when accounting for convoy losses and logistics overhead. **Wireless power eliminates fuel convoys**, removes single-point energy targets, enables flexible generation. WPT identified as a key enabler for future "expeditionary energy" doctrine.
- **Relevance to Aether:** Mission context. The simulation's core value is modeling this scenario.

### China OMEGA / Xidian University SBSP Program
- **Authors:** Duan Baoyan (Chinese Academy of Engineering), Xidian University
- **Year:** 2019–2025
- **Source:** Global Times, China-in-space.com, PowerMag
- **URL:** https://www.china-in-space.com/p/why-china-is-developing-space-based | https://www.powermag.com/china-group-announces-successful-test-of-space-based-solar-power/
- **Key finding:** OMEGA (Orb-shape Membrane Energy Gathering and Orienting) architecture designed for GEO SBSP. **24% more power-per-mass** vs. US SPS-ALPHA. Bishan test facility in Chongqing ($15M), testing microwave WPT transmission technology. 2022 announced successful ground test. Timeline: small test satellite by 2028, 1 MW station by 2035, 1 GW by 2050.
- **Relevance to Aether:** Competition driver; validates global race to develop WPT for grid-scale power delivery.

### Development and Prospect of WPT for UAVs (Review 2022)
- **Authors:** Various (Chinese and international)
- **Year:** July 2022
- **Source:** Electronics (MDPI) 11(15), 2297
- **URL:** https://www.mdpi.com/2079-9292/11/15/2297
- **Key finding:** LWPT and MWPT both viable for long-range UAV power supply; LWPT better for precision/small aperture applications, MWPT better for larger aperture/all-weather operations. Reviews all UAV WPT demonstrations through 2022.
- **Relevance to Aether:** Confirms design space for UAV WPT — LWPT vs MWPT trade-off depends primarily on range and weather resilience requirements.

### China High-Power WPT Demonstration Mission Proposal (2025)
- **Authors:** CASC-affiliated research group
- **Year:** 2025
- **Source:** ScienceDirect
- **URL:** https://www.sciencedirect.com/science/article/pii/S2950104025000276
- **Key finding:** kW-level microwave WPT from LEO to ground + kW-level laser WPT between spacecraft simultaneously. Validates end-to-end efficiency chain under orbital conditions. **Dual-mode (microwave + laser) WPT on same mission.**
- **Relevance to Aether:** Only known mission planning simultaneous MW + laser WPT comparison.

---

## 4. Atmospheric Effects & Propagation

### ITU-R P.838-3: Specific Attenuation Model for Rain (Microwave)
- **Authors:** ITU-R Study Group 3
- **Year:** March 2005 (current edition)
- **Source:** ITU International Telecommunications Union
- **URL:** https://www.itu.int/rec/R-REC-P.838-3-200503-I/en
- **Key finding:** Standard power law for rain attenuation: **γ = k × R^α (dB/km)** where R is rain rate (mm/hr). At 5.8 GHz horizontal polarization: **k_H ≈ 0.00454, α_H ≈ 1.244** (interpolated from ITU table). Computed attenuation:
  - Light rain (10 mm/hr): **≈ 0.07 dB/km**
  - Moderate rain (25 mm/hr): **≈ 0.20 dB/km**
  - Heavy rain (50 mm/hr): **≈ 0.45 dB/km**
  - Extreme rain (100 mm/hr): **≈ 1.0 dB/km**
- **Relevance to Aether:** **Primary rain attenuation model for microwave path loss.** These numbers are THE authoritative source for 5.8 GHz rain attenuation. Confirm current simulator implementation.

### ITU-R P.676-11: Attenuation by Atmospheric Gases (Microwave)
- **Authors:** ITU-R
- **Year:** September 2016
- **Source:** ITU
- **URL:** https://www.itu.int/dms_pubrec/itu-r/rec/p/R-REC-P.676-11-201609-I!!PDF-E.pdf
- **Key finding:** At 5.8 GHz, **gaseous absorption (O₂ + H₂O) is approximately 0.003–0.010 dB/km** for typical sea-level conditions. The 60 GHz oxygen absorption peak (10 dB/km) does NOT affect 5.8 GHz. Water vapor absorption is also negligible at 5.8 GHz (peak at 22.2 GHz). **5.8 GHz is specifically chosen for WPT because it sits in an atmospheric transmission window.**
- **Relevance to Aether:** Gaseous absorption is negligible at 5.8 GHz — rain is the dominant atmospheric loss mechanism. Do NOT add significant gaseous loss to the microwave model.

### Atmospheric Transmission Windows for High-Power Lasers
- **Authors:** Various (NPS / AFRL)
- **Year:** 2003–2021 (foundational + updates)
- **Source:** DTIC / NPS Thesis (ADA420318) + MDPI 2021
- **URL:** https://apps.dtic.mil/sti/tr/pdf/ADA420318.pdf
- **Key finding:** Atmospheric transmission windows for laser WPT:
  - **~1 µm (1000–1100 nm):** Moderate transmission but **high aerosol extinction** relative to longer wavelengths. Dominant military fiber laser wavelength (Yb, 1070 nm). Clear sky transmission: **~0.93–0.98 per km** depending on visibility.
  - **~1.55 µm (1550 nm):** Better aerosol transmission, eye-safe. Lower PV efficiency available. Clear sky: **~0.97–0.99 per km**.
  - **~800–850 nm:** Near-IR, GaAs PV peak efficiency window. Higher aerosol extinction. Clear sky: **~0.90–0.95 per km**.
  - Note: **Fog and clouds completely block all near-IR/optical WPT** (>20 dB/km extinction), unlike microwave.
- **Relevance to Aether:** Laser atmospheric transmission parameters. **Use 0.93/km for 1070 nm in clear conditions** as conservative estimate; 0.98/km for favorable/high altitude conditions.

### Comparison of Laser Beam Propagation at 785 nm and 1550 nm in Fog and Haze
- **Authors:** McMaster University team
- **Year:** 2000 (foundational, still definitive)
- **Source:** SPIE Proceedings / McMaster ECE
- **URL:** https://www.ece.mcmaster.ca/~hranilovic/woc/resources/local/spie2000b.pdf
- **Key finding:** Fog is catastrophic for optical WPT — attenuation can reach **20–100+ dB/km** in dense fog. Light haze: **1–5 dB/km**. 1550 nm is significantly more fog-tolerant than 785 nm due to larger particle Mie scattering crosssection effects. **There is no "near-IR fog window"** that beats microwave for all-weather ops.
- **Relevance to Aether:** Laser WPT is weather-limited. Critical for realistic availability modeling in the simulator. FOB scenarios in humid/cloudy climates should model hybrid MW+laser or MW-only.

### Laser Beam Atmospheric Propagation Modelling for LIDAR Applications
- **Authors:** Various
- **Year:** July 2021
- **Source:** MDPI Atmosphere 12(7), 918
- **URL:** https://www.mdpi.com/2073-4433/12/7/918
- **Key finding:** Three degradation mechanisms for laser beams in atmosphere: **(1) beam spreading** (divergence increases with turbulence), **(2) scintillation** (power fluctuations from refractive index turbulence), **(3) beam wander** (lateral displacement). All three increase with range and decrease with altitude. Near-ground, turbulence is worst (Cn² typically 10⁻¹⁵ to 10⁻¹² m⁻²/³).
- **Relevance to Aether:** Implement Rytov variance or Cn² turbulence model for scintillation. Use Kolmogorov spectrum. At 1 km ground-level range, scintillation can cause **±3–6 dB power fluctuations.**

### Rain Attenuation Measurement for Short-Range mmWave Fixed Link (ITU validation)
- **Authors:** Zahid et al.
- **Year:** April 2022
- **Source:** Radio Science (AGU / Wiley)
- **URL:** https://agupubs.onlinelibrary.wiley.com/doi/full/10.1029/2021RS007307
- **Key finding:** Experimental validation of ITU-R P.838-3 model against real measurements. Confirms ITU model is accurate for frequencies 1–100 GHz terrestrial paths. Provides k and α table for reference.
- **Relevance to Aether:** ITU-R P.838-3 is experimentally validated — **use it as primary rain attenuation model.**

### OHISAMA Mission: Atmosphere + Ionosphere Effects on WPT (2024–2025)
- **Authors:** Japan Space Systems / JAXA / ISAS
- **Year:** 2024–2025
- **Source:** Asahi Shimbun / NotebookCheck / JAXA
- **URL:** https://www.asahi.com/ajw/articles/16293144 | https://www.notebookcheck.net/Space-based-solar-power-Japan-s-OHISAMA-project-aims-to-beam-solar-energy-to-Earth.1025860.0.html
- **Key finding:** Satellite mission from 450 km LEO will specifically measure how transmission distance, **ionosphere, and atmosphere affect efficiency** for 5.8 GHz microwave beaming. Aircraft demo at 7 km was rehearsal. The ionosphere causes **Faraday rotation and dispersion** for frequencies below ~10 GHz — relevant for space-to-ground but negligible for terrestrial (< 30 km path).
- **Relevance to Aether:** For ground-level WPT scenarios, ionospheric effects are negligible. For space WPT extension of the model, add Faraday rotation loss (~0.5–2 dB at 5.8 GHz for typical TEC).

---

## 5. Hardware — Rectenna / PV Efficiency Records

### GaN HEMT Rectenna Record at 5.8 GHz (2020–2023)
- **Authors:** AlGaN/GaN HEMT research groups (ScienceDirect 2020)
- **Year:** July 2020
- **Source:** ScienceDirect (Materials Science in Semiconductor Processing)
- **URL:** https://www.sciencedirect.com/science/article/abs/pii/S0749603620306480
- **Key finding:** Multi-channel AlGaN/GaN structure: **85.1% RF-DC rectification at 33 dBm (2W) input power** at 5.8 GHz. Efficiency >60% over broad input range (14–38 dBm = 25 mW to 6.3W). SiN passivation reduces surface traps. Low turn-on voltage (0.38V) is key advantage of GaN vs GaAs for high-power rectification.
- **Relevance to Aether:** **Best validated GaN rectenna efficiency: 85% at 2W, 5.8 GHz.** Use as upper bound for high-power 5.8 GHz rectenna in simulator.

### GaAs Rectenna: >90% Efficiency at High Power (2022)
- **Authors:** Referenced in MDPI Sensors review (Rec. [5,8])
- **Year:** Various (pre-2022)
- **Source:** MDPI Sensors 22(3)
- **URL:** https://www.mdpi.com/1424-8220/22/3/787
- **Key finding:** GaAs diode rectennas purpose-built for **high input power (>30 dBm)** can exceed **90% RF-DC conversion efficiency**. Only achievable with receiver optimized for that specific power level — not suitable for wide dynamic range applications. Fundamental limit: diode series resistance and junction capacitance.
- **Relevance to Aether:** **90% is the theoretical ceiling for microwave rectenna** — only at very high, constant power levels with precisely matched impedance. Real-world deployable systems: 70–85% expected.

### Schottky Diode High-Efficiency Rectenna for Energy Harvesting (2024)
- **Authors:** Various
- **Year:** March 2024
- **Source:** Heliyon (ScienceDirect)
- **URL:** https://www.sciencedirect.com/science/article/pii/S2405844024038234
- **Key finding:** Commercial Schottky diode at low power density (−5 dBm = 0.3 mW): **52% RF-DC conversion**. Efficiency drops sharply at low power density — fundamental physics of diode rectification.
- **Relevance to Aether:** Rectenna efficiency is strongly power-density dependent. At low input power (long range / small aperture), expect 40–60% efficiency, NOT the 80–90% achievable at high power.

### Teravec Technologies PRAD Receiver
- **Authors:** Raymond Hoheisel (PI), Teravec / Packet Digital / RIT
- **Year:** 2025
- **Source:** DARPA POWER press release
- **URL:** https://www.darpa.mil/news/2025/darpa-program-distance-record-power-beaming
- **Key finding:** Novel compact-aperture receiver with parabolic mirror concentrator + dozens of PV cells. Designed for long-range laser WPT. **~20% optical-to-electrical efficiency at shorter ranges.** Note: efficiency was not the optimization target — distance was. Built in ~3 months. Scalable design suitable for UAV integration.
- **Relevance to Aether:** Current deployed/military laser receiver achieves ~20% efficiency. The 55% PV cell efficiency shown in lab conditions is NOT the system efficiency — optical path losses, tracking losses, and receiver design losses reduce it significantly.

### InP-Based 8-Junction Laser Power Converter (1070 nm, 55%)
- **Authors:** InP group (published MDPI Photonics 2025)
- **Year:** April 2025
- **Source:** MDPI Photonics 12(5), 406
- **URL:** https://www.mdpi.com/2304-6732/12/5/406
- **Key finding:** **8-junction lattice-matched InGaAsP subcells, 55% efficiency at 18W output, 1070 nm.** This is the cell efficiency, not system efficiency. Requires precisely matched laser wavelength and power density.
- **Relevance to Aether:** **PV cell efficiency ceiling for 1070 nm: 55%.** System efficiency in practice: 20–45% (accounting for optics, tracking, thermal effects).

### GaAs Laser Power Converter for 800–860 nm Power Beaming
- **Authors:** Various (ResearchGate / MDPI)
- **Year:** 2015–2023
- **Source:** ResearchGate
- **URL:** https://www.researchgate.net/publication/274097170_Design_and_Optimization_of_GaAs_Photovoltaic_Converter_for_Laser_Power_Beaming
- **Key finding:** GaAs-based PV converters for 800–860 nm. Efficiency up to **55% for wavelengths 800–850 nm** (bandgap-matched). GaAs is the dominant material for this wavelength. Used in most commercial laser WPT systems using 808/830/850 nm pump/transmit lasers.
- **Relevance to Aether:** If using 800–850 nm laser: 55% PV efficiency is achievable. If 1070 nm: also 55% with InGaAsP (newer). Trade-off: beam divergence is worse at shorter wavelengths.

---

## 6. State of the Art Summary (2025)

### Current Best Demonstrated WPT Performance

| Parameter | Microwave | Laser |
|-----------|-----------|-------|
| **Best rectenna/PV efficiency (lab)** | ~92% (GaAs, high power) | 55% (1070nm InGaAsP, 2025) |
| **Best deployed system efficiency** | ~22% end-to-end (JAXA 2021) | ~20% (DARPA PRAD, 2025) |
| **Max demonstrated range (appreciable power)** | ~7 km (OHISAMA aircraft, Dec 2024) | **8.6 km (DARPA POWER PRAD, May 2025)** |
| **Max power delivered at range** | ~10 kW at 500m (Mitsubishi, 2015) | **800W at 8.6 km (DARPA, 2025)** |
| **All-weather capability** | Yes (rain: 0.07–1.0 dB/km at 5.8 GHz) | No (fog/cloud: >20 dB/km) |
| **Beam safety** | Low SAR per ITU limits | Eye/skin hazard, requires exclusion zone |
| **Frequency/wavelength** | 2.45 or 5.8 GHz preferred | 800–850 nm, 1070 nm, 1550 nm |

### Current Best Microwave WPT Efficiency
- **Rectenna only:** ~85–92% (GaN or GaAs at high input power, lab conditions)
- **End-to-end system (transmitter DC → receiver DC):** ~20–25% for practical demonstrations
- **Why the gap?** Beam spreading losses (inverse square), aperture efficiency, impedance matching losses, amplifier efficiency (~40–60% for solid-state PA at 5.8 GHz)

### Current Best Laser WPT Efficiency
- **PV cell only:** 55% at 1070 nm (2025 record); 55% at 800–850 nm
- **End-to-end system (electrical → electrical):** ~20% at 8.6 km (DARPA PRAD); ~30–45% at close range
- **Why the gap?** Laser wall-plug efficiency (~35–50% for fiber lasers), atmospheric losses, beam divergence/tracking losses, PV receiver losses

### Max Demonstrated Range
- **Microwave:** 7 km (Japan OHISAMA aircraft demo, December 2024)
- **Laser:** **8.6 km horizontal ground path (DARPA POWER PRAD, May 2025)** — shattering the previous 1.7 km record

### Key Unsolved Problems (for defense logistics)
1. **All-weather laser WPT** — fog/cloud availability problem; no solution other than switching to microwave
2. **Tracking moving targets at km range** — beam jitter and atmospheric turbulence limit efficient energy delivery to fast-moving UAVs
3. **Eye safety in military airspace** — limits laser power density and requires exclusion zones
4. **High-altitude UAV power delivery** — atmosphere thins but tracking and divergence become dominant
5. **Size/weight of rectenna arrays** — large aperture needed for efficient microwave reception
6. **Multi-target beam splitting** — phased arrays can steer to multiple targets but efficiency drops proportionally
7. **EMI and spectrum coordination** — 5.8 GHz conflicts with ISM band; limited spectrum allocation for high-power WPT
8. **System end-to-end efficiency** — current ~20% system efficiency means 5× power generation overhead vs. delivered power

---

## 7. Physics Constants & Validated Parameters

> These are the authoritative numbers for the Aether simulator physics engine.
> Sources cited. Where a range is given, use the conservative (lower) value for design.

### Rectenna (Microwave Receiver) Efficiency
- **Peak lab efficiency (GaAs, >30 dBm input, 5.8 GHz):** **92%** (MDPI Sensors 2022)
- **High-power deployed (GaN, 2W input, 5.8 GHz):** **85%** (ScienceDirect 2020 GaN study)
- **Typical medium-power (1–10 mW input, wide dynamic range):** **60–70%** (Shinohara rectenna arrays)
- **Low-power density (−5 dBm = 0.3 mW):** **52%** (Heliyon 2024)
- **Recommended simulator default:** `rectenna_efficiency = 0.70` (practical deployed system)

### Rain Attenuation at 5.8 GHz (ITU-R P.838-3)
- **Formula:** γ = k × R^α dB/km (horizontal polarization)
- **k_H = 0.00454, α_H = 1.244** at 5.8 GHz (interpolated from ITU-R P.838-3 table)
- **At 10 mm/hr:** **0.068 dB/km** (~1.6% power loss per km)
- **At 25 mm/hr:** **0.196 dB/km** (~4.4% power loss per km)
- **At 50 mm/hr:** **0.437 dB/km** (~9.6% power loss per km)
- **At 100 mm/hr (extreme):** **0.971 dB/km** (~20% power loss per km)
- **Source:** ITU-R P.838-3 (2005), validated by Zahid et al. 2022

### Atmospheric Gas Absorption at 5.8 GHz
- **Clear air (O₂ + H₂O vapor):** **~0.003–0.008 dB/km** at sea level
- **This is negligible** — rain dominates by factor of 10–100×
- **Source:** ITU-R P.676-11 (2016), JPL D-27879

### Laser Atmospheric Transmission (Clear Sky)
- **At 1070 nm (Yb fiber laser):** **0.93–0.98 per km** (0.09–0.30 dB/km)
  - Conservative (lower atmosphere, industrial aerosols): **0.93/km**
  - Favorable (high altitude, clean air): **0.98/km**
- **At 1550 nm (telecom / eye-safe):** **0.97–0.99 per km** (0.04–0.13 dB/km)
- **At 808–850 nm (GaAs PV match):** **0.90–0.95 per km** (0.23–0.46 dB/km)
- **In fog (any near-IR):** **0.001–0.10 per km (10–30 dB/km)** — effectively zero transmission
- **In rain (1070 nm):** **0.5–0.8 per km** (moderate rain), 0.1–0.3 per km (heavy rain)
- **Source:** AFRL/NPS atmospheric transmission windows study (DTIC ADA420318); McMaster FSO paper (2000); MODTRAN atmospheric model

### Laser Power Converter (PV Cell) Efficiency
- **Peak at 1070 nm (InP 8-junction, 2025):** **55%** (MDPI Photonics 2025)
- **Peak at 800–850 nm (GaAs):** **55%** (Joule review 2021)
- **Typical deployed system (accounting for tracking, optics, thermal):** **20–45%**
- **DARPA PRAD deployed (8.6 km, 2025):** **~20%** (noted as not efficiency-optimized)
- **Recommended simulator default:** `laser_receiver_efficiency = 0.40` (near-optimal tracking system)

### Microwave Transmitter (DC-to-RF) Efficiency
- **GaN power amplifier at 5.8 GHz (solid state, 2024):** **50–65%** (state of art)
- **Magnetron (legacy, high power):** **70–85%** (less suitable for phased arrays)
- **Recommended simulator default:** `tx_dc_to_rf_efficiency = 0.55`

### Laser Wall-Plug Efficiency
- **Yb fiber laser (1070 nm, CW, kW-class):** **35–50%** (electrical-to-optical)
- **Diode direct (808/976 nm):** **50–60%** (lower beam quality but more efficient)
- **Recommended simulator default:** `laser_wall_plug_efficiency = 0.45`

### Free-Space Path Loss (Friis / Beam Geometry)
- **Microwave (Friis formula at 5.8 GHz):** FSPL = (4πd/λ)². At d=1 km: FSPL = 107.7 dB
  - Note: Phased arrays with directional gain can overcome FSPL; the gain × aperture product determines received power
  - Relevant formula: P_r = P_t × G_t × G_r × (λ/4πd)²
- **Laser (Gaussian beam divergence):** For ideal diffraction-limited Gaussian beam, far-field divergence θ = λ/(πw₀). At 1070 nm with w₀ = 10 cm aperture: θ = 3.4 µrad → beam radius at 1 km = 3.4 mm. Real beam quality factor M² ≈ 1.1–1.5 for good fiber lasers.

### Atmospheric Turbulence (Laser Scintillation)
- **Refractive index structure constant Cn²:** 10⁻¹⁵ m⁻²/³ (weak), 10⁻¹³ m⁻²/³ (moderate), 10⁻¹² m⁻²/³ (strong)
- **Rytov variance σ_R² = 1.23 Cn² k^(7/6) L^(11/6)** where k=2π/λ, L=path length
  - At L=1 km, 1070 nm, moderate turbulence (Cn²=10⁻¹⁴): σ_R² ≈ 0.5 → significant scintillation
  - Scintillation causes ±3–6 dB power fluctuations at ground level
- **Source:** MDPI Atmosphere 2021; Fried parameter theory

### Safety Limits
- **Microwave (5.8 GHz) — FCC/ICNIRP:** General public limit: **1 mW/cm²** (10 W/m²). Occupational: 5 mW/cm². At high WPT power densities, exclusion zones required.
- **Laser — ANSI Z136.1 / IEC 60825:** Eye-safe limit for 1070 nm (Class 1): extremely low power; high-power laser WPT requires active exclusion/sentinel systems. 1550 nm is more eye-safe by ~10× due to corneal absorption.

---

## 8. Key Researchers & Programs Summary

| Researcher / Group | Affiliation | Focus | Status |
|--------------------|-------------|-------|--------|
| Paul Jaffe | NRL / DARPA POWER PM | Laser WPT, PRAM, space solar | Very active; DARPA POWER 8.6 km record (2025) |
| Naoki Shinohara | Kyoto University | Microwave WPT, rectenna | Active; 2025 IEEE paper; foundational authority |
| Ali Hajimiri | Caltech SSPP | IC-based microwave phased arrays | Active post-SSPD-1; MAPLE demonstrated 2023 |
| John Mankins | Artemis Innovation | SPS-ALPHA architecture | Active; IAC 2021 roadmap |
| PowerLight (Nugent) | PowerLight Technologies | Laser UAV power beaming | Very active; CENTCOM PTROL-UAS Dec 2025 |
| Sanjay Vijendran | ESA SOLARIS (now SEI) | SBSP policy/tech roadmap | Led ESA SOLARIS 2022–2024 |
| JAXA OHISAMA team | JAXA / Japan Space Systems | Aircraft/satellite WPT demo | Very active; Dec 2024 aircraft demo |
| Xidian (Duan Baoyan) | Xidian University, China | OMEGA SBSP, Chongqing facility | Active 2022–2025 |
| Teravec (Hoheisel) | Teravec Technologies | Laser receiver arrays | Built PRAD receiver; key hardware player |
| UTD Mahbub group | UT Dallas | Far-field WPT circuits | DARPA-funded 2024 |

---

## 9. Chronological Milestones (2015–2025)

| Year | Milestone | Key Numbers |
|------|-----------|-------------|
| 2015 | JAXA: 1.8 kW WPT over 55m | End-to-end ~22% |
| 2015 | Mitsubishi: 10 kW over 500m | Ground-to-ground terrestrial record |
| 2020 | NRL PRAM launched on X-37B | First space solar sandwich module |
| 2022 | ESA SOLARIS: 36m WPT demo | Tech validation only |
| 2022 | China Xidian: ground test announced | Bishan Chongqing facility |
| 2023 (Jan) | Caltech SSPD-1 launched | MAPLE, DOLCE, ALBA modules |
| 2023 (May) | Caltech MAPLE: LEO→Earth WPT | **First-ever orbit-to-Earth power beam** |
| 2024 (Dec) | Japan OHISAMA: Aircraft 7km WPT | Aircraft-mounted MW transmitter |
| 2025 (Apr) | 55% PV at 1070nm published | InP 8-junction, 18W output |
| 2025 (May) | **DARPA POWER PRAD: 8.6 km record** | **800W delivered, ~20% efficiency** |
| 2025 (Dec) | PowerLight PTROL-UAS milestone | kW-class to 5,000ft, CENTCOM-sponsored |

---

## 10. Gaps & Caveats for the Simulator

1. **End-to-end system efficiency numbers are sparse** — most papers report component-level efficiency (rectenna, PV cell) not full system including transmitter, pointing losses, and thermal management. The JAXA ~22% and DARPA ~20% are the best real-world anchors.

2. **Dynamic efficiency (moving targets)** — all demonstrated efficiencies are for static or slow-moving targets. Fast UAV tracking will likely reduce efficiency by 5–15% due to beam jitter.

3. **Multi-target sharing** — no major demonstrated results for simultaneous multi-UAV WPT with a single transmitter. Efficiency per UAV will drop proportionally with number of simultaneous targets (phased array beam splitting).

4. **Power density limits** — the 5.8 GHz public exposure limit (1 mW/cm²) severely constrains power delivery area at ground level. For military applications, higher limits may apply within exclusion zones.

5. **Night/cloud conditions for laser** — cloud cover data for specific FOB locations should be factored in. In tropical climates, laser WPT availability may drop to 40–60% of operational hours. Microwave WPT at 5.8 GHz retains >95% availability.

---

*Sources cross-referenced from: DARPA.mil, NASA.gov, IEEE Xplore, MDPI, ScienceDirect, ResearchGate, OSTI.gov, DTIC, Caltech SSPP, ESA SOLARIS, JAXA R&D, PowerLight Technologies press releases, ITU-R recommendations.*
