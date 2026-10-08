# Episode 27: Reading Maps, Census Data, and Greenprint

Builds habits for checking geography, vintage, uncertainty, access, and licensing in planning data.

## Sources and attribution

- [Toolbox Tuesday Training Archive](https://scag.ca.gov/toolbox-tuesday) by Southern California Association of Governments; published by Southern California Association of Governments.

This episode is an independent study production based on the sources listed above. Source attribution does not imply affiliation, approval, sponsorship, or endorsement by any author, publisher, or institution.

## License

No broad open license identified; original summary and attribution only

## Production notes

Preparation only. Not legal, planning, or financial advice. The narration is an original synthesis. Verify current law, guidance, course requirements, and source terms before relying on it.

Stable episode ID: `787d636d-7576-5eac-b4f4-7923632d31f1`

## Transcript

Imagine a Torrance hearing where two maps appear to disagree. One colors a tract as highly burdened. Another shows a corridor as relatively advantaged. A speaker cites a percentage from the American Community Survey, but the number came from a different five-year release than the staff report. A map looks authoritative because its boundaries are crisp. Good planning begins by asking what the map measures, when it was measured, how uncertain it is, and what disappears at that scale.

This episode is preparation, not legal, statistical, or survey advice for a specific decision. Datasets, geographic boundaries, web tools, and legal standards change. Use current metadata, official releases, local verification, the complete administrative record, and advice from the Torrance city attorney.

Read every map from the outside inward. Start with title and purpose. Then read the source, date, geography, legend, units, and notes. Identify whether the values are counts, percentages, rates, percentiles, modeled estimates, or categories. Only then inspect the colors.

A count answers how many. A percentage answers what share of a defined denominator. A rate usually normalizes by population, time, area, or exposure. A percentile ranks one place against others in the reference set. A modeled value estimates a condition from assumptions and inputs. These are not interchangeable.

Color choices can exaggerate or hide differences. A classification method may use equal intervals, quantiles, natural breaks, or policy thresholds. The same data can produce different visual stories under each method. Ask for the break values. If two places on opposite sides of a break have nearly identical values, do not narrate them as fundamentally different.

Geography creates another trap. Census tracts, block groups, blocks, ZIP Code Tabulation Areas, council districts, neighborhoods, parcels, and transportation analysis zones serve different purposes. Aggregating points into larger areas can hide local variation. Changing boundaries or scale can change an apparent relationship. This is sometimes called the modifiable areal unit problem.

Avoid the ecological fallacy. If a tract has a high share of renters, that does not mean every person in the tract is a renter. Area-level data describes an area, not the identity or behavior of each resident. Do not infer an individual's income, race, travel pattern, or vulnerability from a map polygon.

The decennial census aims to count the population and provides core demographic and housing information at detailed geographies. The American Community Survey, or ACS, provides a broader set of social, economic, housing, and demographic estimates. One-year ACS products cover larger populations with more current information. Five-year products combine more survey responses and reach smaller geographies, but represent a multi-year period.

An ACS value is an estimate. Read its margin of error. A difference between two estimates may not be meaningful when uncertainty is large. For a percentage, inspect both numerator and denominator. Small denominators can create unstable rates. When comparing releases, use compatible tables, geographies, inflation treatment where relevant, and nonoverlapping periods when trend claims require independence.

Do not say the ACS interviewed every resident. Do not call a five-year estimate a measurement of the final year. Do not compare a city one-year estimate with a tract five-year estimate without explaining the mismatch. Use the Census Bureau's table identifiers and metadata so another analyst can reproduce the result.

SCAG's public Toolbox Tuesday sessions support this data literacy. Its August 2025 session, Working With Census Data in R: Analyzing and Visualizing Trends, demonstrated reproducible access and visualization. Its May 2026 session on economic statistics explained major Census Bureau business datasets and newer access tools. Earlier SCAG sessions covered GIS modeling and regional analytics. The important habit is preserving a chain from source to transformation to visual.

For every number, record the dataset, table or field, vintage, universe, geography, retrieval date, and transformation. The universe is the population eligible for the measure. A table about workers is not a table about all residents. A poverty measure may exclude or treat some populations differently under the table definition.

Now add Greenprint. SCAG describes the SoCal Greenprint as an optional, flexible conservation-focused web-mapping tool for land-use and transportation decisions, conservation investment, funding, and mitigation planning. Its public thematic layers include agriculture and working lands, habitat and biodiversity, water resources, built environment, environmental justice and inclusion, climate vulnerability and resilience, and geographic context.

Greenprint can bring multiple regional layers into one view. It can help a planner identify overlap, generate questions, and compare alternatives. It does not make the decision. A layer may have a different date, resolution, extent, or method from the layer beneath it. Overlap does not prove causation, ownership, legal jurisdiction, habitat condition on a parcel, or the presence of a regulatory constraint.

SCAG's September 2026 public Toolbox Tuesday demonstrated the SoCal Greenprint. Use the tool according to current access terms and documentation. Cite the original layer when possible, not only the web viewer. If data is licensed, restricted, or proprietary, do not copy or redistribute it. The assignment in this course uses only public metadata, public outputs permitted by the source, and original analysis.

For practical application, build a map-reading card for one public Torrance planning question, such as heat and transit access. Select one Census or ACS variable and one public environmental layer. Write the decision question before opening the map. Record the source details for both layers.

Then complete six checks. Check one is meaning: what exactly does each variable measure? Check two is time: what period does it represent? Check three is scale: what geography or resolution is used? Check four is uncertainty: what margin of error, model limitation, or missing data applies? Check five is comparability: can the layers reasonably be combined? Check six is ground truth: what field observation or community evidence is needed?

Create two visual versions using different reasonable classifications. Describe how the story changes. Do not choose the version that best supports a preferred outcome. Choose the version that answers the decision question most honestly, and show the underlying values.

Add a privacy screen. Never publish a map that can identify a vulnerable person or household from sensitive records. Aggregate or suppress when needed. Public availability does not automatically make every reuse ethical.

Add a reproducibility log. Save the query or table identifiers, filters, calculations, software version, and retrieval date. Give the output a plain-language title and a limitations box. If you cannot reproduce the number, it is not ready to carry a finding.

Commissioners should ask simple questions that expose complex errors. What is the denominator? What year is this? What does the darkest color mean numerically? Is the difference larger than the uncertainty? Are we describing an area or assuming facts about individuals? What would we see at another scale?

Details change. A web map can update without a printed packet changing. Current metadata, source documentation, governing law, and city-attorney advice control.

Now three recall questions.

Question one. What should you read before interpreting map colors?

Answer. The title, purpose, source, date, geography, legend, units, notes, and classification breaks.

Question two. Why does an ACS estimate need its margin of error?

Answer. The ACS is a sample-based estimate. The margin helps show uncertainty and whether apparent differences may be too small to support a confident conclusion.

Question three. What can Greenprint do, and what can it not do?

Answer. It can organize public regional layers, reveal overlap, and support questions and alternatives. It cannot by itself prove causation, parcel conditions, regulatory status, or the correct policy decision.

Your learner artifact is the map-reading card, two classified map versions, and a reproducibility log. Use only public data you are permitted to use. Include source, vintage, universe, geography, uncertainty, retrieval date, transformation, privacy review, and limitations.

This lesson draws from SCAG's public Toolbox Tuesday materials from 2023 through 2026 on GIS modeling, Census and ACS analysis, economic statistics, environmental-justice tools, and the September 2026 SoCal Greenprint demonstration. It also uses public U.S. Census Bureau guidance on the decennial census, ACS estimates, geographies, and margins of error, plus SCAG's public description of Greenprint. The narration is original. No slide, map, recording, source prose, or proprietary data has been copied. Confirm current metadata, access terms, source documentation, legal requirements, and Torrance city-attorney advice.
