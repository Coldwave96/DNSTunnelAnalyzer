# DNSTunnelAnalyzer
Domain Name System (DNS) is a popular way to steal sensitive information from enterprise networks and maintain a covert tunnel for command and control communications with a malicious server. Due to the significant role of DNS services, enterprises often set the firewalls to let DNS traffic in, which encourages the adversaries to exfiltrate encoded data to a compromised server controlled by them.

A two-layered hybrid approach is used to detect low and slow data exfiltration and tunneling over DNS.

## Datasets Details
The dataset used for this research is the CIC-Bell-DNS-EXF-2021 dataset developed by the Canadian Institute of Cybersecurity. This dataset can be found [here](https://www.unb.ca/cic/datasets/dns-exf-2021.html).

## Model Design
### Layer 1
* Random Forest Classifier (RF)
* Decision Tree Classifier (DT)

### Layer 2
* MLP (Multilayer Perceptron)

## Detect Progress
* the stateless features are extracted from the incoming DNS traffic in window τ (window of packets), and then the structured data goes through a trained classifier. The classifier output probability is then divided into three bins, i.e., [0-0.4), [0.4-0.7), [0.7-1] to help the classifier score each input sample in window τ as benign, suspicious, or malicious.
* If the ratio of the suspicious samples in window τ, i.e., r_sus^τ, exceeds the threshold δ, the whole traffic window is re-analyzed using stateful features to let the trained classifier on stateful features decide about the whole window τ. Otherwise, the input sample is either identified as benign for which the DNS traffic keeps on flowing or is detected as attack for which we terminate the DNS traffic.
