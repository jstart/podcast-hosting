# Episode 7: Build a Reproducible API Query

Constructs Census API requests from year, dataset, variables, and geography.

## Sources and attribution

- [Introduction to the Census Bureau Data API](https://www.census.gov/data/academy/courses/intro-to-the-census-bureau-data-api.html) by U.S. Census Bureau Census Academy instructors; published by U.S. Census Bureau Census Academy.
- [Census Data API User Guide](https://www.census.gov/data/developers/guidance/api-user-guide.html) by U.S. Census Bureau; published by U.S. Census Bureau.
- [Census Data API Terms of Service](https://www.census.gov/data/developers/about/terms-of-service.html) by U.S. Census Bureau; published by U.S. Census Bureau.
- [About Torrance](https://www.torranceca.gov/Government/About-Torrance) by City of Torrance; published by City of Torrance.

This episode is an independent study production based on the sources listed above. Source attribution does not imply affiliation, approval, sponsorship, or endorsement by any author, publisher, or institution.

## License

U.S. Government work not subject to copyright in the United States; API terms apply; Use subject to Census Data API Terms of Service and required non-endorsement notice; Copyrighted local government webpage; facts summarized with attribution, no expressive text reproduced

## Production notes

Independent educational production. Not an official U.S. Census Bureau or City of Torrance course, not endorsed or certified by either, and not legal or statistical advice. The narration is an original synthesis. Verify current law, guidance, course requirements, and source terms before relying on it.

Stable episode ID: `1f0de947-bccd-5145-bce3-86e9dae74b20`

## Transcript

This episode focuses on API construction. Census data becomes useful when the population, measure, geography, and time period are stated before anyone searches for a number.

A Census Data API request combines a year, dataset path, requested variables, and geography. Begin with the dataset discovery page and variables metadata instead of guessing variable names.

The get clause selects fields. The for clause identifies the target geography, and an in clause supplies its parent where required. Store the complete request URL, response, retrieval time, and software transformation.

Check returned headers and geography codes before converting text to numbers. Handle nulls, annotations, changed variables, and API errors explicitly. Respect service limits and cache results rather than sending needless repeated calls.

Torrance application segment. This local application is separate from the Census Academy instruction. The cited City of Torrance primary source is About Torrance, published at https://www.torranceca.gov/Government/About-Torrance. For a local analysis, derive Torrance's official place code through Census geography metadata, then save a query whose universe and vintage match the local question. Do not present City policy or administrative records as Census Bureau findings, and do not present a federal estimate as adopted City policy.

Keep a reproducibility packet containing the question, source URLs, exact vintage, table or query, geography codes, raw result, calculations, and uncertainty note. This narration is an original synthesis of cited U.S. Census Bureau government works and separately cited City of Torrance material. Third-party videos, software, graphics, and linked works are excluded. This product uses Census Bureau information but is not endorsed or certified by the Census Bureau. It is not an official City product and does not imply City endorsement.
