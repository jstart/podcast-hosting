# Episode 12: Statistics: Interpreting Public Claims Responsibly

Tests public claims using samples, center, spread, bias, uncertainty, and limits on causal inference.

## Sources and attribution

- [Introductory Statistics 2e](https://openstax.org/books/introductory-statistics-2e/pages/1-introduction) by OpenStax; published by OpenStax, Rice University.
- [Khan Academy](https://www.khanacademy.org/) by Khan Academy; published by Khan Academy.

This episode is an independent study production based on the sources listed above. Source attribution does not imply affiliation, approval, sponsorship, or endorsement by any author, publisher, or institution.

## License

CC BY-NC-SA 4.0; Copyrighted public lessons; original summary and attribution only

## Production notes

Preparation only. Not accredited instruction and does not establish transfer credit. The narration is an original synthesis. Verify current law, guidance, course requirements, and source terms before relying on it.

Stable episode ID: `09ccffbb-f493-5887-8836-6bb3ce8656a5`

## Transcript

A California city says average emergency response time fell by fifteen percent after a dispatch change. Is that evidence that the change worked, or could the result reflect which calls were counted, an unusually quiet month, or a new definition of response time? Statistics helps separate the measured claim from the causal story.

This is study preparation only. It awards no score, course credit, or transfer credit. The city and numbers in this episode are invented for practice.

Start by defining the data. A population is the full group we want to understand. A sample is the part actually observed. If the question concerns all emergency calls in a year but the report analyzes two hundred calls from April, those two hundred calls are the sample.

A parameter describes a population. A statistic describes a sample. The true annual mean response time is a parameter, usually unknown. The April sample mean is a statistic used to estimate it. Similar words do not make the quantities interchangeable.

A variable records a characteristic for each observational unit. Response time in minutes is quantitative. Call type, such as medical or fire, is categorical. A quantitative variable can be discrete, like the number of calls, or continuous, like elapsed time. Clear units and definitions are part of the variable. "Response time" is incomplete until we know when the clock starts and stops.

Sampling method affects what a sample can represent. In a simple random sample, every possible sample of a stated size has an equal chance of selection. A stratified sample divides the population into meaningful groups, such as call type, then samples within each group. A cluster sample randomly selects whole groups, perhaps dispatch zones, then studies calls in the chosen zones. A systematic sample might select every twentieth call after a random start.

Convenience samples use cases that are easy to reach. Voluntary response samples attract people who choose to participate. Both can be biased. If a city surveys only residents who completed an online complaint form, it may miss residents without reliable internet access and residents who gave up before completion.

An observational study records what happened without assigning treatments. An experiment deliberately assigns conditions. A city that compares response times before and after a software launch has an observational before-and-after comparison unless assignment was controlled. Confounding occurs when another factor changes alongside the factor of interest. Staffing, weather, call severity, and reporting rules can all confound the software comparison.

Descriptive statistics organize what was observed. Consider five response times: eight, nine, ten, eleven, and twenty-two minutes. To find the mean, add them. The total is sixty. Divide by five. The mean is twelve minutes. The median is the middle ordered value, which is ten minutes. The unusually long twenty-two-minute call pulls the mean above the median.

Quartiles divide ordered data into four parts. The interquartile range describes the spread of the middle half and resists extreme values better than the range. A box plot displays the median, quartiles, and potential outliers.

Variance and standard deviation use every observation. Standard deviation describes a typical distance from the mean in the variable's original units. A standard deviation of three minutes says more directly than a variance of nine squared minutes. Two districts can have the same mean response time but different standard deviations. The less consistent district poses a different policy problem.

A percentile states relative position. If a response time is at the ninetieth percentile, about ninety percent of observed times are at or below it. That does not mean the response was ninety percent correct or ninety percent faster. For public service, the median describes the middle case, while the ninetieth percentile draws attention to slower cases near the tail.

Distributions have shape, center, and spread. A symmetric distribution balances around its center. A right-skewed distribution has a longer tail toward larger values, common when most calls are handled quickly but a few take much longer. In a right-skewed distribution, the mean often exceeds the median. Report both when one number could conceal the shape.

Probability describes uncertainty. An outcome is one possible result. An event is a set of outcomes. Probability ranges from zero to one. A probability of zero means impossible under the model. One means certain under the model. Neither statement proves that the model matches reality.

Suppose twenty of one hundred sampled calls exceed fifteen minutes. The empirical probability of a sampled call exceeding fifteen minutes is twenty divided by one hundred, or zero point two. That is twenty percent. It estimates a broader rate only if the sample and measurement process are appropriate.

The complement of an event means the event does not occur. If the estimated probability of exceeding fifteen minutes is zero point two, the estimated probability of not exceeding fifteen minutes is one minus zero point two, or zero point eight.

A probability distribution pairs possible values with their probabilities. For a discrete count, the probabilities must be nonnegative and total one. Expected value is a long-run weighted average, not a promise for the next case.

Now examine two quantitative variables together. A scatter plot places one variable on each axis. Look for direction, form, strength, and unusual points. Positive association means larger values of one variable tend to accompany larger values of the other. Negative association means larger values tend to accompany smaller values.

Correlation measures the strength and direction of a linear relationship. It ranges from negative one to positive one. Values near positive one indicate strong positive linear association. Values near negative one indicate strong negative linear association. Values near zero indicate little linear association, but a strong curved relationship can still exist.

Correlation has no units and is sensitive to outliers. It also does not establish causation. Ice cream sales and heat-related calls may rise together because temperature influences both. Removing one unusual district can change the correlation substantially, so inspect the scatter plot before summarizing it.

A least-squares regression line predicts an output from an input by minimizing the sum of squared residuals. Suppose a simple model predicts response time in minutes as eighteen minus one point five times the number of available units. With six units, multiply one point five by six, giving nine. Subtract nine from eighteen. The predicted response time is nine minutes.

The slope is negative one point five minutes per additional available unit. The intercept, eighteen minutes at zero available units, may not be operationally meaningful. An intercept can be mathematically necessary without being a sensible real-world scenario.

A residual is actual value minus predicted value. If the actual response took eleven minutes and the model predicted nine, the residual is positive two minutes. Positive means the actual value lies above the prediction. A curved residual pattern signals that the linear model misses structure.

Prediction within the observed input range is interpolation. Prediction far beyond that range is extrapolation and carries more risk. If data cover two through eight available units, predicting twenty units assumes the same linear pattern continues where it was never observed.

Return to the civic claim. Last quarter, two hundred calls had a mean response time of forty minutes and a median of thirty. This quarter, one hundred fifty calls had a mean of thirty-four and a median of thirty-two. The mean fell fifteen percent because six divided by forty is zero point one five. Yet the median rose by two minutes, and the caseload fell.

The accurate conclusion is limited: the measured mean was lower in this quarter under the reported definition. To claim that dispatch software caused improvement, investigate sampling, call mix, missing data, clock definitions, staffing, weather, ordinary variation, and the distribution of times. One correct percentage cannot answer all those questions.

Three questions.

First, what is the difference between a population parameter and a sample statistic?

Second, why might a city report both the median and the ninetieth percentile?

Third, what does a positive residual mean?

First answer: a parameter describes the full population, while a statistic describes the observed sample and may estimate the parameter.

Second answer: the median shows the middle case, while the ninetieth percentile reveals performance among relatively slow cases near the upper tail.

Third answer: the actual observed value was greater than the regression model predicted.

Artifact: write a one-page audit of a real chart or numerical claim from a California local-government report. Identify the population, sample, variables, sampling risk, distribution shape if available, center, spread, and any correlation or regression claim. Recalculate one reported percentage, name one plausible confounder, and state the strongest conclusion the evidence supports.

Source note: Original study audio based on public learning materials, without quoting source prose. See OpenStax, Introductory Statistics 2e, Chapter 1, Sampling and Data; Chapter 2, Descriptive Statistics; Chapter 3, Probability Topics; and Chapter 12, Linear Regression and Correlation. Access for free at openstax.org. The current OpenStax web preface identifies Introductory Statistics 2e as licensed under Creative Commons Attribution-NonCommercial-ShareAlike 4.0, or CC BY-NC-SA 4.0. Also consult Khan Academy public Statistics and Probability lessons on study design, descriptive statistics, probability, distributions, scatter plots, correlation, least-squares regression, and residuals.

Preparation only. No credit or transfer credit is awarded by this episode.
