# JPL Academic Divisions

## Objective
This project aims to demonstrate Natural Language Processing by answering the following problem:

**Can we identify the scientific field a JPL author belongs to?**

For this project, we will use Caltech's academic divisions as a way to define a scientific field. Caltech has 6 academic divisions:
- Biology and Biological Engineering
- Chemistry and Chemical Engineering
- Engineering and Applied Science
- Geological and Planetary Sciences
- Humanities and Social Science
- Physics, Mathematics and Astronomy

Thus, the problem changes to the following:

**Can we determine which Caltech academic division a JPL author most likely belongs to?**

## General Tasks

### Gathering Publication Data
We must source publication data from Caltech and JPL to accomplish this task. We obtained articles and conference proceedings from Web of Science with the following filter:
- `Organization-Enhanced`: Califonia Institute of Technology or NASA Jet Propulsion Lab
- `Dates`: Last 5 years (2017 - 2021)

Here are the number of publications found:
- `Caltech`: 19206
- `JPL`: 8310

We will store all of this data into MongoDB

### Data Cleaning and Processing
Determine which fields from the Web of Science output that will be used for the analysis

### Calculate TF-IDF vector representation of each document

### Create `Author` document

### Create `Division` document

### Perform similarity calculation between JPL `Author` and `Division`

### Create dashboard to visualize similarity of JPL `Author` to all `Division`s