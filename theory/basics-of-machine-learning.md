---
description: 'Author:'
---

# NORBIT MBES Snippets

## I**ntroduction**

 **pawel - Jens - Can we use it?**

Sidescan sonar systems are widespread in geological seafloor mapping and so far they are the devices of choice in German territories for habitat mapping. This ECOMAP deliverable aims to elaborate how modern multibeam echosounder systems perform in comparison with classical sidescan using data examples.

Advantages of towed sidescan sonar systems comprise their ease of use and subsequent data processing as well as their large swath ranges and a geometry that is favorable for the detection of objects. Nevertheless, traditional sidescan sonar systems also have considerable disadvantages that are mitigated by the application of exactly geo-located multibeam beam echosounder \(MBES\) sidescan-like backscatter data commonly referred to as snippets. Earlier surveys demonstrated that snippet multibeam backscatter maps can be of comparable or even better resolution compared to classical sidescan sonar mosaics when recorded with similar acoustic ranges, e.g. for the detection of unexploded ordnance in the Baltic Sea \(Kunde et al., 2018\). In this report we want to elucidate the potential of the NORBIT MBES for assessing sidescan-like data.

Modern shallow water multibeam systems typically form 512 individual beams. Bathymetry and co-registered backscatter are available in realtime. In postprocessing the true incidence angle on the seabed can be calculated and thus correction of the backscattering strength with respect to the intrinsic angular backscattering response becomes feasible as implemented in the GEOCODER toolbox \(Fonseca and Calder 2005\). Sidescan sonar systems record backscattering strength time series, usually lack depth measurement, and suffer in limited underwater positioning accuracy. In contrast MBES systems are nowadays coupled with highly accurate inertial navigation and motion system \(IMU\) fed by real time global navigation satellite systems \(GPS, BEIDOU, GLONASS, GALILEO\). Especially in coastal areas positioning can be even improved through real time kinematic \(RTK\) corrections, allowing for appr. 2 cm accurate lateral and twice as high vertical positioning. Therefore IMU-RTK guided MBES in shallow coastal waters outperforms underwater navigation such as USBL systems by an order of magnitude.

Sidescan systems only form one wide beam to starboard and port each but do not offer angle dependent individual beams and lack bathymetry. Therefore, the true incidence of sound on the seabed remains unknown and the intrinsic angular range curve function can neither be fully evaluated for seabed classification nor corrected for ideal imagery. Furtheron, angle dependent refraction effects caused by complex oceanographic setting being especially valid for the Baltic Sea can not be compensated. Sidescan sonar \(with the exception of phase measuring bathymetry systems, which are intrinsically noisy\) lack the precisely co-registered bathymetric information. This offsets the advantages of sidescan sonar systems for object ****detection in many circumstances. Of special interest here is the reliable detection of boulders \(Feldens et al., 2019\), with the upcoming research topic of the detection of vegetated boulders.

This document defines the various forms of MBES backscatter and lists the technological advancement of NORBIT for snippets. It also compares classical sidescan sonar systems and multibeam echo sounder snippet-derived seafloor maps for BONUS ECOMAP relevant topics.

## Technological advancement: MBES Snippet-derived backscatter

There are various types of backscattering strength data that can be formed by MBES. We hereby want to explain and showcase the 6 different types of NORBIT WBMS and WBMS STX backscattering strength information.

Each mode reflects different data characteristics and is used to optimize different operational scenarios. All modes are produced over the full frequency band of NORBIT WBMS systems from 160kHz to 700kHz that allows further multispectral analysis \(Feldens et al., 2018\).

- Water Column \(WC\)

- Bottom Detection Backscatter \(BDB\)

- Sidescan \(SS\)

- Snippets data \(SN\) and Snippets Backscattering Strength \(BS\)

- Snippets-Sidescan \(SN-SS\)

\*\*\*\*

