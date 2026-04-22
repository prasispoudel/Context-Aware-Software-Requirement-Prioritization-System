# Context-Aware Software Requirements Prioritization System

## Overview

Effective prioritization of software requirements is critical for reducing project risk, optimizing resource allocation, and ensuring timely delivery. Traditional prioritization techniques such as **Analytic Hierarchy Process (AHP)** and **MoSCoW** rely heavily on manual judgment, making them subjective, inefficient, and poorly scalable for large or evolving projects.

This repository presents a **machine learning–based, context-aware software requirements prioritization system** that automatically analyzes textual requirement statements, infers project-specific contextual factors, and predicts **continuous priority scores** to support transparent and reliable decision-making.

The system is designed as a **decision-support tool** for requirements engineers, system analysts, and project managers.

---

##  Key Contributions

* Automated prioritization of textual software requirements
* Context-aware modeling using multiple inferred requirement attributes
* Separation of **context inference (NLP)** and **priority prediction (ML)**
* Explainable and transparent prioritization outputs
* Empirical validation against expert judgments
* Scalable and extensible system design

---

##  System Architecture

The system follows a modular pipeline:

1. **Requirement Input**

   * Natural language requirement statements (from SRS or similar artifacts)

2. **Contextual Feature Inference (NLP Layer)**

   * Infers contextual attributes such as:

     * Risk
     * Complexity
     * Urgency
     * Dependencies
     * Effort
     * Stability
   * Uses transformer-based language models and ordinal classification techniques

3. **Priority Prediction (Machine Learning Layer)**

   * An optimized machine learning model predicts **continuous priority scores**
   * Scores are used to rank requirements objectively

4. **Explainability & Analysis**

   * Feature contribution analysis enables interpretability
   * Supports transparent prioritization decisions

5. **Decision Support Output**

   * Ranked list of requirements
   * Suitable for planning, sprint selection, and release management

---

##  Machine Learning Methodology

### Context Estimation

* Transformer-based NLP models (e.g., RoBERTa) fine-tuned on requirement text
* Ordinal regression used to preserve natural ordering of contextual attributes

### Priority Modeling

* Integrated regression-based learning approach
* Continuous-valued priority estimation instead of coarse categorical labels
* Model selection and tuning performed using appropriate evaluation metrics

### Evaluation

* Quantitative evaluation using:

  * RMSE / MAE
  * Rank correlation metrics
* Qualitative validation through **expert judgment comparison**

---

##  Why Context Awareness Matters

Most ML-based prioritization approaches focus solely on textual similarity or historical labels. This system explicitly models **project-specific context**, enabling:

* Reduced bias in prioritization
* Improved scalability for large requirement sets
* Better alignment with real-world project constraints
* More reliable decision support under uncertainty

---

##  Publication

This work has been published in a **Scopus-indexed journal**:

**Title:**
*Context-Aware Requirements Prioritization Using Integrated Regression Learning with Ordinal Neural Modeling and RoBERTa*

**Journal:**
International Journal of Advanced Computer Science and Applications (IJACSA)

**DOI:**
[https://dx.doi.org/10.14569/IJACSA.2025.0161293](https://dx.doi.org/10.14569/IJACSA.2025.0161293)

---

## Author

**Prasis Poudel**
Machine Learning Engineer | Software Engineer
MSc in Software Engineering

---

##  Use Cases

* Requirement prioritization for large-scale software projects
* Decision support for sprint and release planning
* Research and experimentation in requirements engineering
* Integration into software project management tools

---

##  Future Work

* Integration with real-time project management systems
* Enhanced explainability dashboards
* Feedback-driven online learning
* Extension to multi-project prioritization scenarios

---

##  License

This project is intended for academic and research purposes.
Please cite the associated publication if you use this work in your research.

---


