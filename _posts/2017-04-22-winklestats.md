---
layout: "post"
title: "WinkleStats"
date: "2017-04-22 17:57:34 +0000"
slug: "winklestats"
image: /assets/blog/winkles/01.jpg
show_hero: false
description: "The data, R scripts and figures behind my undergraduate study of periwinkle shell shape on exposed and sheltered shores, using PCA, clustering and multidimensional scaling."
original_publication: "WinkleStats"
original_url: "https://winklestats.wordpress.com/"
publication_tag: "Published on WinkleStats"
---

<p><strong>CONTAINS DATA, R SCRIPTS OF AN UNDERGRAD ASSIGNMENT<br>
Please read whole assignment</strong></p>

<p>As part of an undergraduate science degree at Anglia Ruskin University, we collected  rough periwinkles <em>(Littorina saxatilis)</em> in North Devon and this webpage is designed to ‘show what I have done’ with my data.</p>

<p>Read whole assignment here: <strong><a href="{{ '/assets/documents/winklestats/winklestats.pdf' | relative_url }}">WinkleStats</a></strong></p>

<hr>

<p>Winkle shape differences on exposed and versus sheltered shores are investigated using<br>
<strong>(1) Principal Component Analysis</strong> (PCA, normal and Bayesian),<br>
<strong>(2) Cluster Analysis</strong> (CLA, hierarchical and model based), and<br>
<strong>(3) Nonmetric Multidimensional Scaling (NMDS)</strong>.</p>

{% include blog-gallery.html gallery="gallery-1" unit="figures" %}

<p>Excel file of data can be downloaded here: <strong><a href="{{ '/assets/documents/winklestats/all_winkle_data.xlsx' | relative_url }}">All_winkle_data</a></strong><br>
 Excel file of all test results can be downloaded here: <strong><a href="{{ '/assets/documents/winklestats/winkle_output.xlsx' | relative_url }}">Winkle_output</a></strong><br>
 Full R script can be found here: <strong><a href="{{ '/assets/documents/winklestats/r-script-for-winklestats.docx' | relative_url }}">R script for WinkleStats</a></strong></p>

<p>All graph output can be found on Dropbox: <a href="https://www.dropbox.com/sh/r2shikhks4t9z5a/AADWEuThgWHZUFaJzhOOkiZ1a?dl=0">https://www.dropbox.com/sh/r2shikhks4t9z5a/AADWEuThgWHZUFaJzhOOkiZ1a?dl=0 </a></p>

<hr>

<p>General terms and approaches are described by <a href="http://onlinelibrary.wiley.com/doi/10.1111/mec.13536/full">Paily and Shankar</a> (2016). The analyses were performed on the three different data sets (log<sub>e</sub> transformed, ratios, geometric mean transformed), separately for exposed, sheltered and the combination of the two.</p>

{% include blog-gallery.html gallery="gallery-2" unit="figures" %}

<hr>

<p>THIS SECTION IS UNDER CONSTRUCTION</p>

<p>Orthogonal varimax rotation (Kaiser, 1958; Abdi and Williams, 2010) to attempt to maximize the loading variance in favour of one factor in each case, and zeros the remaining factors (Bellman, 2016) was applied for the PCA results reported.</p>

<p>Normal PCA treats variables as a fixed effect, the PCs are estimated only from the measured data (Nounoi et al., 2002). Information about range of variation and the mean value of PC loading and scores in not available.</p>

<p><strong>Bayesian statistics</strong> considers random, observable and unobservable quantities with a posterior probability density function. It conditions the observed data, allows external prior information about the variables, explores likelihood density, and evaluates the accuracy of posterior estimates.</p>

<p>Bayesian PCA on ratios. Biplots show the posterior distribution of individual winkles and how variable contributions change in Euclidean space.</p>

{% include blog-gallery.html gallery="gallery-3" unit="figures" %}

<p>The aim is to find <strong>biological significance</strong> by considering the first quartile, 50% and the last quartile of the PCA results. The likelihood of different morphotypes within the normal, the ratio and the GM data is put through a comprehensive data analysis. The Bayesian PCA, Cluster Analysis was carried out in R.3.4.0 with “bPCA”, “mclust”, “FactoMineR” and “factoextra” packages.</p>

<p>Firstly, descriptive statistics and correlation coefficients were extracted from each data set, then with Bayesian PCA the posterior distribution of eigenvalues, and explained variance and loadings were all calculated for the first, 50% and third quartile.</p>

{% include blog-gallery.html gallery="gallery-4" unit="figures" %}

<p>As “bPCA” does not have a function to extract variable contributions and individual contribution, normal PCA was analysed with “FactoMiner”. Orthogonal varimax rotation (Kaiser, 1958; Abdi and Williams, 2010) to attempt to maximize the loading variance in favour of one factor in each case, and zeros the remaining factors (Bellman, 2016) was applied for the PCA results reported.</p>

{% include blog-gallery.html gallery="gallery-5" unit="figures" %}

<p>Package <a href="https://cran.r-project.org/web/packages/mclust/mclust.pdf">“mclust”</a> (Fraley and Raftery, 1999) is an integrated approach to model-based hierarchical clustering via the Expectation Maximization (EM) (Dempster et al. 1977; Do and Batzoglou, 2008) algorithm. Classification and density estimation based on finite Gaussian mixture modelling with a variety of covariance structures through eigenvalue decomposition. The best model is chosen by the mclust() function which then produces a predicative clustering table.</p>

<p>The best model is chosen by the <a href="https://cran.r-project.org/web/packages/mclust/mclust.pdf"><strong>mclust()</strong> </a>function which then produces a predicative clustering table. For ratio data, <strong>Eigenvalue Decomposition Discriminant Analysis</strong> (EDDA, Bensmail and Celeux, 1996) clustered the exposed and sheltered samples precisely.</p>

<hr>

<p>Clustering of variables:</p>

{% include blog-gallery.html gallery="gallery-6" unit="figures" %}

<p>EDDA models:</p>

{% include blog-gallery.html gallery="gallery-7" unit="figures" %}

<p>Certainty of Finite Gaussian mixed models – see clustering tables and BIC reported in ‘Winkles output’ excel sheet:</p>

{% include blog-gallery.html gallery="gallery-8" unit="figures" %}

<p>Variable contribution posterior distribution of PC1, PC2 and PC3:</p>

{% include blog-gallery.html gallery="gallery-9" unit="figures" %}
